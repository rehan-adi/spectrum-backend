from fastapi import FastAPI
from app.routes.health import health_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Route
app.include_router(health_router, tags=["Health Check"], prefix="/api/v1")