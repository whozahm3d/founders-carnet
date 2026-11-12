"""Private disk cache for user-scoped structured Gemini responses."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import time
from collections.abc import Callable
from pathlib import Path

from app.config import _REPOSITORY_ROOT, get_settings


DEFAULT_CACHE_TTL_SECONDS = 24 * 60 * 60
_HASH_PATTERN = re.compile(r"^[a-f0-9]{64}$")


class StructuredResponseDiskCache:
    def __init__(
        self,
        cache_dir: Path,
        *,
        ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("Cache TTL must be positive")
        self.root = _validated_cache_root(cache_dir)
        self.ttl_seconds = ttl_seconds
        self._clock = clock

    def make_key(
        self,
        *,
        model_name: str,
        fallback_model: str | None,
        operation: str,
        prompt_version: str,
        system_instruction: str,
        payload: dict[str, object],
        schema: dict[str, object],
        output_instruction: str,
    ) -> str:
        request = {
            "model": model_name,
            "fallback_model": fallback_model,
            "operation": operation,
            "prompt_version": prompt_version,
            "system_instruction": system_instruction,
            "payload": payload,
            "schema": schema,
            "output_instruction": output_instruction,
        }
        canonical = json.dumps(request, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def get(self, scope: int | str, key: str) -> str | None:
        path = self._entry_path(scope, key)
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
            if entry.get("key") != key or entry.get("expires_at", 0) <= self._clock():
                path.unlink(missing_ok=True)
                return None
            response_json = entry.get("response_json")
            return response_json if isinstance(response_json, str) else None
        except FileNotFoundError:
            return None
        except (OSError, json.JSONDecodeError, AttributeError, TypeError):
            return None

    def set(self, scope: int | str, key: str, response_json: str) -> None:
        path = self._entry_path(scope, key)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        entry = json.dumps(
            {
                "key": key,
                "expires_at": self._clock() + self.ttl_seconds,
                "response_json": response_json,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                prefix=".cache-",
                suffix=".tmp",
                delete=False,
            ) as cache_file:
                temp_path = Path(cache_file.name)
                cache_file.write(entry)
            os.replace(temp_path, path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def remove(self, scope: int | str, key: str) -> None:
        self._entry_path(scope, key).unlink(missing_ok=True)

    def clear_scope(self, scope: int | str) -> None:
        directory = self._scope_directory(scope)
        if directory.exists():
            resolved = directory.resolve()
            if resolved.parent != self.root:
                raise RuntimeError("Invalid private cache scope path")
            shutil.rmtree(resolved)

    def _entry_path(self, scope: int | str, key: str) -> Path:
        if not _HASH_PATTERN.fullmatch(key):
            raise ValueError("Invalid structured cache key")
        path = self._scope_directory(scope) / f"{key}.json"
        if path.parent.resolve() != self.root and self.root not in path.parent.resolve().parents:
            raise RuntimeError("Invalid private cache path")
        return path

    def _scope_directory(self, scope: int | str) -> Path:
        scope_hash = hashlib.sha256(str(scope).encode("utf-8")).hexdigest()
        return self.root / scope_hash


def clear_structured_response_cache(scope: int | str) -> None:
    cache = StructuredResponseDiskCache(get_settings().llm_cache_dir)
    cache.clear_scope(scope)


def _validated_cache_root(cache_dir: Path) -> Path:
    root = cache_dir.expanduser().resolve()
    repository_root = _REPOSITORY_ROOT.resolve()
    private_base = (_REPOSITORY_ROOT / "backend" / ".private").resolve()
    served_directory = (_REPOSITORY_ROOT / "frontend" / "public").resolve()
    if (
        root == served_directory
        or served_directory in root.parents
        or (root.is_relative_to(repository_root) and not root.is_relative_to(private_base))
    ):
        raise RuntimeError("Structured response cache must be private and outside served source directories")
    return root
