from fastapi import APIRouter

from api.schemas.system import HealthResponse, RootResponse

router = APIRouter()


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(
        name="HelpDesk Hub API",
        status="ok",
        docs="/docs",
    )


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
