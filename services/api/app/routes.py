from fastapi import APIRouter

from app.admin_api import router as admin_router
from app.document_api import router as document_router
from app.bank_api import router as bank_router
from app.movement_api import router as movement_router
from app.ticket_api import router as ticket_router

router = APIRouter()
router.include_router(admin_router)
router.include_router(document_router)
router.include_router(movement_router)
router.include_router(bank_router)
router.include_router(ticket_router)
