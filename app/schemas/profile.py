from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str]
    profileImage: Optional[str]
    role: str
    twitter: Optional[str]
    instagram: Optional[str]
    createdAt: datetime


class UpdateProfile(BaseModel):
    name: Optional[str]
    profileImage: Optional[str]
    twitter: Optional[str]
    instagram: Optional[str]
