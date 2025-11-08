import enum
from sqlalchemy import Column, Integer, String, DateTime, func, Enum

from app.core.db import Base


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSource(str, enum.Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
    OTHER = "other"


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False)
    source = Column(Enum(IncidentSource), default=IncidentSource.OTHER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
