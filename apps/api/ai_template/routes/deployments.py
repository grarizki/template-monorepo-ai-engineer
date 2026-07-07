"""Deployment routes - full CRUD."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ai_template.db import Deployment, get_db

router = APIRouter(prefix="/api/v1/deployments", tags=["deployments"])


class DeploymentCreate(BaseModel):
    model_id: int
    status: str = "pending"
    url: str | None = None


class DeploymentUpdate(BaseModel):
    model_id: int | None = None
    status: str | None = None
    url: str | None = None


class DeploymentResponse(BaseModel):
    id: int
    model_id: int | None
    status: str | None
    deployed_at: datetime | None
    url: str | None

    class Config:
        from_attributes = True


@router.get("/", response_model=list[DeploymentResponse])
def list_deployments(db: Session = Depends(get_db)):
    return db.query(Deployment).all()


@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(deployment_id: int, db: Session = Depends(get_db)):
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment


@router.post("/", response_model=DeploymentResponse, status_code=201)
def create_deployment(data: DeploymentCreate, db: Session = Depends(get_db)):
    deployment = Deployment(**data.model_dump())
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.put("/{deployment_id}", response_model=DeploymentResponse)
def update_deployment(
    deployment_id: int, data: DeploymentCreate, db: Session = Depends(get_db)
):
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    for k, v in data.model_dump().items():
        setattr(deployment, k, v)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.patch("/{deployment_id}", response_model=DeploymentResponse)
def patch_deployment(
    deployment_id: int, data: DeploymentUpdate, db: Session = Depends(get_db)
):
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(deployment, k, v)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.delete("/{deployment_id}", status_code=204)
def delete_deployment(deployment_id: int, db: Session = Depends(get_db)):
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    db.delete(deployment)
    db.commit()
