import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ai_template.models.database import Model
from ai_template.models.engine import db_session
from ai_template.modules.model.schema import ModelCreate, ModelResponse, ModelUpdate

router = APIRouter(prefix="/api/v1/models", tags=["models"])


@router.get("/", response_model=list[ModelResponse])
def list_models(db: Session = Depends(db_session)):
    return db.exec(select(Model)).all()


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: str, db: Session = Depends(db_session)):
    model = db.exec(select(Model).where(Model.id == uuid.UUID(model_id))).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model


@router.post("/", response_model=ModelResponse, status_code=201)
def create_model(data: ModelCreate, db: Session = Depends(db_session)):
    model = Model(**data.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@router.put("/{model_id}", response_model=ModelResponse)
def update_model(model_id: str, data: ModelUpdate, db: Session = Depends(db_session)):
    model = db.exec(select(Model).where(Model.id == uuid.UUID(model_id))).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(model, k, v)
    db.commit()
    db.refresh(model)
    return model


@router.delete("/{model_id}", status_code=204)
def delete_model(model_id: str, db: Session = Depends(db_session)):
    model = db.exec(select(Model).where(Model.id == uuid.UUID(model_id))).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    db.delete(model)
    db.commit()
