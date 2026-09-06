from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_compatibility_endpoint_is_public_metadata_only() -> None:
    response = client.get("/api/v1/meta/compatibility?client_version=0.1.0")
    assert response.status_code == 200
    assert response.json()["compatible"] is True
