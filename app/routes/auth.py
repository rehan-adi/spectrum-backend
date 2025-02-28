from app.db.db import prisma
from app.core.logger import logger
from app.schemas.auth import Signup
from app.utils.password import hash_password
from fastapi import APIRouter, HTTPException, status

auth_router = APIRouter()


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: Signup):
    email = data.email
    password = data.password

    try:
        existing_user = await prisma.user.find_first(where={"email": email})
    except Exception:
        logger.error("DB Error while checking existing user", exc_info=True)
        raise HTTPException(
            status_code=500, detail="DB Error while checking existing user"
        )

    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use")

    password_hash = hash_password(password)

    try:
        await prisma.user.create(
            data={
                "email": email,
                "password": password_hash,
            }
        )
        return {"status": "success", "message": "User created successfully"}
    except Exception:
        logger.error("DB Error while creating user", exc_info=True)
        raise HTTPException(status_code=500, detail="DB Error while creating user")
