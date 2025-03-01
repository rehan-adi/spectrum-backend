from app.db.db import prisma
from prisma.enums import Role
from app.core.logger import logger
from app.utils.token import get_user_id
from app.schemas.profile import UserProfile
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.response import ApiResponse, ResponseStatus, MessageResponse

profile_router = APIRouter()


@profile_router.get(
    "/me", status_code=status.HTTP_200_OK, response_model=ApiResponse[UserProfile]
)
async def get_profile(user_id: str = Depends(get_user_id)):
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
            instagram=user.instagram,
            twitter=user.twitter,
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


@profile_router.post(
    "/upgrade-to-artist", status_code=status.HTTP_200_OK, response_model=MessageResponse
)
async def upgrade_to_artist(user_id: str = Depends(get_user_id)):
    try:
        user = await prisma.user.find_unique(where={"id": user_id})

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
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
    "/account/delete", status_code=status.HTTP_200_OK, response_model=MessageResponse
)
async def delete_account(user_id: str = Depends(get_user_id)):
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
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
