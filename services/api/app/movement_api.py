from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import AccountingMovement, CompanyUser, Document, MovementDocument, User
from app.rbac import require_permission

router = APIRouter(prefix="/api/v1/movements", tags=["accounting-movements"])
REQUIRED_DOCUMENT_TYPES = {"DOCUMENTO", "COBRANCA", "COMPROVANTE"}


class MovementDocumentLink(BaseModel):
    document_id: UUID
    document_type: str


class MovementCreate(BaseModel):
    company_id: UUID
    competency_id: UUID
    note: str | None = None
    documents: list[MovementDocumentLink] = Field(default_factory=list)


class MovementResponse(BaseModel):
    id: UUID
    status: str
    missing_document_types: list[str]


def missing_types(session: Session, movement_id: UUID) -> list[str]:
    links = session.scalars(select(MovementDocument.document_type).where(MovementDocument.movement_id == movement_id)).all()
    return sorted(REQUIRED_DOCUMENT_TYPES - set(links))


def ensure_company_access(session: Session, user: User, company_id: UUID) -> None:
    if session.scalar(select(CompanyUser).where(CompanyUser.company_id == company_id, CompanyUser.user_id == user.id)) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company access denied")


@router.post("", response_model=MovementResponse, status_code=status.HTTP_201_CREATED)
def create_movement(
    payload: MovementCreate,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "create")),
) -> MovementResponse:
    ensure_company_access(session, user, payload.company_id)
    types = [link.document_type.upper() for link in payload.documents]
    if len(types) != len(set(types)) or not set(types).issubset(REQUIRED_DOCUMENT_TYPES):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or duplicated document types")
    document_ids = [link.document_id for link in payload.documents]
    documents = list(session.scalars(select(Document).where(Document.id.in_(document_ids), Document.company_id == payload.company_id)).all())
    if len(documents) != len(set(document_ids)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document does not belong to company")
    movement = AccountingMovement(company_id=payload.company_id, competency_id=payload.competency_id, note=payload.note, status="incomplete")
    session.add(movement)
    session.flush()
    for link in payload.documents:
        session.add(MovementDocument(movement_id=movement.id, document_id=link.document_id, document_type=link.document_type.upper()))
    session.flush()
    missing = missing_types(session, movement.id)
    movement.status = "received" if not missing else "incomplete"
    session.commit()
    return MovementResponse(id=movement.id, status=movement.status, missing_document_types=missing)


@router.get("/{movement_id}", response_model=MovementResponse)
def get_movement(
    movement_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MovementResponse:
    movement = session.get(AccountingMovement, movement_id)
    if movement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
    ensure_company_access(session, user, movement.company_id)
    return MovementResponse(id=movement.id, status=movement.status, missing_document_types=missing_types(session, movement.id))


@router.post("/{movement_id}/complete", response_model=MovementResponse)
def complete_movement(
    movement_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "update")),
) -> MovementResponse:
    movement = session.get(AccountingMovement, movement_id)
    if movement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement not found")
    ensure_company_access(session, user, movement.company_id)
    missing = missing_types(session, movement.id)
    if missing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"missing_document_types": missing})
    movement.status = "received"
    session.commit()
    return MovementResponse(id=movement.id, status=movement.status, missing_document_types=[])
