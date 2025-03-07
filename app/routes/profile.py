from app.db.db import prisma
from typing import Optional
from prisma.enums import Role
from app.core.logger import logger
from app.utils.token import get_user_id
from fastapi_limiter.depends import RateLimiter
from app.schemas.profile import UserProfile, UpdateProfile
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.response import ApiResponse, ResponseStatus, MessageResponse

profile_router = APIRouter()


@profile_router.get(
    "/me",
    dependencies=[Depends(RateLimiter(times=60, seconds=60))],
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[UserProfile],
)
async def get_profile(user_id: str = Depends(get_user_id)) -> ApiResponse[UserProfile]:
    try:
        user = await prisma.user.find_unique(where={"id": user_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        profile = UserProfile(
            id=user.id,
            name=user.name,
            email=user.email,
            profileImage=user.profileImage,
            role=user.role,
            twitter=user.twitter,
            instagram=user.instagram,
            createdAt=user.createdAt,
        )

        return ApiResponse(
            status=ResponseStatus.SUCCESS,
            data=profile,
            message="User profile fetched successfully",
        )

    except Exception:
        logger.error("DB error while getting user profile", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@profile_router.put(
    "/update",
    dependencies=[Depends(RateLimiter(times=2, seconds=60))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
)
async def update_profile(
    data: UpdateProfile, user_id: str = Depends(get_user_id)
) -> MessageResponse:
    try:
        user = await prisma.user.find_unique(where={"id": user_id})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        update_data: dict[str, Optional[str]] = {}

        if data.name is not None:
            update_data["name"] = data.name

        if data.profileImage is not None:
            update_data["profileImage"] = str(data.profileImage)

        if data.twitter is not None:
            update_data["twitter"] = str(data.twitter)

        if data.instagram is not None:
            update_data["instagram"] = str(data.instagram)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        await prisma.user.update(
            where={"id": user_id},
            data=update_data,  # type: ignore
        )

        return MessageResponse(
            status=ResponseStatus.SUCCESS, message="Profile successfully updated."
        )

    except Exception:
        logger.error("Failed to update user profile", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@profile_router.get(
    "/get/{user_id}",
    dependencies=[Depends(RateLimiter(times=100, seconds=60))],
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[UserProfile],
)
async def get_users_profile(user_id: str) -> ApiResponse[UserProfile]:
    try:
        user_profile = await prisma.user.find_unique(where={"id": user_id})

        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        profile_data = UserProfile(
            id=user_profile.id,
            name=user_profile.name,
            email=user_profile.email,
            role=user_profile.role,
            profileImage=user_profile.profileImage,
            twitter=user_profile.twitter,
            instagram=user_profile.instagram,
            createdAt=user_profile.createdAt,
        )

        return ApiResponse(
            status=ResponseStatus.SUCCESS,
            data=profile_data,
            message="Profile details retrieved successfully.",
        )

    except Exception:
        logger.error("Failed to get User profile", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@profile_router.post(
    "/upgrade-to-artist",
    dependencies=[Depends(RateLimiter(times=3, seconds=60))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
)
async def upgrade_to_artist(user_id: str = Depends(get_user_id)) -> MessageResponse:
    try:
        user = await prisma.user.find_unique(where={"id": user_id})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if user.role == Role.Artist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already an artist. This action can only be performed once.",
            )

        await prisma.user.update(where={"id": user_id}, data={"role": Role.Artist})

        return MessageResponse(
            status=ResponseStatus.SUCCESS,
            message="User upgraded to artist successfully",
        )

    except Exception:
        logger.error("DB error while updating user profile", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@profile_router.delete(
    "/account/delete",
    dependencies=Depends(RateLimiter(times=3, seconds=60)),
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
)
async def delete_account(user_id: str = Depends(get_user_id)) -> MessageResponse:
    try:
        user = await prisma.user.find_unique(where={"id": user_id})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        await prisma.user.delete(where={"id": user_id})

        return MessageResponse(
            status=ResponseStatus.SUCCESS, message="Account deleted successfully"
        )

    except Exception:
        logger.error("Failed to delete account", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
