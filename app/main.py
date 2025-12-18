from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import weather, users
from app.middleware.logging_middleware import log_requests
from app.core.lifespan import lifespan
from app.core.config import settings


app = FastAPI(title="Weather_App", lifespan=lifespan)

app.middleware("http")(log_requests)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(weather.router)
app.include_router(users.router)
