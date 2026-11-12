"""Export the current FastAPI schema to backend/openapi.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.main import app  # noqa: E402


def export_openapi(output_path: Path = BACKEND_ROOT / "openapi.json") -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


if __name__ == "__main__":
    path = export_openapi()
    print(f"Exported OpenAPI schema to {path}")

