import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import CORS_ORIGINS
from .database import Base, engine
from .routes import endpoints, health, tickets, dashboard, auth
from .models import models
from .seed import init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("endpoint-support")

init_database()

app = FastAPI(
    title="Endpoint Health & IT Support API",
    version="1.0.0",
    description="Endpoint monitoring and IT support REST API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "name": "Endpoint Health & IT Support API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
def api_health():
    return {"status": "ok"}

app.include_router(endpoints.router)
app.include_router(health.router)
app.include_router(tickets.router)
app.include_router(dashboard.router)
app.include_router(auth.router)
