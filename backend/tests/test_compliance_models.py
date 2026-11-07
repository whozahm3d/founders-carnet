from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool

from app.models import Base


def test_compliance_tables_build_on_sqlite_for_local_tests():
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)

    table_names = set(inspect(engine).get_table_names())

    assert {
        "compliance_documents",
        "compliance_chunks",
        "compliance_queries",
        "compliance_citations",
    }.issubset(table_names)
    assert "embedding" in {
        column["name"] for column in inspect(engine).get_columns("compliance_chunks")
    }
    engine.dispose()
