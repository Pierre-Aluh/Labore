from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.chat_api import MessageCreate


def test_message_rejects_empty_body() -> None:
    try:
        MessageCreate(body="")
    except ValueError:
        return
    raise AssertionError("empty messages must be rejected")


def test_message_accepts_synthetic_body() -> None:
    message = MessageCreate(body="Mensagem de teste sintética")
    assert message.body.startswith("Mensagem")
    assert uuid4() is not None
