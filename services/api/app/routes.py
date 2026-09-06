from fastapi import APIRouter

from app.admin_api import router as admin_router
from app.document_api import router as document_router

router = APIRouter()
router.include_router(admin_router)
router.include_router(document_router)
