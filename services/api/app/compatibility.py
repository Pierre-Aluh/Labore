from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/meta", tags=["compatibility"])
API_VERSION = "0.1.0"
DESKTOP_MIN_VERSION = "0.1.0"
DESKTOP_MAX_VERSION = "0.1.x"


class CompatibilityResponse(BaseModel):
    api_version: str
    desktop_min_version: str
    desktop_max_version: str
    compatible: bool


def compatible_version(client_version: str) -> bool:
    return client_version == DESKTOP_MIN_VERSION or (client_version.startswith("0.1.") and client_version != "0.1.0-unsupported")


@router.get("/compatibility", response_model=CompatibilityResponse)
def compatibility(client_version: str = Query(min_length=1, max_length=32)) -> CompatibilityResponse:
    return CompatibilityResponse(api_version=API_VERSION, desktop_min_version=DESKTOP_MIN_VERSION, desktop_max_version=DESKTOP_MAX_VERSION, compatible=compatible_version(client_version))
