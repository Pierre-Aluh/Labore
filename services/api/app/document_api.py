from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import AuditLog, CompanyUser, Competency, Document, DocumentCategory, User
from app.rbac import require_permission
from app.storage import persist_quarantined, storage_path, validate_extension

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    id: UUID
    original_filename: str
    status: str
    file_size_bytes: int
    checksum_hash: str


class CompetencyResponse(BaseModel):
    id: UUID
    year: int
    month: int
    status: str


class CategoryResponse(BaseModel):
    id: UUID
    code: str
    name: str


def ensure_company_access(session: Session, user: User, company_id: UUID) -> None:
    if session.scalar(select(CompanyUser).where(CompanyUser.company_id == company_id, CompanyUser.user_id == user.id)) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company access denied")


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(
    session: Session = Depends(get_db),
    _: User = Depends(require_permission("documents", "view")),
) -> list[DocumentCategory]:
    return list(session.scalars(select(DocumentCategory).order_by(DocumentCategory.name)).all())


@router.get("/competencies", response_model=list[CompetencyResponse])
def list_competencies(
    company_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "view")),
) -> list[Competency]:
    ensure_company_access(session, user, company_id)
    return list(session.scalars(select(Competency).where(Competency.company_id == company_id).order_by(Competency.year.desc(), Competency.month.desc())).all())


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    company_id: UUID = Form(...),
    competency_id: UUID = Form(...),
    category_id: UUID = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "create")),
) -> Document:
    ensure_company_access(session, user, company_id)
    try:
        validate_extension(file.filename or "")
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(error)) from error
    category = session.get(DocumentCategory, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown document category")
    document_id = uuid4()
    destination = storage_path(company_id, competency_id, category.code, document_id, file.filename or "file")
    try:
        file_size, checksum = persist_quarantined(file.file, destination)
        document = Document(id=document_id, company_id=company_id, competency_id=competency_id, category_id=category_id, original_filename=file.filename or "file", normalized_filename=destination.name, logical_path=str(destination.relative_to(Path.cwd())), checksum_hash=checksum, file_size_bytes=file_size, mime_type=file.content_type or "application/octet-stream", uploaded_by_user_id=user.id)
        session.add(document)
        session.add(AuditLog(actor_user_id=user.id, company_id=company_id, action="document_uploaded", target_type="document", target_id=document_id, outcome="success", metadata_json={"status": "quarantined"}))
        session.commit()
        session.refresh(document)
        return document
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(error)) from error
    except Exception:
        destination.unlink(missing_ok=True)
        session.rollback()
        raise


@router.get("", response_model=list[DocumentResponse])
def list_documents(
    company_id: UUID | None = None,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "view")),
) -> list[Document]:
    statement = select(Document).where(Document.status == "available")
    if company_id is not None:
        ensure_company_access(session, user, company_id)
        statement = statement.where(Document.company_id == company_id)
    else:
        statement = statement.where(
            Document.company_id.in_(
                select(CompanyUser.company_id).where(CompanyUser.user_id == user.id)
            )
        )
    return list(session.scalars(statement.order_by(Document.created_at.desc())).all())


@router.get("/{document_id}/download")
def download_document(
    document_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "download")),
) -> FileResponse:
    document = session.get(Document, document_id)
    if document is None or document.status != "available":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document unavailable")
    ensure_company_access(session, user, document.company_id)
    path = Path(document.logical_path).resolve()
    if not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document file missing")
    session.add(AuditLog(actor_user_id=user.id, company_id=document.company_id, action="document_downloaded", target_type="document", target_id=document.id, outcome="success", metadata_json={}))
    session.commit()
    return FileResponse(path, filename=document.original_filename, media_type=document.mime_type)


@router.post("/{document_id}/approve", response_model=DocumentResponse)
def approve_document(
    document_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "update")),
) -> Document:
    document = session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    ensure_company_access(session, user, document.company_id)
    document.status = "available"
    session.add(AuditLog(actor_user_id=user.id, company_id=document.company_id, action="document_approved", target_type="document", target_id=document.id, outcome="success", metadata_json={"approved_at": datetime.now(UTC).isoformat()}))
    session.commit()
    session.refresh(document)
    return document
