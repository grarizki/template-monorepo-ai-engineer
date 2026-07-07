"""FastAPI server with Scalar docs."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from ai_template.db import init_db
from ai_template.routes import deployments, models, projects, training_scripts


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Template API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(projects.router)
app.include_router(models.router)
app.include_router(training_scripts.router)
app.include_router(deployments.router)


@app.get("/api/v1/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        dark_mode=True,
    )
