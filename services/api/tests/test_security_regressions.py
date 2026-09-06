from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pytest

from app.storage import persist_quarantined, storage_path


def test_storage_path_cannot_escape_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.storage.get_settings", lambda: type("Settings", (), {"storage_root": str(tmp_path), "max_upload_size_bytes": 100})())
    destination = storage_path(uuid4(), uuid4(), "../../outside", uuid4(), "safe.txt")
    assert tmp_path in destination.parents


def test_size_limit_rejects_large_synthetic_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.storage.get_settings", lambda: type("Settings", (), {"storage_root": str(tmp_path), "max_upload_size_bytes": 2})())
    with pytest.raises(ValueError):
        persist_quarantined(BytesIO(b"123"), tmp_path / "file.txt")
