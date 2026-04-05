from fastapi import FastAPI

from helpdesk_hub_api.api.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="HelpDesk Hub API",
        version="0.1.0",
        description="Backend API for internal helpdesk ticket management.",
    )
    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
