"""Seed the initial document categories."""

from alembic import op

revision = "0003_document_categories"
down_revision = "0002_seed_rbac"
branch_labels = None
depends_on = None

CATEGORIES = [
    ("MOVIMENTACAO_CONTABIL", "Movimentação Contábil"),
    ("EXTRATOS", "Extratos Bancários"),
    ("INVESTIMENTOS", "Investimentos"),
    ("DOCUMENTOS_CONTABILIDADE", "Documentos da Contabilidade"),
    ("CHAMADOS", "Anexos de Chamados"),
]


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def upgrade() -> None:
    for code, name in CATEGORIES:
        op.execute(f"INSERT INTO document_categories (id, code, name) VALUES (gen_random_uuid(), {sql_string(code)}, {sql_string(name)}) ON CONFLICT (code) DO NOTHING")


def downgrade() -> None:
    op.execute("DELETE FROM document_categories WHERE code IN ('MOVIMENTACAO_CONTABIL', 'EXTRATOS', 'INVESTIMENTOS', 'DOCUMENTOS_CONTABILIDADE', 'CHAMADOS')")
