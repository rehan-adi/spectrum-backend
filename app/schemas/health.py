from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    success: bool
    status: str
    message: str
