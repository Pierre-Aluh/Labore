from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import AuditLog, Company, CompanyUser, Department, Role, User, UserRole
from app.rbac import require_permission
from app.security import hash_password

router = APIRouter(prefix="/api/v1/admin", tags=["administration"])


class CompanyCreate(BaseModel):
    legal_name: str = Field(min_length=2, max_length=240)
    trade_name: str | None = Field(default=None, max_length=240)
    tax_identifier: str = Field(min_length=3, max_length=32)


class CompanyResponse(BaseModel):
    id: UUID
    legal_name: str
    trade_name: str | None
    tax_identifier: str
    status: str


class UserCreate(BaseModel):
    email: str
    display_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=12)
    role_name: str
    company_ids: list[UUID] = []


class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: str
    status: str


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class DepartmentResponse(BaseModel):
    id: UUID
    name: str
    status: str


class AuditResponse(BaseModel):
    id: UUID
    action: str
    target_type: str
    outcome: str
    created_at: str


@router.get("/users", response_model=list[UserResponse])
def list_users(
    session: Session = Depends(get_db),
    _: User = Depends(require_permission("users", "view")),
) -> list[User]:
    return list(session.scalars(select(User).order_by(User.display_name)).all())


@router.get("/audit", response_model=list[AuditResponse])
def list_audit(
    session: Session = Depends(get_db),
    _: User = Depends(require_permission("audit", "view")),
) -> list[AuditLog]:
    return list(session.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(100)).all())


@router.post("/companies", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    session: Session = Depends(get_db),
    actor: User = Depends(require_permission("companies", "create")),
) -> Company:
    if session.scalar(select(Company).where(Company.tax_identifier == payload.tax_identifier)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
    company = Company(**payload.model_dump())
    session.add(company)
    session.flush()
    session.add(CompanyUser(company_id=company.id, user_id=actor.id))
    session.add(AuditLog(actor_user_id=actor.id, company_id=company.id, action="company_created", target_type="company", target_id=company.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(company)
    return company


@router.get("/companies", response_model=list[CompanyResponse])
def list_companies(
    session: Session = Depends(get_db),
    _: User = Depends(require_permission("companies", "view")),
) -> list[Company]:
    return list(session.scalars(select(Company).order_by(Company.legal_name)).all())


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    session: Session = Depends(get_db),
    actor: User = Depends(require_permission("users", "create")),
) -> User:
    if session.scalar(select(User).where(User.email == payload.email.lower().strip())):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    role = session.scalar(select(Role).where(Role.name == payload.role_name))
    if role is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown role")
    companies = list(session.scalars(select(Company).where(Company.id.in_(payload.company_ids))).all())
    if len(companies) != len(set(payload.company_ids)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown company")
    user = User(email=payload.email.lower().strip(), display_name=payload.display_name, password_hash=hash_password(payload.password))
    session.add(user)
    session.flush()
    session.add(UserRole(user_id=user.id, role_id=role.id))
    for company in companies:
        session.add(CompanyUser(company_id=company.id, user_id=user.id))
    session.add(AuditLog(actor_user_id=actor.id, action="user_created", target_type="user", target_id=user.id, outcome="success", metadata_json={"role": role.name}))
    session.commit()
    session.refresh(user)
    return user


@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    session: Session = Depends(get_db),
    actor: User = Depends(require_permission("departments", "create")),
) -> Department:
    if session.scalar(select(Department).where(Department.name == payload.name)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Department already exists")
    department = Department(name=payload.name)
    session.add(department)
    session.flush()
    session.add(AuditLog(actor_user_id=actor.id, action="department_created", target_type="department", target_id=department.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(department)
    return department


@router.get("/roles", response_model=list[str])
def list_roles(
    session: Session = Depends(get_db),
    _: User = Depends(require_permission("roles", "view")),
) -> list[str]:
    return list(session.scalars(select(Role.name).order_by(Role.name)).all())
