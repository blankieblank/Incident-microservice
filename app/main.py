import logging
from fastapi import FastAPI
from app.api.routers import incidents
from app.core.db import Base, engine
from app.core.logging_config import setup_logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Incident Management API")

app.include_router(incidents.router)


@app.on_event("startup")
async def startup():
    setup_logging()
    logger.info("Application startup...")

    async with engine.begin() as conn:
        logger.info("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized.")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Incident Management API"}
