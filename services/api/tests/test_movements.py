from pathlib import Path
import sys
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from pydantic import ValidationError

from app.movement_api import MovementCreate, MovementDocumentLink, REQUIRED_DOCUMENT_TYPES


def test_movement_requires_only_known_document_types() -> None:
    payload = MovementCreate(company_id=uuid4(), competency_id=uuid4(), documents=[MovementDocumentLink(document_id=uuid4(), document_type="documento")])
    assert payload.documents[0].document_type == "documento"
    assert REQUIRED_DOCUMENT_TYPES == {"DOCUMENTO", "COBRANCA", "COMPROVANTE"}


def test_movement_document_link_requires_uuid() -> None:
    with pytest.raises(ValidationError):
        MovementDocumentLink(document_id="not-a-uuid", document_type="DOCUMENTO")
