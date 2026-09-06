from app.chat_api import ConnectionManager


def test_connection_manager_starts_empty() -> None:
    manager = ConnectionManager()
    assert manager.connections == {}
