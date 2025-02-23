from fastapi import APIRouter
from app.schemas.health import HealthCheckResponse

health_router = APIRouter()

@health_router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(success=True, status="ok", message="Service is healthy")