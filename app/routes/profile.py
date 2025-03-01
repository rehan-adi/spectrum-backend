from app.db.db import prisma
from app.core.logger import logger
from app.utils.token import get_user_id
from app.schemas.profile import UserProfile
from app.schemas.response import ApiResponse, ResponseStatus
from fastapi import APIRouter, Depends, HTTPException, status

profile_router = APIRouter()


@profile_router.get(
    "/", status_code=status.HTTP_200_OK, response_model=ApiResponse[UserProfile]
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
