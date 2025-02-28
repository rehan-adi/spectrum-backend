from jose import jwt
from typing import Dict, Any
from app.core.config import settings
from datetime import timedelta, datetime, timezone

ALGORITHM = "HS256"


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: Dict[str, Any] = {"id": user_id, "exp": expire}

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token
