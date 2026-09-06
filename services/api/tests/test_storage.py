from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pytest

from app.storage import normalize_filename, persist_quarantined, storage_path, validate_extension


def test_filename_is_sanitized_and_extension_is_checked() -> None:
    assert normalize_filename("../relatorio com acentuação.pdf") == "relatorio_com_acentuacao.pdf"
    assert validate_extension("documento.PDF") == ".pdf"
    with pytest.raises(ValueError):
        validate_extension("malware.exe")


def test_upload_is_atomic_and_hashed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.storage.get_settings", lambda: type("Settings", (), {"storage_root": str(tmp_path), "max_upload_size_bytes": 100})())
    destination = storage_path(uuid4(), uuid4(), "MOVIMENTACAO_CONTABIL", uuid4(), "arquivo.txt")
    size, checksum = persist_quarantined(BytesIO(b"synthetic-content"), destination)
    assert size == len(b"synthetic-content")
    assert len(checksum) == 64
    assert destination.read_bytes() == b"synthetic-content"


def test_upload_size_limit_removes_temporary_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.storage.get_settings", lambda: type("Settings", (), {"storage_root": str(tmp_path), "max_upload_size_bytes": 3})())
    destination = storage_path(uuid4(), uuid4(), "EXTRATOS", uuid4(), "extrato.txt")
    with pytest.raises(ValueError):
        persist_quarantined(BytesIO(b"too-large"), destination)
    assert not destination.exists()
    assert not list(tmp_path.rglob(".upload-*"))
