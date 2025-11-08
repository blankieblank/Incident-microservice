import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from app.models.incident import Incident, IncidentStatus
from app.schemas.incident import IncidentCreate, IncidentUpdate

logger = logging.getLogger(__name__)


class IncidentRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_incident(self, incident: IncidentCreate) -> Incident:
        try:
            new_incident = Incident(description=incident.description, source=incident.source)
            self.db_session.add(new_incident)
            await self.db_session.commit()
            await self.db_session.refresh(new_incident)
            return new_incident
        except SQLAlchemyError as e:
            logger.error(f"Database error during incident creation: {e}", exc_info=True)
            await self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during incident creation."
            )

    async def get_incident_by_id(self, incident_id: int) -> Optional[Incident]:
        try:
            result = await self.db_session.execute(select(Incident).where(Incident.id == incident_id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching incident by id={incident_id}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred while fetching the incident."
            )

    async def get_incidents(self, status: Optional[IncidentStatus] = None) -> List[Incident]:
        try:
            query = select(Incident).order_by(Incident.id)
            if status:
                query = query.where(Incident.status == status)
            result = await self.db_session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching incidents: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred while fetching incidents."
            )

    async def update_incident_status(self, incident_id: int, incident_update: IncidentUpdate) -> Optional[Incident]:
        try:
            incident = await self.get_incident_by_id(incident_id)
            if incident:
                incident.status = incident_update.status
                await self.db_session.commit()
                await self.db_session.refresh(incident)
            return incident
        except SQLAlchemyError as e:
            logger.error(f"Database error during incident update for id={incident_id}: {e}", exc_info=True)
            await self.db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred during incident update."
            )
