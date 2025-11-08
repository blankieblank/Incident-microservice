from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.incident_repo import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentUpdate
from app.models.incident import Incident, IncidentStatus


async def create_incident(incident_data: IncidentCreate, db_session: AsyncSession) -> Incident:
    repo = IncidentRepository(db_session)
    return await repo.create_incident(incident_data)


async def get_all_incidents(db_session: AsyncSession, status: Optional[IncidentStatus] = None) -> List[Incident]:
    repo = IncidentRepository(db_session)
    return await repo.get_incidents(status)


async def update_incident_status(incident_id: int, status_update: IncidentUpdate, db_session: AsyncSession) -> Optional[Incident]:
    repo = IncidentRepository(db_session)
    return await repo.update_incident_status(incident_id, status_update)