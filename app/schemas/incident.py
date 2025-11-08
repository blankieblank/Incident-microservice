from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.models.incident import IncidentStatus, IncidentSource


class IncidentBase(BaseModel):
    description: str
    source: IncidentSource


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    status: IncidentStatus


class Incident(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime

    class Config:
        orm_mode = True
