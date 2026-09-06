from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import AuditLog, CompanyUser, Department, Ticket, TicketParticipant, User
from app.rbac import require_permission

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])


class TicketCreate(BaseModel):
    company_id: UUID
    subject: str = Field(min_length=3, max_length=240)
    description: str = Field(min_length=1)
    department_id: UUID | None = None


class TicketResponse(BaseModel):
    id: UUID
    company_id: UUID
    subject: str
    description: str
    status: str
    department_id: UUID | None


class ParticipantCreate(BaseModel):
    user_id: UUID


def ensure_company_access(session: Session, user: User, company_id: UUID) -> None:
    if session.scalar(select(CompanyUser).where(CompanyUser.company_id == company_id, CompanyUser.user_id == user.id)) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company access denied")


def get_ticket_or_404(session: Session, ticket_id: UUID) -> Ticket:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    payload: TicketCreate,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("tickets", "create")),
) -> Ticket:
    ensure_company_access(session, user, payload.company_id)
    if payload.department_id is not None and session.get(Department, payload.department_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown department")
    ticket = Ticket(**payload.model_dump(), requester_user_id=user.id)
    session.add(ticket)
    session.flush()
    session.add(TicketParticipant(ticket_id=ticket.id, user_id=user.id))
    session.add(AuditLog(actor_user_id=user.id, company_id=ticket.company_id, action="ticket_created", target_type="ticket", target_id=ticket.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(ticket)
    return ticket


@router.get("/companies/{company_id}", response_model=list[TicketResponse])
def list_tickets(
    company_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Ticket]:
    ensure_company_access(session, user, company_id)
    return list(session.scalars(select(Ticket).where(Ticket.company_id == company_id).order_by(Ticket.updated_at.desc())).all())


@router.post("/{ticket_id}/participants", status_code=status.HTTP_204_NO_CONTENT)
def add_participant(
    ticket_id: UUID,
    payload: ParticipantCreate,
    session: Session = Depends(get_db),
    actor: User = Depends(require_permission("tickets", "assign")),
) -> None:
    ticket = get_ticket_or_404(session, ticket_id)
    ensure_company_access(session, actor, ticket.company_id)
    participant = session.scalar(select(TicketParticipant).where(TicketParticipant.ticket_id == ticket.id, TicketParticipant.user_id == payload.user_id))
    if participant is None:
        if session.scalar(select(CompanyUser).where(CompanyUser.company_id == ticket.company_id, CompanyUser.user_id == payload.user_id)) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Participant is not linked to company")
        session.add(TicketParticipant(ticket_id=ticket.id, user_id=payload.user_id))
    session.add(AuditLog(actor_user_id=actor.id, company_id=ticket.company_id, action="ticket_assigned", target_type="ticket", target_id=ticket.id, outcome="success", metadata_json={"participant_id": str(payload.user_id)}))
    session.commit()


@router.post("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(
    ticket_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("tickets", "close")),
) -> Ticket:
    ticket = get_ticket_or_404(session, ticket_id)
    ensure_company_access(session, user, ticket.company_id)
    ticket.status = "closed"
    ticket.closed_at = datetime.now(UTC)
    session.add(AuditLog(actor_user_id=user.id, company_id=ticket.company_id, action="ticket_closed", target_type="ticket", target_id=ticket.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(ticket)
    return ticket


@router.post("/{ticket_id}/reopen", response_model=TicketResponse)
def reopen_ticket(
    ticket_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("tickets", "reopen")),
) -> Ticket:
    ticket = get_ticket_or_404(session, ticket_id)
    ensure_company_access(session, user, ticket.company_id)
    ticket.status = "reopened"
    ticket.closed_at = None
    session.add(AuditLog(actor_user_id=user.id, company_id=ticket.company_id, action="ticket_reopened", target_type="ticket", target_id=ticket.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(ticket)
    return ticket
