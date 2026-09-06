from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_collaborator_workspace_requires_authentication() -> None:
    response = client.get("/api/v1/workspace/summary")
    assert response.status_code == 401


def test_workspace_routes_are_registered() -> None:
    paths = set(app.openapi()["paths"])
    assert "/api/v1/workspace/companies" in paths
    assert "/api/v1/workspace/documents" in paths
    assert "/api/v1/workspace/tickets" in paths