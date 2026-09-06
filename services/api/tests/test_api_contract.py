from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_has_no_auth_requirement() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_protected_me_endpoint_requires_authentication() -> None:
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
