import hashlib
import os
import re
import shutil
import tempfile
import unicodedata
from pathlib import Path
from typing import BinaryIO
from uuid import UUID

from app.core.config import get_settings

ALLOWED_EXTENSIONS = {".pdf", ".xml", ".xlsx", ".xls", ".csv", ".ofx", ".txt", ".jpg", ".jpeg", ".png", ".zip"}


def normalize_filename(filename: str) -> str:
    base_name = Path(filename).name
    normalized = unicodedata.normalize("NFKD", base_name).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "_", normalized).strip("._")
    return normalized[:255] or "file"


def validate_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("File type is not allowed")
    return extension


def storage_path(company_id: UUID, competency_id: UUID, category: str, document_id: UUID, filename: str) -> Path:
    safe_category = re.sub(r"[^A-Za-z0-9_-]+", "_", category).strip("_") or "uncategorized"
    safe_name = normalize_filename(filename)
    relative = Path(str(company_id)) / str(competency_id) / safe_category / f"{document_id}_{safe_name}"
    root = Path(get_settings().storage_root).resolve()
    result = (root / relative).resolve()
    if root not in result.parents:
        raise ValueError("Invalid storage path")
    return result


def persist_quarantined(source: BinaryIO, destination: Path, max_size: int | None = None) -> tuple[int, str]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    digest = hashlib.sha256()
    total_size = 0
    limit = max_size or get_settings().max_upload_size_bytes
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".upload-", delete=False) as temporary:
            temp_path = Path(temporary.name)
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > limit:
                    raise ValueError("File exceeds configured size limit")
                digest.update(chunk)
                temporary.write(chunk)
        os.replace(temp_path, destination)
        temp_path = None
        return total_size, digest.hexdigest()
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def remove_file(path: Path) -> None:
    path.unlink(missing_ok=True)


def restore_or_remove(path: Path, destination: Path) -> None:
    if path.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), str(destination))
