from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.bank_api import BankAccountCreate, InvestmentRequirementCreate


def test_bank_account_payload_keeps_identifier_masked() -> None:
    payload = BankAccountCreate(company_id=uuid4(), institution_name="Banco Sintético", masked_identifier="****1234")
    assert payload.masked_identifier.startswith("****")


def test_investment_requirement_defaults_to_expected_category() -> None:
    payload = InvestmentRequirementCreate(competency_id=uuid4())
    assert payload.requirement_key == "INVESTIMENTOS"
