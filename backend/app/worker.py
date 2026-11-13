"""Celery worker entrypoint for the registered background tasks."""

from app.celery_app import celery_app

__all__ = ["celery_app"]
