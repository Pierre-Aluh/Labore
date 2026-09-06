from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models import AuditLog, BankAccount, CompanyUser, CompetencyRequirement, Document, User
from app.rbac import require_permission

router = APIRouter(prefix="/api/v1", tags=["statements-and-investments"])


class BankAccountCreate(BaseModel):
    company_id: UUID
    institution_name: str = Field(min_length=2, max_length=160)
    masked_identifier: str = Field(min_length=2, max_length=80)


class BankAccountResponse(BaseModel):
    id: UUID
    company_id: UUID
    institution_name: str
    masked_identifier: str
    status: str


class InvestmentRequirementCreate(BaseModel):
    competency_id: UUID
    requirement_key: str = "INVESTIMENTOS"


class RequirementResponse(BaseModel):
    id: UUID
    competency_id: UUID
    requirement_key: str
    status: str
    is_required: bool


def ensure_company_access(session: Session, user: User, company_id: UUID) -> None:
    if session.scalar(select(CompanyUser).where(CompanyUser.company_id == company_id, CompanyUser.user_id == user.id)) is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company access denied")


@router.post("/bank-accounts", response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
def create_bank_account(
    payload: BankAccountCreate,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("bank_accounts", "create")),
) -> BankAccount:
    ensure_company_access(session, user, payload.company_id)
    if session.scalar(select(BankAccount).where(BankAccount.company_id == payload.company_id, BankAccount.masked_identifier == payload.masked_identifier)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bank account already exists")
    account = BankAccount(**payload.model_dump())
    session.add(account)
    session.flush()
    session.add(AuditLog(actor_user_id=user.id, company_id=account.company_id, action="bank_account_created", target_type="bank_account", target_id=account.id, outcome="success", metadata_json={}))
    session.commit()
    session.refresh(account)
    return account


@router.get("/companies/{company_id}/bank-accounts", response_model=list[BankAccountResponse])
def list_bank_accounts(
    company_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BankAccount]:
    ensure_company_access(session, user, company_id)
    return list(session.scalars(select(BankAccount).where(BankAccount.company_id == company_id).order_by(BankAccount.institution_name)).all())


@router.post("/bank-accounts/{account_id}/statements/{document_id}", response_model=BankAccountResponse)
def link_statement(
    account_id: UUID,
    document_id: UUID,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("bank_accounts", "update")),
) -> BankAccount:
    account = session.get(BankAccount, account_id)
    document = session.get(Document, document_id)
    if account is None or document is None or document.company_id != account.company_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account or document not found")
    ensure_company_access(session, user, account.company_id)
    document.bank_account_id = account.id
    session.add(AuditLog(actor_user_id=user.id, company_id=account.company_id, action="statement_linked", target_type="document", target_id=document.id, outcome="success", metadata_json={"bank_account_id": str(account.id)}))
    session.commit()
    session.refresh(account)
    return account


@router.post("/investment-requirements", response_model=RequirementResponse, status_code=status.HTTP_201_CREATED)
def create_investment_requirement(
    payload: InvestmentRequirementCreate,
    session: Session = Depends(get_db),
    user: User = Depends(require_permission("documents", "create")),
) -> CompetencyRequirement:
    competency = session.execute(select(CompetencyRequirement).where(CompetencyRequirement.competency_id == payload.competency_id)).scalars().first()
    if competency is not None and competency.requirement_key == payload.requirement_key:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Requirement already exists")
    requirement = CompetencyRequirement(competency_id=payload.competency_id, requirement_key=payload.requirement_key, status="pending", is_required=True)
    session.add(requirement)
    session.commit()
    session.refresh(requirement)
    return requirement
