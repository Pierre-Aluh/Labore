import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from sqlalchemy.dialects import postgresql

from app.models import Base


EXPECTED_TABLES = {
    "users",
    "companies",
    "company_users",
    "roles",
    "permissions",
    "role_permissions",
    "user_roles",
    "departments",
    "competencies",
    "competency_requirements",
    "bank_accounts",
    "document_categories",
    "documents",
    "accounting_movements",
    "movement_documents",
    "tickets",
    "ticket_participants",
    "ticket_messages",
    "ticket_attachments",
    "notifications",
    "audit_logs",
    "sessions",
}


def test_metadata_contains_all_phase_two_tables() -> None:
    assert EXPECTED_TABLES.issubset(Base.metadata.tables)
    assert "documents" in Base.metadata.tables
    assert "data" not in Base.metadata.tables["documents"].columns


def test_schema_uses_postgresql_types_for_uuid_and_audit_metadata() -> None:
    document_table = Base.metadata.tables["documents"]
    assert isinstance(document_table.c.id.type, postgresql.UUID)
    audit_table = Base.metadata.tables["audit_logs"]
    assert isinstance(audit_table.c.metadata_json.type, postgresql.JSONB)


def test_initial_migration_exists() -> None:
    migration = Path(__file__).parents[1] / "migrations" / "versions" / "0001_initial_schema.py"
    assert migration.exists()
