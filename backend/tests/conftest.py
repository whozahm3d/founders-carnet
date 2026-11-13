from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.tasks as background_tasks
from app.celery_app import celery_app
from app.database import get_db
from app.main import app
from app.models import Base

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


class FakeTaskEncoder:
    model_name = "test-embedding-model"

    def encode(self, texts: list[str]) -> tuple[tuple[float, float], ...]:
        return tuple((1.0, 0.0) for _text in texts)


def override_get_db() -> Generator[Session, None, None]:
    with TestSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
def reset_database():
    original_session_factory = background_tasks.database_session_factory
    original_encoder_factory = background_tasks.configured_encoder_factory
    original_task_always_eager = celery_app.conf.task_always_eager
    background_tasks.database_session_factory = TestSessionLocal
    background_tasks.configured_encoder_factory = FakeTaskEncoder
    celery_app.conf.task_always_eager = True
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    celery_app.conf.task_always_eager = original_task_always_eager
    background_tasks.database_session_factory = original_session_factory
    background_tasks.configured_encoder_factory = original_encoder_factory
