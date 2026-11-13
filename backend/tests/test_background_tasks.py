from datetime import datetime, timedelta

from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.celery_app import celery_app
from app.config import Settings
from app.feature_models import EcosystemProfile, ResumeOptimization
from app.models import Base, ComplianceQuery, ConsentRecord, User
from app.services import llm_cache, resume_optimizer
from app.services.matching import profile_match_text
from app.tasks import purge_due_accounts, regenerate_ecosystem_profile_embedding


class FakeEncoder:
    model_name = "test-profile-embedding-v1"

    def __init__(self):
        self.texts = []

    def encode(self, texts):
        self.texts.extend(texts)
        return ([0.25, 0.75],)


def _task_database(monkeypatch, tmp_path):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    settings = Settings(
        llm_cache_dir=tmp_path / "private-cache",
        resume_storage_dir=tmp_path / "private-resumes",
    )
    monkeypatch.setattr("app.tasks.database_session_factory", session_factory)
    monkeypatch.setattr(llm_cache, "get_settings", lambda: settings)
    monkeypatch.setattr(resume_optimizer, "get_settings", lambda: settings)
    return engine, session_factory, settings


def _make_user(session, email, *, active=True, deletion_scheduled_for=None):
    user = User(
        email=email,
        full_name="Background Task User",
        hashed_password="test-hash",
        role="talent",
        is_active=active,
        deletion_requested_at=datetime(2025, 1, 1) if deletion_scheduled_for else None,
        deletion_scheduled_for=deletion_scheduled_for,
    )
    session.add(user)
    session.flush()
    return user


def test_profile_embedding_task_regenerates_with_current_model(monkeypatch, tmp_path):
    engine, session_factory, _settings = _task_database(monkeypatch, tmp_path)
    encoder = FakeEncoder()
    monkeypatch.setattr("app.tasks.configured_encoder_factory", lambda: encoder)
    try:
        with session_factory() as session:
            user = _make_user(session, "embedding-task@example.com")
            profile = EcosystemProfile(
                user_id=user.id,
                sector="logistics",
                stages=["mvp"],
                skills=["operations"],
                availability="open",
                location="Lahore",
                summary="Supports early logistics teams.",
                consent_version="ecosystem-profile-v1",
                embedding=None,
                embedding_model=None,
            )
            session.add(profile)
            session.commit()
            profile_id = profile.id
            expected_text = profile_match_text(profile)

        result = regenerate_ecosystem_profile_embedding.run(profile_id)

        with session_factory() as session:
            updated = session.get(EcosystemProfile, profile_id)
            assert result == "updated"
            assert updated.embedding == [0.25, 0.75]
            assert updated.embedding_model == "test-profile-embedding-v1"
        assert encoder.texts == [expected_text]
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_account_purge_removes_due_user_data_and_private_resume_and_cache(
    monkeypatch, tmp_path
):
    engine, session_factory, settings = _task_database(monkeypatch, tmp_path)
    cutoff = datetime(2026, 1, 31, 12, 0, 0)
    due_for = cutoff - timedelta(days=1)
    future_for = cutoff + timedelta(days=1)
    try:
        with session_factory() as session:
            due_user = _make_user(
                session,
                "purge-due@example.com",
                active=False,
                deletion_scheduled_for=due_for,
            )
            due_user_id = due_user.id
            session.add(
                ConsentRecord(
                    user_id=due_user.id,
                    consent_type="registration",
                    consent_version="v1",
                    source="web",
                )
            )
            session.add(
                ComplianceQuery(
                    user_id=due_user.id,
                    question="Private compliance question",
                    outcome="abstained",
                )
            )
            session.add(
                EcosystemProfile(
                    user_id=due_user.id,
                    sector="logistics",
                    stages=["mvp"],
                    skills=[],
                    availability="open",
                    location="Lahore",
                    summary="Private profile summary",
                    consent_version="ecosystem-profile-v1",
                )
            )
            resume = ResumeOptimization(
                user_id=due_user.id,
                storage_key="a" * 32,
                file_sha256="b" * 64,
                target_role="Engineer",
                processing_consent_version="v1",
                status="completed",
                prompt_version="resume-v1",
                model_name="test-model",
            )
            session.add(resume)

            future_user = _make_user(
                session,
                "purge-future@example.com",
                active=False,
                deletion_scheduled_for=future_for,
            )
            future_user_id = future_user.id
            still_active = _make_user(
                session,
                "purge-active@example.com",
                active=True,
                deletion_scheduled_for=due_for,
            )
            still_active_id = still_active.id
            session.commit()

        resume_path = settings.resume_storage_dir / f"{'a' * 32}.pdf"
        resume_path.parent.mkdir(parents=True, exist_ok=True)
        resume_path.write_bytes(b"private resume")
        cache = llm_cache.StructuredResponseDiskCache(settings.llm_cache_dir)
        cache_key = "c" * 64
        cache.set(due_user_id, cache_key, '{"private":"result"}')

        purged_count = purge_due_accounts.run(cutoff.isoformat())

        with session_factory() as session:
            assert session.get(User, due_user_id) is None
            assert session.get(User, future_user_id) is not None
            assert session.get(User, still_active_id) is not None
            assert (
                session.scalar(
                    select(ConsentRecord.id).where(ConsentRecord.user_id == due_user_id)
                )
                is None
            )
            assert (
                session.scalar(
                    select(ComplianceQuery.id).where(
                        ComplianceQuery.user_id == due_user_id
                    )
                )
                is None
            )
            assert (
                session.scalar(
                    select(EcosystemProfile.id).where(
                        EcosystemProfile.user_id == due_user_id
                    )
                )
                is None
            )
            assert (
                session.scalar(
                    select(ResumeOptimization.id).where(
                        ResumeOptimization.user_id == due_user_id
                    )
                )
                is None
            )
        assert purged_count == 1
        assert not resume_path.exists()
        assert cache.get(due_user_id, cache_key) is None
        assert purge_due_accounts.run(cutoff.isoformat()) == 0
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_celery_tasks_are_registered_without_running_a_worker():
    assert "app.tasks.regenerate_ecosystem_profile_embedding" in celery_app.tasks
    assert "app.tasks.purge_due_accounts" in celery_app.tasks
    assert regenerate_ecosystem_profile_embedding.ignore_result is True
    assert purge_due_accounts.ignore_result is True
