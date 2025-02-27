from fastapi import FastAPI
from app.core.logger import logger
from app.core.config import settings
from app.routes.auth import auth_router
from contextlib import asynccontextmanager
from app.routes.health import health_router
from app.db.db import db_connect, db_disconnect
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_connect()
    logger.info("✅ Database connect")

    yield

    # Shutdown
    await db_disconnect()
    logger.info("❌ Database disconnected!")


app = FastAPI(lifespan=lifespan)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Routes
app.include_router(health_router, tags=["Health Route"], prefix="/api/v1/health")
app.include_router(auth_router, tags=["Authentication Routes"], prefix="/api/v1/auth")
