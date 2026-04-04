from fastapi import FastAPI


app = FastAPI(
    title="HelpDesk Hub API",
    version="0.1.0",
    description="Backend API for internal helpdesk ticket management.",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "name": "HelpDesk Hub API",
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
