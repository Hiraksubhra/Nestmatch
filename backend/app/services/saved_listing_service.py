import math
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, delete
from fastapi import HTTPException, status

from app.models.saved_listing import SavedListing
from app.models.listing import Listing
from app.schemas.saved_listing import (
    SavedListingItemResponse,
    PaginatedSavedListingsResponse,
    SavedListingToggleResponse,
)


class SavedListingService:
    @staticmethod
    async def toggle_save_listing(
        db: AsyncSession,
        user_id: str,
        listing_id: str,
    ) -> SavedListingToggleResponse:
        # Check listing exists
        listing_query = select(Listing).where(Listing.id == listing_id)
        listing_res = await db.execute(listing_query)
        listing = listing_res.scalars().first()
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found"
            )

        # Check if already saved
        query = select(SavedListing).where(
            and_(SavedListing.user_id == user_id, SavedListing.listing_id == listing_id)
        )
        res = await db.execute(query)
        existing = res.scalars().first()

        if existing:
            await db.delete(existing)
            await db.commit()
            return SavedListingToggleResponse(
                is_saved=False,
                listing_id=listing_id,
                message="Listing removed from bookmarks",
            )
        else:
            saved = SavedListing(user_id=user_id, listing_id=listing_id)
            db.add(saved)
            await db.commit()
            return SavedListingToggleResponse(
                is_saved=True,
                listing_id=listing_id,
                message="Listing saved to bookmarks",
            )

    @staticmethod
    async def get_saved_listings(
        db: AsyncSession,
        user_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> PaginatedSavedListingsResponse:
        # Count
        count_query = select(func.count(SavedListing.listing_id)).where(
            SavedListing.user_id == user_id
        )
        total_res = await db.execute(count_query)
        total = total_res.scalar() or 0

        # Query items
        offset = (page - 1) * limit
        query = (
            select(SavedListing)
            .where(SavedListing.user_id == user_id)
            .order_by(SavedListing.saved_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(query)
        items = result.scalars().all()

        pages = math.ceil(total / limit) if limit > 0 else 1
        return PaginatedSavedListingsResponse(
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            items=[SavedListingItemResponse.model_validate(item) for item in items],
        )

    @staticmethod
    async def is_listing_saved(
        db: AsyncSession,
        user_id: str,
        listing_id: str,
    ) -> bool:
        query = select(SavedListing).where(
            and_(SavedListing.user_id == user_id, SavedListing.listing_id == listing_id)
        )
        res = await db.execute(query)
        return res.scalars().first() is not None
