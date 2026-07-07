"""FastAPI server with Scalar docs."""

import pickle
from contextlib import asynccontextmanager

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

from ai_template.db import init_db
from ai_template.routes import (
    benchmarks,
    deployments,
    models,
    projects,
    training_scripts,
)
from ai_template.train import MODELS_DIR


class PredictRequest(BaseModel):
    input: list[float]


class PredictResponse(BaseModel):
    input: list[float]
    prediction: list[list[float]]
    model: str


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
app.include_router(benchmarks.router)


@app.get("/api/v1/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.post("/api/v1/predict", response_model=PredictResponse, tags=["inference"])
def predict(data: PredictRequest, model_name: str = "demo_model"):
    artifact_path = MODELS_DIR / f"{model_name}.pkl"
    if not artifact_path.exists():
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")

    with open(artifact_path, "rb") as f:
        artifact = pickle.load(f)

    weights = np.array(artifact["weights"])
    input_arr = np.array(data.input).reshape(1, -1)

    if input_arr.shape[1] != weights.shape[0]:
        got = input_arr.shape[1]
        want = weights.shape[0]
        raise HTTPException(
            status_code=400,
            detail=f"Input shape {got} != model input {want}",
        )

    result = input_arr @ weights
    return PredictResponse(
        input=data.input,
        prediction=result.tolist(),
        model=model_name,
    )


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        dark_mode=True,
    )
