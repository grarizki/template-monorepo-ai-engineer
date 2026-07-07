from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from ai_template.core.settings import settings
from ai_template.models.init_db import init_db
from ai_template.modules.auth.router import auth_router
from ai_template.modules.stock.router import stocks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(stocks_router)


@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
