from app.db.db import prisma
from app.core.logger import logger
from app.schemas.auth import Signup, Signin
from app.utils.token import create_access_token
from app.utils.password import hash_password, verify_password
from fastapi import APIRouter, HTTPException, status, Response

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


@auth_router.post("/signin", status_code=status.HTTP_200_OK)
async def signin(data: Signin, response: Response):
    email = data.email
    password = data.password

    try:
        user = await prisma.user.find_first(where={"email": email})
    except Exception:
        logger.error("Failed to get user details from db", exc_info=True)
        raise HTTPException(status_code=500, detail="fuck")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    valid_password = verify_password(password, user.password)

    if not valid_password:
        raise HTTPException(
            status_code=401, detail="Incorrect password. Please try again."
        )

    token = create_access_token(user_id=user.id)

    response.set_cookie(
        key="token",
        value=f"Bearer {token}",
        httponly=False,
        max_age=2 * 24 * 60 * 60,
        samesite="lax",
        secure=True,
    )

    return {"status": "success", "token": token, "message": "Login successful"}


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie("token")
    return {"status": "success", "message": "Logged out successfully"}
