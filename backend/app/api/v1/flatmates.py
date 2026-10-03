from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.schemas.flatmate import (
    FlatmateProfileCreate,
    FlatmateProfileUpdate,
    FlatmateProfileResponse,
    PaginatedFlatmateProfilesResponse,
)
from app.services.flatmate_service import FlatmateService, calculate_compatibility_score

router = APIRouter(prefix="/flatmates", tags=["Flatmates"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Browse and search flatmate profiles"
)
async def browse_flatmates(
    city: Optional[str] = Query(None, description="Preferred city"),
    university: Optional[str] = Query(None, description="Preferred university"),
    min_budget: Optional[Decimal] = Query(None, ge=0, description="Min budget filter"),
    max_budget: Optional[Decimal] = Query(None, ge=0, description="Max budget filter"),
    gender: Optional[str] = Query(None, description="Gender: MALE, FEMALE, ANY"),
    tags: Optional[str] = Query(None, description="Comma-separated lifestyle tags"),
    min_match: Optional[int] = Query(None, ge=0, le=100, description="Minimum match percentage threshold"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_optional_current_user),
    session: AsyncSession = Depends(get_db),
):
    lifestyle_tags = None
    if tags:
        lifestyle_tags = [t.strip() for t in tags.split(",") if t.strip()]

    result = await FlatmateService.search_profiles(
        db=session,
        current_user=current_user,
        city=city,
        university=university,
        min_budget=min_budget,
        max_budget=max_budget,
        gender=gender,
        lifestyle_tags=lifestyle_tags,
        min_match=min_match,
        page=page,
        limit=limit,
    )

    return {
        "success": True,
        "data": [item.model_dump() for item in result.items],
        "meta": {
            "total": result.total,
            "page": result.page,
            "limit": result.limit,
            "pages": result.pages,
        }
    }


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user's flatmate profile"
)
async def get_my_flatmate_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    profile = await FlatmateService.get_my_profile(session, current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't created a flatmate profile yet."
        )

    return {
        "success": True,
        "data": FlatmateProfileResponse.model_validate(profile).model_dump()
    }


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Create or update current user's flatmate profile"
)
async def upsert_my_flatmate_profile(
    data: FlatmateProfileCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    profile = await FlatmateService.upsert_profile(
        db=session,
        user_id=current_user.id,
        data=data,
    )
    return {
        "success": True,
        "message": "Flatmate profile saved successfully",
        "data": FlatmateProfileResponse.model_validate(profile).model_dump()
    }


@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Deactivate current user's flatmate profile"
)
async def deactivate_my_flatmate_profile(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await FlatmateService.deactivate_profile(session, current_user.id)
    return {
        "success": True,
        "message": "Flatmate profile deactivated successfully"
    }


@router.get(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a specific flatmate profile by ID"
)
async def get_flatmate_profile_by_id(
    profile_id: str,
    current_user: Optional[User] = Depends(get_optional_current_user),
    session: AsyncSession = Depends(get_db),
):
    profile = await FlatmateService.get_profile_by_id(session, profile_id)
    if not profile or not profile.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flatmate profile not found"
        )

    my_profile = None
    if current_user:
        my_profile = await FlatmateService.get_my_profile(session, current_user.id)

    score = calculate_compatibility_score(my_profile, profile)
    res = FlatmateProfileResponse.model_validate(profile)
    res.compatibility_score = score

    return {
        "success": True,
        "data": res.model_dump()
    }
