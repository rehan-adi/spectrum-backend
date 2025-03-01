from typing import Dict, Any
from jose import jwt, JWTError
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Cookie, HTTPException, status
from datetime import timedelta, datetime, timezone

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: Dict[str, Any] = {"id": user_id, "exp": expire}

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token


async def get_user_id(token: str = Cookie(None)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
