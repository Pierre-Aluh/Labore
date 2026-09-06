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


def upgrade() -> None:
    for role in ROLES:
        op.execute("INSERT INTO roles (id, name) VALUES (gen_random_uuid(), :name) ON CONFLICT (name) DO NOTHING", {"name": role})
    for department in DEPARTMENTS:
        op.execute("INSERT INTO departments (id, name) VALUES (gen_random_uuid(), :name) ON CONFLICT (name) DO NOTHING", {"name": department})
    for resource, action in PERMISSIONS:
        op.execute("INSERT INTO permissions (id, resource, action) VALUES (gen_random_uuid(), :resource, :action) ON CONFLICT (resource, action) DO NOTHING", {"resource": resource, "action": action})
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
