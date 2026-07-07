"""Training script routes - full CRUD."""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_template.db import TrainingScript, get_db

router = APIRouter(prefix="/api/v1/training-scripts", tags=["training-scripts"])


class TrainingScriptCreate(BaseModel):
    name: str
    description: Optional[str] = None
    model_id: Optional[int] = None
    image_url: Optional[str] = None


class TrainingScriptUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_id: Optional[int] = None
    image_url: Optional[str] = None


class TrainingScriptResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    model_id: Optional[int]
    created_at: Optional[datetime]
    image_url: Optional[str]

    class Config:
        from_attributes = True


@router.get("/", response_model=list[TrainingScriptResponse])
def list_training_scripts(db: Session = Depends(get_db)):
    return db.query(TrainingScript).all()


@router.get("/{script_id}", response_model=TrainingScriptResponse)
def get_training_script(script_id: int, db: Session = Depends(get_db)):
    script = db.query(TrainingScript).filter(TrainingScript.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Training script not found")
    return script


@router.post("/", response_model=TrainingScriptResponse, status_code=201)
def create_training_script(data: TrainingScriptCreate, db: Session = Depends(get_db)):
    script = TrainingScript(**data.model_dump())
    db.add(script)
    db.commit()
    db.refresh(script)
    return script


@router.put("/{script_id}", response_model=TrainingScriptResponse)
def update_training_script(
    script_id: int, data: TrainingScriptCreate, db: Session = Depends(get_db)
):
    script = db.query(TrainingScript).filter(TrainingScript.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Training script not found")
    for k, v in data.model_dump().items():
        setattr(script, k, v)
    db.commit()
    db.refresh(script)
    return script


@router.patch("/{script_id}", response_model=TrainingScriptResponse)
def patch_training_script(
    script_id: int, data: TrainingScriptUpdate, db: Session = Depends(get_db)
):
    script = db.query(TrainingScript).filter(TrainingScript.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Training script not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(script, k, v)
    db.commit()
    db.refresh(script)
    return script


@router.delete("/{script_id}", status_code=204)
def delete_training_script(script_id: int, db: Session = Depends(get_db)):
    script = db.query(TrainingScript).filter(TrainingScript.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Training script not found")
    db.delete(script)
    db.commit()
