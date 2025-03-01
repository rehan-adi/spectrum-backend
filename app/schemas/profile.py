from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserProfile(BaseModel):
    id: str
    email: str
    name: Optional[str]
    profileImage: Optional[str]
    instagram: Optional[str]
    twitter: Optional[str]
    createdAt: datetime
