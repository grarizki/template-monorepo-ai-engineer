import uuid
from typing import Optional

from sqlalchemy import JSON
from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(unique=True, description="Project name")
    description: Optional[str] = Field(default=None, description="Project description")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
    image_url: Optional[str] = Field(default=None, description="Project image URL")


class Model(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(unique=True, description="Model name")
    description: Optional[str] = Field(default=None, description="Model description")
    project_id: Optional[uuid.UUID] = Field(default=None, foreign_key="project.id")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
    artifact_path: Optional[str] = Field(
        default=None, description="Path to model artifact"
    )
    metrics: Optional[dict] = Field(
        default=None, sa_type=JSON, description="Training metrics"
    )


class TrainingScript(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(unique=True, description="Script name")
    description: Optional[str] = Field(default=None, description="Script description")
    model_id: Optional[uuid.UUID] = Field(default=None, foreign_key="model.id")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
    image_url: Optional[str] = Field(default=None, description="Script image URL")


class Deployment(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    model_id: Optional[uuid.UUID] = Field(default=None, foreign_key="model.id")
    status: str = Field(default="pending", description="Deployment status")
    deployed_at: Optional[str] = Field(default=None, description="Deployment timestamp")
    url: Optional[str] = Field(default=None, description="Deployment URL")


class Benchmark(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    model_id: Optional[uuid.UUID] = Field(default=None, foreign_key="model.id")
    name: str = Field(description="Benchmark name")
    dataset_size: Optional[int] = Field(default=None, description="Dataset size")
    metrics: Optional[dict] = Field(
        default=None, sa_type=JSON, description="Benchmark metrics"
    )
    duration_ms: Optional[int] = Field(
        default=None, description="Duration in milliseconds"
    )
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")


class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(description="User's full name")
    email: str = Field(index=True, unique=True, description="User's email address")
    password: str = Field(description="Hashed password")
