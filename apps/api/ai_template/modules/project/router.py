import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ai_template.models.database import Project
from ai_template.models.engine import db_session
from ai_template.modules.project.schema import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(db_session)):
    return db.exec(select(Project)).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(db_session)):
    project = db.exec(
        select(Project).where(Project.id == uuid.UUID(project_id))
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(db_session)):
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str, data: ProjectUpdate, db: Session = Depends(db_session)
):
    project = db.exec(
        select(Project).where(Project.id == uuid.UUID(project_id))
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(project, k, v)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: str, db: Session = Depends(db_session)):
    project = db.exec(
        select(Project).where(Project.id == uuid.UUID(project_id))
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
