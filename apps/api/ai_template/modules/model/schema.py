import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ModelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: Optional[uuid.UUID] = None
    artifact_path: Optional[str] = None
    metrics: Optional[dict] = None


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[uuid.UUID] = None
    artifact_path: Optional[str] = None
    metrics: Optional[dict] = None


class ModelResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    project_id: Optional[uuid.UUID] = None
    created_at: Optional[str] = None
    artifact_path: Optional[str] = None
    metrics: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)
