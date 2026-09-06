"""Seed the initial RBAC catalog and departments."""

from alembic import op

revision = "0002_seed_rbac"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None

ROLES = ["Administrador", "Contador", "Fiscal", "Departamento Pessoal", "Atendimento", "Cliente"]
DEPARTMENTS = ["Contábil", "Fiscal", "Departamento Pessoal", "Legalização", "Financeiro", "Outros"]
PERMISSIONS = [
    ("companies", "view"), ("companies", "create"), ("companies", "update"),
    ("users", "view"), ("users", "create"), ("users", "update"),
    ("roles", "view"), ("roles", "manage"), ("departments", "view"), ("departments", "create"),
    ("documents", "view"), ("documents", "create"), ("documents", "download"),
    ("documents", "update"), ("documents", "delete"),
    ("tickets", "view"), ("tickets", "create"), ("tickets", "respond"),
    ("audit", "view"),
]


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def upgrade() -> None:
    for role in ROLES:
        op.execute(f"INSERT INTO roles (id, name) VALUES (gen_random_uuid(), {sql_string(role)}) ON CONFLICT (name) DO NOTHING")
    for department in DEPARTMENTS:
        op.execute(f"INSERT INTO departments (id, name) VALUES (gen_random_uuid(), {sql_string(department)}) ON CONFLICT (name) DO NOTHING")
    for resource, action in PERMISSIONS:
        op.execute(f"INSERT INTO permissions (id, resource, action) VALUES (gen_random_uuid(), {sql_string(resource)}, {sql_string(action)}) ON CONFLICT (resource, action) DO NOTHING")
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r CROSS JOIN permissions p
        WHERE r.name = 'Administrador'
        ON CONFLICT DO NOTHING
    """)
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource = 'documents' AND p.action IN ('view', 'create', 'download')
        WHERE r.name = 'Cliente'
        ON CONFLICT DO NOTHING
    """)
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource IN ('companies', 'documents', 'tickets') AND p.action IN ('view', 'create', 'download', 'respond')
        WHERE r.name IN ('Contador', 'Fiscal', 'Departamento Pessoal', 'Atendimento')
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    op.execute("DELETE FROM role_permissions")
    op.execute("DELETE FROM permissions")
    op.execute("DELETE FROM departments")
    op.execute("DELETE FROM roles")
