from fastapi import FastAPI

from api.routes.categories import router as categories_router
from api.routes.system import router as system_router
from api.routes.tickets import router as tickets_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="HelpDesk Hub API",
        version="0.1.0",
        description="Backend API for internal helpdesk ticket management.",
    )
    app.include_router(system_router, prefix="/api/v1")
    app.include_router(tickets_router, prefix="/api/v1")
    app.include_router(categories_router, prefix="/api/v1")
    return app


app = create_app()
