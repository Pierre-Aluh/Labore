from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import Company, CompanyUser, Document, Ticket, User
from app.rbac import require_permission

router = APIRouter(prefix="/api/v1/workspace", tags=["office-workspace"])


class WorkspaceSummary(BaseModel):
    company_count: int
    document_count: int
    open_ticket_count: int


class CompanySummary(BaseModel):
    id: UUID
    legal_name: str
    trade_name: str | None
    tax_identifier: str
    status: str


class DocumentSummary(BaseModel):
    id: UUID
    company_id: UUID
    original_filename: str
    status: str
    file_size_bytes: int


class TicketSummary(BaseModel):
    id: UUID
    company_id: UUID
    subject: str
    status: str


def linked_company_ids(session: Session, user: User):
    return select(CompanyUser.company_id).where(CompanyUser.user_id == user.id)


@router.get("/summary", response_model=WorkspaceSummary)
def workspace_summary(
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("companies", "view")),
) -> WorkspaceSummary:
    company_ids = linked_company_ids(session, user)
    company_count = session.scalar(select(func.count()).select_from(Company).where(Company.id.in_(company_ids))) or 0
    document_count = session.scalar(select(func.count()).select_from(Document).where(Document.company_id.in_(company_ids))) or 0
    open_ticket_count = session.scalar(select(func.count()).select_from(Ticket).where(Ticket.company_id.in_(company_ids), Ticket.status != "closed")) or 0
    return WorkspaceSummary(company_count=company_count, document_count=document_count, open_ticket_count=open_ticket_count)


@router.get("/companies", response_model=list[CompanySummary])
def workspace_companies(
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("companies", "view")),
) -> list[Company]:
    return list(session.scalars(select(Company).where(Company.id.in_(linked_company_ids(session, user))).order_by(Company.legal_name)).all())


@router.get("/documents", response_model=list[DocumentSummary])
def workspace_documents(
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "view")),
) -> list[Document]:
    return list(session.scalars(select(Document).where(Document.company_id.in_(linked_company_ids(session, user))).order_by(Document.created_at.desc())).all())


@router.get("/tickets", response_model=list[TicketSummary])
def workspace_tickets(
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("tickets", "view")),
) -> list[Ticket]:
    return list(session.scalars(select(Ticket).where(Ticket.company_id.in_(linked_company_ids(session, user))).order_by(Ticket.updated_at.desc())).all())
