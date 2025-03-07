from app.db.db import prisma
from app.core.logger import logger
from app.schemas.auth import Signup, Signin
from app.utils.token import create_access_token
from fastapi_limiter.depends import RateLimiter
from app.utils.password import hash_password, verify_password
from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.schemas.response import MessageResponse, ResponseStatus, ApiResponse

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
)
async def signup(data: Signup) -> MessageResponse:
    email = data.email
    password = data.password

    try:
        existing_user = await prisma.user.find_unique(where={"email": email})
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
        return MessageResponse(
            status=ResponseStatus.SUCCESS, message="User created successfully"
        )
    except Exception:
        logger.error("DB Error while creating user", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Error while creating user")


@auth_router.post(
    "/signin",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse,
)
async def signin(data: Signin, response: Response) -> ApiResponse:
    email = data.email
    password = data.password

    try:
        user = await prisma.user.find_unique(where={"email": email})
    except Exception:
        logger.error("Failed to get user details from db", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch user details")

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
        value=token,
        httponly=True,
        max_age=2 * 24 * 60 * 60,
        samesite="lax",
        secure=False,
    )

    return ApiResponse(
        status=ResponseStatus.SUCCESS, data={"token": token}, message="Login successful"
    )


@auth_router.post(
    "/logout",
    dependencies=[Depends(RateLimiter(times=30, seconds=60))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
)
async def logout(response: Response) -> MessageResponse:
    response.delete_cookie("token")
    return MessageResponse(
        status=ResponseStatus.SUCCESS, message="Logged out successfully"
    )
