"""Model routes - full CRUD."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_template.db import Model, get_db

router = APIRouter(prefix="/api/v1/models", tags=["models"])


class ModelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    artifact_path: Optional[str] = None
    metrics: Optional[dict] = None


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    artifact_path: Optional[str] = None
    metrics: Optional[dict] = None


class ModelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    project_id: Optional[int]
    created_at: Optional[datetime]
    artifact_path: Optional[str]
    metrics: Optional[dict]

    class Config:
        from_attributes = True


@router.get("/", response_model=list[ModelResponse])
def list_models(db: Session = Depends(get_db)):
    return db.query(Model).all()


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.post("/", response_model=ModelResponse, status_code=201)
def create_model(data: ModelCreate, db: Session = Depends(get_db)):
    model = Model(**data.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.put("/{model_id}", response_model=ModelResponse)
def update_model(model_id: int, data: ModelCreate, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    for k, v in data.model_dump().items():
        setattr(model, k, v)
    db.commit()
    db.refresh(model)
    return model


@router.patch("/{model_id}", response_model=ModelResponse)
def patch_model(model_id: int, data: ModelUpdate, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(model, k, v)
    db.commit()
    db.refresh(model)
    return model


@router.delete("/{model_id}", status_code=204)
def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    db.delete(model)
    db.commit()
