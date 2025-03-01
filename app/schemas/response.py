from enum import Enum
from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    FAIL = "fail"


class ApiResponse(BaseModel, Generic[T]):
    status: ResponseStatus
    data: Optional[T] = None
    message: Optional[str] = None


class MessageResponse(BaseModel):
    status: ResponseStatus
    message: Optional[str] = None
