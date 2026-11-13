"""Celery application configuration for background jobs (NFR-2, NFR-21)."""

from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()
celery_app = Celery(
    "founders_carnet",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(
    accept_content=["json"],
    broker_connection_retry_on_startup=True,
    result_serializer="json",
    task_serializer="json",
    timezone="UTC",
    imports=("app.tasks",),
    beat_schedule={
        "purge-due-accounts": {
            "task": "app.tasks.purge_due_accounts",
            "schedule": crontab(minute="*/15"),
        },
    },
)
