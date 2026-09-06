from collections.abc import Callable
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import Permission, RolePermission, User, UserRole


@lru_cache
def permission_dependency(resource: str, action: str) -> Callable:
    def dependency(user: User = Depends(get_current_user), session: Session = Depends(get_db)) -> User:
        allowed = session.scalar(
            select(exists().where(
                UserRole.user_id == user.id,
                UserRole.role_id == RolePermission.role_id,
                RolePermission.permission_id == Permission.id,
                Permission.resource == resource,
                Permission.action == action,
            ))
        )
        if not allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user

    return dependency


def require_permission(resource: str, action: str) -> Callable:
    return permission_dependency(resource, action)
