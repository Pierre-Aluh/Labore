from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_messages_require_authentication() -> None:
    response = client.get("/api/v1/notifications")
    assert response.status_code == 401
