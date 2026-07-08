import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeploymentCreate(BaseModel):
    model_id: Optional[uuid.UUID] = None
    status: str = "pending"
    url: Optional[str] = None


class DeploymentUpdate(BaseModel):
    model_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    url: Optional[str] = None


class DeploymentResponse(BaseModel):
    id: uuid.UUID
    model_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    deployed_at: Optional[str] = None
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
