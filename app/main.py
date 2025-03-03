from fastapi import FastAPI
from app.core.logger import logger
from app.core.config import settings
from app.routes.auth import auth_router
from contextlib import asynccontextmanager
from app.routes.health import health_router
from app.routes.profile import profile_router
from app.db.db import db_connect, db_disconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.limiter import init_limiter, close_limiter
from app.core.redis import connect_redis, disconnect_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_connect()
    logger.info("✅ Database connect")

    await connect_redis()
    await init_limiter()

    yield

    # Shutdown
    await db_disconnect()
    logger.info("❌ Database disconnected!")

    await disconnect_redis()
    await close_limiter()


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
app.include_router(profile_router, tags=["Profile Routes"], prefix="/api/v1/profile")
