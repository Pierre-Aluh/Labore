from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_bank_account_endpoint_requires_authentication() -> None:
    response = client.get("/api/v1/companies/00000000-0000-0000-0000-000000000000/bank-accounts")
    assert response.status_code == 401
