"""Add ticket lifecycle permissions."""

from alembic import op

revision = "0006_ticket_permissions"
down_revision = "0005_bank_accounts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("INSERT INTO permissions (id, resource, action) VALUES (gen_random_uuid(), 'tickets', 'assign'), (gen_random_uuid(), 'tickets', 'close'), (gen_random_uuid(), 'tickets', 'reopen') ON CONFLICT (resource, action) DO NOTHING")
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource = 'tickets'
        WHERE r.name IN ('Administrador', 'Atendimento', 'Contador', 'Fiscal')
        ON CONFLICT DO NOTHING
    """)
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource = 'tickets' AND p.action IN ('create', 'view', 'respond', 'close')
        WHERE r.name = 'Cliente'
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    op.execute("DELETE FROM role_permissions WHERE permission_id IN (SELECT id FROM permissions WHERE resource = 'tickets' AND action IN ('assign', 'close', 'reopen'))")
    op.execute("DELETE FROM permissions WHERE resource = 'tickets' AND action IN ('assign', 'close', 'reopen')")
