"""Add bank account document linkage and permissions."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0005_bank_accounts"
down_revision = "0004_movement_permissions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("bank_account_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key("fk_documents_bank_account", "documents", "bank_accounts", ["bank_account_id"], ["id"], ondelete="SET NULL")
    op.execute("INSERT INTO permissions (id, resource, action) VALUES (gen_random_uuid(), 'bank_accounts', 'view'), (gen_random_uuid(), 'bank_accounts', 'create'), (gen_random_uuid(), 'bank_accounts', 'update') ON CONFLICT (resource, action) DO NOTHING")
    op.execute("""
        INSERT INTO role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.resource = 'bank_accounts'
        WHERE r.name IN ('Administrador', 'Contador', 'Fiscal', 'Cliente')
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    op.execute("DELETE FROM role_permissions WHERE permission_id IN (SELECT id FROM permissions WHERE resource = 'bank_accounts')")
    op.execute("DELETE FROM permissions WHERE resource = 'bank_accounts'")
    op.drop_constraint("fk_documents_bank_account", "documents", type_="foreignkey")
    op.drop_column("documents", "bank_account_id")
