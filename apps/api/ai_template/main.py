from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from ai_template.core.settings import settings
from ai_template.models.init_db import init_db
from ai_template.modules.auth.router import auth_router
from ai_template.modules.deployment.router import router as deployment_router
from ai_template.modules.model.router import router as model_router
from ai_template.modules.project.router import router as project_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(model_router)
app.include_router(deployment_router)


@app.get("/api/v1/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
