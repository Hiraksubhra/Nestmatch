import math
from datetime import datetime, timezone, date
from typing import Optional, List, Tuple
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from fastapi import HTTPException, status

from app.models.flatmate import FlatmateProfile
from app.models.user import User
from app.schemas.flatmate import (
    FlatmateProfileCreate,
    FlatmateProfileUpdate,
    FlatmateProfileResponse,
    PaginatedFlatmateProfilesResponse,
)


def calculate_compatibility_score(
    profile_a: Optional[FlatmateProfile],
    profile_b: FlatmateProfile,
) -> Optional[int]:
    """
    Calculate compatibility score (0-100%) between two flatmate profiles.
    - Lifestyle tags overlap: up to 40 points
    - Budget compatibility: up to 30 points
    - City / University alignment: up to 20 points
    - Move-in timeline alignment: up to 10 points

    Returns None if profile_a is None (i.e. viewer is not logged in or has no flatmate profile).
    """
    if not profile_a:
        return None


    score = 0.0

    # 1. Lifestyle Tags (up to 40 pts)
    tags_a = set(t.lower() for t in (profile_a.lifestyle_tags or []))
    tags_b = set(t.lower() for t in (profile_b.lifestyle_tags or []))
    if tags_a and tags_b:
        intersection = tags_a & tags_b
        union = tags_a | tags_b
        score += (len(intersection) / len(union)) * 40.0
    elif not tags_a and not tags_b:
        score += 20.0
    else:
        score += 15.0

    # 2. Budget Compatibility (up to 30 pts)
    min_a = float(profile_a.budget_min or 0)
    max_a = float(profile_a.budget_max)
    min_b = float(profile_b.budget_min or 0)
    max_b = float(profile_b.budget_max)

    overlap_start = max(min_a, min_b)
    overlap_end = min(max_a, max_b)
    if overlap_start <= overlap_end:
        score += 30.0
    else:
        gap = overlap_start - overlap_end
        denom = max(max_a, max_b, 1.0)
        gap_penalty = min(gap / denom, 1.0) * 30.0
        score += max(0.0, 30.0 - gap_penalty)

    # 3. Location (City & University) (up to 20 pts)
    city_a = (profile_a.preferred_city or "").strip().lower()
    city_b = (profile_b.preferred_city or "").strip().lower()
    if city_a and city_b and city_a == city_b:
        score += 10.0

    uni_a = (profile_a.preferred_university or "").strip().lower()
    uni_b = (profile_b.preferred_university or "").strip().lower()
    if uni_a and uni_b and (uni_a in uni_b or uni_b in uni_a):
        score += 10.0
    elif not uni_a or not uni_b:
        score += 5.0

    # 4. Move-in Date Alignment (up to 10 pts)
    if profile_a.move_in_date and profile_b.move_in_date:
        diff_days = abs((profile_a.move_in_date - profile_b.move_in_date).days)
        max_flex = max(profile_a.move_in_flexibility, profile_b.move_in_flexibility, 7)
        if diff_days <= max_flex:
            score += 10.0
        elif diff_days <= max_flex * 2:
            score += 6.0
        else:
            score += 2.0
    else:
        score += 5.0

    final_score = int(round(score))
    return max(15, min(99, final_score))


class FlatmateService:
    @staticmethod
    async def get_my_profile(db: AsyncSession, user_id: str) -> Optional[FlatmateProfile]:
        query = select(FlatmateProfile).where(FlatmateProfile.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_profile_by_id(db: AsyncSession, profile_id: str) -> Optional[FlatmateProfile]:
        query = select(FlatmateProfile).where(FlatmateProfile.id == profile_id)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def upsert_profile(
        db: AsyncSession,
        user_id: str,
        data: FlatmateProfileCreate | FlatmateProfileUpdate,
    ) -> FlatmateProfile:
        existing = await FlatmateService.get_my_profile(db, user_id)
        data_dict = data.model_dump(exclude_unset=True)

        if existing:
            for field, val in data_dict.items():
                setattr(existing, field, val)
            existing.updated_at = datetime.now(timezone.utc)
            profile = existing
        else:
            # Creation requires budget_max
            if "budget_max" not in data_dict or data_dict["budget_max"] is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="budget_max is required to create a flatmate profile"
                )
            profile = FlatmateProfile(
                user_id=user_id,
                **data_dict
            )
            db.add(profile)

        await db.commit()
        await db.refresh(profile)
        return profile

    @staticmethod
    async def deactivate_profile(db: AsyncSession, user_id: str) -> bool:
        profile = await FlatmateService.get_my_profile(db, user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flatmate profile not found"
            )
        profile.is_active = False
        profile.updated_at = datetime.now(timezone.utc)
        await db.commit()
        return True

    @staticmethod
    async def search_profiles(
        db: AsyncSession,
        current_user: Optional[User] = None,
        city: Optional[str] = None,
        university: Optional[str] = None,
        min_budget: Optional[Decimal] = None,
        max_budget: Optional[Decimal] = None,
        gender: Optional[str] = None,
        lifestyle_tags: Optional[List[str]] = None,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedFlatmateProfilesResponse:
        # Get current user's profile if authenticated
        my_profile = None
        if current_user:
            my_profile = await FlatmateService.get_my_profile(db, current_user.id)

        conditions = [FlatmateProfile.is_active == True]

        # Don't show current user's own profile in search results
        if current_user:
            conditions.append(FlatmateProfile.user_id != current_user.id)

        if city:
            conditions.append(FlatmateProfile.preferred_city.ilike(f"%{city}%"))

        if university:
            conditions.append(FlatmateProfile.preferred_university.ilike(f"%{university}%"))

        if min_budget is not None:
            conditions.append(FlatmateProfile.budget_max >= min_budget)

        if max_budget is not None:
            conditions.append(
                or_(
                    FlatmateProfile.budget_min == None,
                    FlatmateProfile.budget_min <= max_budget,
                )
            )

        if gender and gender.upper() != "ANY":
            conditions.append(func.lower(FlatmateProfile.gender) == gender.lower())

        # Count total
        count_query = select(func.count(FlatmateProfile.id)).where(and_(*conditions))
        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        # Query page
        offset = (page - 1) * limit
        query = (
            select(FlatmateProfile)
            .where(and_(*conditions))
            .order_by(FlatmateProfile.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        results = await db.execute(query)
        profiles = results.scalars().all()

        # Build responses with computed compatibility scores
        items: List[FlatmateProfileResponse] = []
        for p in profiles:
            # If tags filter is supplied, optionally boost or filter
            if lifestyle_tags:
                p_tags = set(t.lower() for t in (p.lifestyle_tags or []))
                filter_tags = set(t.lower() for t in lifestyle_tags)
                if not (p_tags & filter_tags):
                    # No overlapping requested tags
                    continue

            score = calculate_compatibility_score(my_profile, p)
            res = FlatmateProfileResponse.model_validate(p)
            res.compatibility_score = score
            items.append(res)

        # Sort items by compatibility score descending if user has a profile
        if my_profile:
            items.sort(key=lambda x: x.compatibility_score or 0, reverse=True)

        pages = math.ceil(total / limit) if limit > 0 else 1

        return PaginatedFlatmateProfilesResponse(
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            items=items,
        )
