from collections import defaultdict
from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_session_token
from app.db import SessionLocal, get_db
from app.dependencies import get_current_user
from app.models import AuditLog, Notification, SessionRecord, Ticket, TicketMessage, TicketParticipant, User
from app.rbac import require_permission

router = APIRouter(prefix="/api/v1", tags=["chat-and-notifications"])


class MessageCreate(BaseModel):
    body: str = Field(min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    id: UUID
    ticket_id: UUID
    author_user_id: UUID
    body: str


class NotificationResponse(BaseModel):
    id: UUID
    event_type: str
    title: str
    body: str
    is_read: bool


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[UUID, set[WebSocket]] = defaultdict(set)

    async def connect(self, ticket_id: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[ticket_id].add(websocket)

    def disconnect(self, ticket_id: UUID, websocket: WebSocket) -> None:
        self.connections[ticket_id].discard(websocket)
        if not self.connections[ticket_id]:
            del self.connections[ticket_id]

    async def broadcast(self, ticket_id: UUID, payload: dict[str, str]) -> None:
        stale: list[WebSocket] = []
        for connection in self.connections[ticket_id]:
            try:
                await connection.send_json(payload)
            except Exception:
                stale.append(connection)
        for connection in stale:
            self.disconnect(ticket_id, connection)


manager = ConnectionManager()


def get_participant(session: Session, ticket_id: UUID, user_id: UUID) -> TicketParticipant | None:
    return session.scalar(select(TicketParticipant).where(TicketParticipant.ticket_id == ticket_id, TicketParticipant.user_id == user_id))


def get_ticket(session: Session, ticket_id: UUID) -> Ticket:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    return ticket


@router.post("/tickets/{ticket_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    ticket_id: UUID,
    payload: MessageCreate,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("tickets", "respond")),
) -> TicketMessage:
    ticket = get_ticket(session, ticket_id)
    if get_participant(session, ticket.id, user.id) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a ticket participant")
    message = TicketMessage(ticket_id=ticket.id, author_user_id=user.id, body=payload.body)
    session.add(message)
    session.flush()
    participants = session.scalars(select(TicketParticipant).where(TicketParticipant.ticket_id == ticket.id, TicketParticipant.user_id != user.id)).all()
    for participant in participants:
        session.add(Notification(user_id=participant.user_id, event_type="ticket_replied", title="Nova resposta no chamado", body=ticket.subject))
    session.add(AuditLog(actor_user_id=user.id, company_id=ticket.company_id, action="ticket_replied", target_type="ticket_message", target_id=message.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(message)
    return message


@router.get("/tickets/{ticket_id}/messages", response_model=list[MessageResponse])
def list_messages(
    ticket_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[TicketMessage]:
    ticket = get_ticket(session, ticket_id)
    if get_participant(session, ticket.id, user.id) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a ticket participant")
    return list(session.scalars(select(TicketMessage).where(TicketMessage.ticket_id == ticket.id).order_by(TicketMessage.created_at)).all())


@router.get("/notifications", response_model=list[NotificationResponse])
def list_notifications(session: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[Notification]:
    return list(session.scalars(select(Notification).where(Notification.user_id == user.id).order_by(Notification.created_at.desc())).all())


@router.post("/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(notification_id: UUID, session: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Notification:
    notification = session.get(Notification, notification_id)
    if notification is None or notification.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    notification.is_read = True
    session.commit()
    session.refresh(notification)
    return notification


async def authenticate_websocket(token: str, ticket_id: UUID, session: Session) -> User | None:
    record = session.scalar(select(SessionRecord).where(SessionRecord.token_hash == hash_session_token(token)))
    if record is None or record.revoked_at is not None or record.expires_at <= datetime.now(UTC):
        return None
    user = session.get(User, record.user_id)
    if user is None or get_participant(session, ticket_id, user.id) is None:
        return None
    return user


@router.websocket("/ws/tickets/{ticket_id}")
async def ticket_websocket(websocket: WebSocket, ticket_id: UUID, token: str | None = None) -> None:
    session = SessionLocal()
    user = None if token is None else await authenticate_websocket(token, ticket_id, session)
    if user is None:
        await websocket.close(code=4401)
        session.close()
        return
    await manager.connect(ticket_id, websocket)
    try:
        while True:
            payload = await websocket.receive_json()
            body = MessageCreate.model_validate(payload)
            message = TicketMessage(ticket_id=ticket_id, author_user_id=user.id, body=body.body)
            session.add(message)
            ticket = session.get(Ticket, ticket_id)
            if ticket is None:
                break
            participants = session.scalars(select(TicketParticipant).where(TicketParticipant.ticket_id == ticket_id, TicketParticipant.user_id != user.id)).all()
            for participant in participants:
                session.add(Notification(user_id=participant.user_id, event_type="ticket_replied", title="Nova resposta no chamado", body=ticket.subject))
            session.add(AuditLog(actor_user_id=user.id, company_id=ticket.company_id, action="ticket_replied", target_type="ticket_message", target_id=message.id, outcome="success", metadata_json={"transport": "websocket"}))
            session.commit()
            await manager.broadcast(ticket_id, {"event": "message", "body": body.body, "message_id": str(message.id)})
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(ticket_id, websocket)
        session.close()
