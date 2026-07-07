"""Model version routes - semantic versioning for trained models."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ai_template.db import Model, ModelVersion, get_db

router = APIRouter(prefix="/api/v1/models/{model_id}/versions", tags=["model-versions"])


class VersionCreate(BaseModel):
    version: str
    metrics: dict | None = None
    artifact_path: str | None = None


class VersionUpdate(BaseModel):
    version: str | None = None
    metrics: dict | None = None
    artifact_path: str | None = None


class VersionResponse(BaseModel):
    id: int
    model_id: int
    version: str
    metrics: dict | None
    artifact_path: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[VersionResponse])
def list_versions(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return db.query(ModelVersion).filter(ModelVersion.model_id == model_id).all()


@router.post("/", response_model=VersionResponse, status_code=201)
def create_version(model_id: int, data: VersionCreate, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    version = ModelVersion(model_id=model_id, **data.model_dump())
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


@router.get("/{version_id}", response_model=VersionResponse)
def get_version(model_id: int, version_id: int, db: Session = Depends(get_db)):
    version = (
        db.query(ModelVersion)
        .filter(ModelVersion.id == version_id, ModelVersion.model_id == model_id)
        .first()
    )
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


@router.delete("/{version_id}", status_code=204)
def delete_version(model_id: int, version_id: int, db: Session = Depends(get_db)):
    version = (
        db.query(ModelVersion)
        .filter(ModelVersion.id == version_id, ModelVersion.model_id == model_id)
        .first()
    )
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    db.delete(version)
    db.commit()
