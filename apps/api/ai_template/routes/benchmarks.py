"""Benchmark routes - harness engineering."""

import pickle
import time
from datetime import datetime

import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ai_template.db import Benchmark, Model, get_db
from ai_template.train import MODELS_DIR

router = APIRouter(prefix="/api/v1/benchmarks", tags=["benchmarks"])


class BenchmarkCreate(BaseModel):
    model_id: int
    name: str
    dataset_size: int | None = 100


class BenchmarkUpdate(BaseModel):
    model_id: int | None = None
    name: str | None = None
    dataset_size: int | None = None


class BenchmarkResponse(BaseModel):
    id: int
    model_id: int | None
    name: str
    dataset_size: int | None
    metrics: dict | None
    duration_ms: int | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[BenchmarkResponse])
def list_benchmarks(db: Session = Depends(get_db)):
    return db.query(Benchmark).all()


@router.get("/{benchmark_id}", response_model=BenchmarkResponse)
def get_benchmark(benchmark_id: int, db: Session = Depends(get_db)):
    bench = db.query(Benchmark).filter(Benchmark.id == benchmark_id).first()
    if not bench:
        raise HTTPException(status_code=404, detail="Benchmark not found")
    return bench


@router.post("/", response_model=BenchmarkResponse, status_code=201)
def run_benchmark(data: BenchmarkCreate, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == data.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    artifact_path = MODELS_DIR / f"{model.name}.pkl"
    if not artifact_path.exists():
        raise HTTPException(status_code=404, detail="Model artifact not found")

    with open(artifact_path, "rb") as f:
        artifact = pickle.load(f)

    weights = np.array(artifact["weights"])
    test_data = np.random.randn(data.dataset_size, 10)

    start = time.time()
    predictions = test_data @ weights
    duration_ms = int((time.time() - start) * 1000)

    metrics = {
        "mean_prediction": float(np.mean(predictions)),
        "std_prediction": float(np.std(predictions)),
        "min_prediction": float(np.min(predictions)),
        "max_prediction": float(np.max(predictions)),
        "samples_per_sec": int(data.dataset_size / max(duration_ms, 1) * 1000),
    }

    bench = Benchmark(
        model_id=data.model_id,
        name=data.name,
        dataset_size=data.dataset_size,
        metrics=metrics,
        duration_ms=duration_ms,
    )
    db.add(bench)
    db.commit()
    db.refresh(bench)
    return bench


@router.patch("/{benchmark_id}", response_model=BenchmarkResponse)
def patch_benchmark(
    benchmark_id: int, data: BenchmarkUpdate, db: Session = Depends(get_db)
):
    bench = db.query(Benchmark).filter(Benchmark.id == benchmark_id).first()
    if not bench:
        raise HTTPException(status_code=404, detail="Benchmark not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(bench, k, v)
    db.commit()
    db.refresh(bench)
    return bench


@router.delete("/{benchmark_id}", status_code=204)
def delete_benchmark(benchmark_id: int, db: Session = Depends(get_db)):
    bench = db.query(Benchmark).filter(Benchmark.id == benchmark_id).first()
    if not bench:
        raise HTTPException(status_code=404, detail="Benchmark not found")
    db.delete(bench)
    db.commit()
