from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routers import weather, users
from app.database.connection import create_db_and_tables
from app.middleware.logging_middleware import log_requests
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Weather App...")
    try:
        await create_db_and_tables()
        logger.info("Database tables created")
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise
    yield
    logger.info("Shutting down Weather App")


app = FastAPI(title="Weather_App", lifespan=lifespan)

app.middleware("http")(log_requests)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)

app.include_router(weather.router)
app.include_router(users.router)
