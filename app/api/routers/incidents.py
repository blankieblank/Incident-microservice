from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.db import get_db
from app.schemas.incident import Incident, IncidentCreate, IncidentUpdate
from app.models.incident import IncidentStatus

from app.services import incident_service

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post("/", response_model=Incident, status_code=status.HTTP_201_CREATED)
async def create_new_incident(incident_data: IncidentCreate, db: AsyncSession = Depends(get_db)):
    """
    Заявить (создать) об инциденте.
    """
    return await incident_service.create_incident(
        incident_data=incident_data, db_session=db
    )


@router.get("/", response_model=List[Incident])
async def read_all_incidents(filter_status: Optional[IncidentStatus] = None, db: AsyncSession = Depends(get_db)):
    """
    Получить список инцидентов. По умолчанию возвращает все инциденты. Можно отфильтровать по статусу.
    Возвращает 404, если по заданному статусу ничего не найдено.
    """
    incidents = await incident_service.get_all_incidents(
        db_session=db, status=filter_status
    )
    if not incidents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Нет инцидентов с соответствующим статусом."
        )
    return incidents


@router.patch("/{incident_id}", response_model=Incident)
async def patch_incident_status(incident_id: int, incident_update: IncidentUpdate, db: AsyncSession = Depends(get_db)):
    """
    Обновить статус инцидента по ID.
    """
    updated_incident = await incident_service.update_incident_status(
        incident_id=incident_id, status_update=incident_update, db_session=db
    )
    if not updated_incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден.")
    return updated_incident
