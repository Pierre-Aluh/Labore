from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.admin_api import CompanyCreate, DepartmentCreate, UserCreate
from app.models import RecordStatus


def test_admin_payloads_validate_synthetic_values() -> None:
    company = CompanyCreate(legal_name="Empresa Sintética", tax_identifier="SYNTH-001")
    department = DepartmentCreate(name="Departamento Sintético")
    user = UserCreate(email="synthetic@example.invalid", display_name="Usuário Sintético", password="synthetic-password-12", role_name="Cliente")
    assert company.tax_identifier == "SYNTH-001"
    assert department.name.startswith("Departamento")
    assert user.role_name == "Cliente"
    assert RecordStatus.ACTIVE.value == "active"


def test_rbac_seed_is_idempotent_and_contains_initial_roles() -> None:
    migration = (Path(__file__).parents[1] / "migrations" / "versions" / "0002_seed_rbac.py").read_text(encoding="utf-8")
    assert "ON CONFLICT" in migration
    assert "Administrador" in migration
    assert "Cliente" in migration
