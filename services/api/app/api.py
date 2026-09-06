from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import authenticate_user, revoke_session
from app.db import get_db
from app.dependencies import get_current_user
from app.models import SessionRecord, User
from app.security import hash_session_token

router = APIRouter(prefix="/api/v1")
bearer = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime
    user_id: str


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str


@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, session: Session = Depends(get_db)) -> LoginResponse:
    result = authenticate_user(session, payload.email, payload.password)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user, token = result
    session_record = session.scalar(select(SessionRecord).where(SessionRecord.token_hash == hash_session_token(token)))
    assert session_record is not None
    return LoginResponse(access_token=token, expires_at=session_record.expires_at, user_id=str(user.id))


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    session: Session = Depends(get_db),
) -> None:
    if credentials is not None:
        revoke_session(session, credentials.credentials)


@router.get("/auth/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(id=str(user.id), email=user.email, display_name=user.display_name)
