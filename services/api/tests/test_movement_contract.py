from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_movement_creation_requires_authentication() -> None:
    response = client.post("/api/v1/movements", json={})
    assert response.status_code == 401
