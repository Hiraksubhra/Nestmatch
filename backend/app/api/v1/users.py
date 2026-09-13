from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user profile"
)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve authenticated user profile.
    """
    return {
        "success": True,
        "data": UserResponse.model_validate(current_user).model_dump()
    }


@router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Update current user profile"
)
async def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Update profile fields for the authenticated user.
    """
    updated = await AuthService.update_profile(session, current_user, update_data)
    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": UserResponse.model_validate(updated).model_dump()
    }
