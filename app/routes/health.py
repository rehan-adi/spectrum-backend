from fastapi import APIRouter, status
from app.schemas.response import MessageResponse, ResponseStatus

health_router = APIRouter()


@health_router.get("/", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def health_check() -> MessageResponse:
    return MessageResponse(status=ResponseStatus.SUCCESS, message="Service is healthy")
