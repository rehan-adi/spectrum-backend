from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.health import health_router
from app.db.db import db_connect, db_disconnect
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_connect()
    print("✅ Database connected!")
    
    yield

    # Shutdown
    await db_disconnect()
    print("❌ Database disconnected!")

app = FastAPI(lifespan=lifespan);

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Route
app.include_router(health_router, tags=["Health Check"], prefix="/api/v1")