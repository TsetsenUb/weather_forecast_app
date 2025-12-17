from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import weather, users
from app.middleware.logging_middleware import log_requests
from app.core.lifespan import lifespan


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
