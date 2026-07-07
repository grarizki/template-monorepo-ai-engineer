import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ai_template.models.database import Deployment
from ai_template.models.engine import db_session
from ai_template.modules.deployment.schema import (
    DeploymentCreate,
    DeploymentResponse,
    DeploymentUpdate,
)

router = APIRouter(prefix="/api/v1/deployments", tags=["deployments"])


@router.get("/", response_model=list[DeploymentResponse])
def list_deployments(db: Session = Depends(db_session)):
    return db.exec(select(Deployment)).all()


@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(deployment_id: str, db: Session = Depends(db_session)):
    deployment = db.exec(
        select(Deployment).where(Deployment.id == uuid.UUID(deployment_id))
    ).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment


@router.post("/", response_model=DeploymentResponse, status_code=201)
def create_deployment(data: DeploymentCreate, db: Session = Depends(db_session)):
    deployment = Deployment(**data.model_dump())
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.put("/{deployment_id}", response_model=DeploymentResponse)
def update_deployment(
    deployment_id: str, data: DeploymentUpdate, db: Session = Depends(db_session)
):
    deployment = db.exec(
        select(Deployment).where(Deployment.id == uuid.UUID(deployment_id))
    ).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(deployment, k, v)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.delete("/{deployment_id}", status_code=204)
def delete_deployment(deployment_id: str, db: Session = Depends(db_session)):
    deployment = db.exec(
        select(Deployment).where(Deployment.id == uuid.UUID(deployment_id))
    ).first()
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    db.delete(deployment)
    db.commit()
