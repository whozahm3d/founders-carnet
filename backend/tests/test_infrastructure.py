import importlib.util
from pathlib import Path

from app.celery_app import celery_app
from app.config import Settings
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXPORT_SCRIPT = REPOSITORY_ROOT / "scripts" / "export_openapi.py"
spec = importlib.util.spec_from_file_location("export_openapi", EXPORT_SCRIPT)
assert spec is not None and spec.loader is not None
export_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_module)
export_openapi = export_module.export_openapi


def test_celery_uses_configured_redis_url() -> None:
    settings = Settings(REDIS_URL="redis://example.test:6380/4")
    assert settings.redis_url == "redis://example.test:6380/4"


def test_celery_app_has_json_safe_worker_defaults() -> None:
    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.result_serializer == "json"
    assert celery_app.conf.accept_content == ["json"]


def test_celery_schedules_due_account_purges() -> None:
    schedule = celery_app.conf.beat_schedule["purge-due-accounts"]
    assert schedule["task"] == "app.tasks.purge_due_accounts"
    assert schedule["schedule"].minute == {0, 15, 30, 45}


def test_compose_declares_database_redis_api_worker_and_beat_services() -> None:
    compose = (REPOSITORY_ROOT / "compose.yaml").read_text(encoding="utf-8")
    for service in ("  db:\n", "  redis:\n", "  api:\n", "  worker:\n", "  beat:\n"):
        assert service in compose
    assert "founders_carnet_redisdata:" in compose


def test_openapi_export_contains_existing_api_routes(tmp_path: Path) -> None:
    output_path = export_openapi(tmp_path / "openapi.json")
    assert output_path.exists()
    schema = output_path.read_text(encoding="utf-8")
    assert '"/api/v1/auth/register/{role}"' in schema
    assert '"/api/v1/jobs"' in schema
    assert '"/api/v1/verification/me"' in schema

