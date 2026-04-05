from fastapi import FastAPI

from helpdesk_hub_api.schemas.system import HealthResponse, RootResponse


app = FastAPI(
    title="HelpDesk Hub API",
    version="0.1.0",
    description="Backend API for internal helpdesk ticket management.",
)


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return RootResponse(
        name="HelpDesk Hub API",
        status="ok",
        docs="/docs",
    )


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
