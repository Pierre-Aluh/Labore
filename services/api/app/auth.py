from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuditLog, SessionRecord, User
from app.security import create_session_token, hash_session_token, session_expiry, verify_password

MAX_FAILED_LOGINS = 5
LOCKOUT_MINUTES = 15


def authenticate_user(session: Session, email: str, password: str) -> tuple[User, str] | None:
    user = session.scalar(select(User).where(User.email == email.lower().strip()))
    now = datetime.now(UTC)
    if user is None or user.status != "active":
        return None
    if user.locked_until is not None and user.locked_until > now:
        return None
    if not verify_password(password, user.password_hash):
        user.failed_login_count += 1
        if user.failed_login_count >= MAX_FAILED_LOGINS:
            from datetime import timedelta

            user.locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
            user.failed_login_count = 0
        session.add(
            AuditLog(
                actor_user_id=user.id,
                action="login_failed",
                target_type="user",
                target_id=user.id,
                outcome="failure",
                metadata_json={},
            )
        )
        session.commit()
        return None
    user.failed_login_count = 0
    user.locked_until = None
    token = create_session_token()
    session.add(
        SessionRecord(
            user_id=user.id,
            token_hash=hash_session_token(token),
            expires_at=session_expiry(),
        )
    )
    session.add(
        AuditLog(
            actor_user_id=user.id,
            action="login_succeeded",
            target_type="user",
            target_id=user.id,
            outcome="success",
            metadata_json={},
        )
    )
    session.commit()
    session.refresh(user)
    return user, token


def revoke_session(session: Session, token: str) -> bool:
    record = session.scalar(select(SessionRecord).where(SessionRecord.token_hash == hash_session_token(token)))
    if record is None or record.revoked_at is not None:
        return False
    record.revoked_at = datetime.now(UTC)
    session.add(
        AuditLog(
            actor_user_id=record.user_id,
            action="logout",
            target_type="session",
            target_id=record.id,
            outcome="success",
            metadata_json={},
        )
    )
    session.commit()
    return True
