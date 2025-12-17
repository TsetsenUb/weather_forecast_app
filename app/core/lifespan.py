from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logger import logger
from app.database.connection import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Weather App...")

    try:
        await create_db_and_tables()
        logger.info("Database tables created")

        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

    finally:
        logger.info("Shutting down Weather App")
