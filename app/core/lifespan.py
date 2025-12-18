from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logger import logger
from app.database.connection import create_db_and_tables, connect_to_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Weather App...")

    redis = None

    try:
        await create_db_and_tables()
        logger.info("Database tables created")

        redis = await connect_to_redis()

        await redis.ping()
        app.state.redis = redis
        logger.info("Redis connection established")

        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

    finally:
        if redis:
            try:
                await redis.close()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.error(f"Error closing Redis: {e}")

        logger.info("Shutting down Weather App")
