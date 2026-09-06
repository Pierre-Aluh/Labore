from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parents[1]))

from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.main import app


client = TestClient(app)


def test_websocket_without_token_is_rejected() -> None:
    try:
        with client.websocket_connect(f"/api/v1/ws/tickets/{uuid4()}"):
            pass
    except WebSocketDisconnect as error:
        assert error.code == 4401
