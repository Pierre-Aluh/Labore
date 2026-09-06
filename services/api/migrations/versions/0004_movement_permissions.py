"""Add movement permissions to the RBAC catalog."""

from alembic import op

revision = "0004_movement_permissions"
down_revision = "0003_document_categories"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("INSERT INTO permissions (id, resource, action) VALUES (gen_random_uuid(), 'movements', 'view'), (gen_random_uuid(), 'movements', 'create'), (gen_random_uuid(), 'movements', 'complete') ON CONFLICT (resource, action) DO NOTHING")
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource = 'movements' AND p.action IN ('view', 'create')
        WHERE r.name = 'Cliente'
        ON CONFLICT DO NOTHING
    """)
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource = 'movements'
        WHERE r.name IN ('Administrador', 'Contador', 'Fiscal')
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    op.execute("DELETE FROM role_permissions WHERE permission_id IN (SELECT id FROM permissions WHERE resource = 'movements')")
    op.execute("DELETE FROM permissions WHERE resource = 'movements'")
