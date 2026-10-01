from datetime import datetime, timezone
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException, status

from app.models.review import Review
from app.models.listing import Listing
from app.models.booking import BookingRequest, BookingStatus
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewResponse,
    ListingReviewsSummaryResponse,
)


class ReviewService:
    @staticmethod
    async def create_review(
        db: AsyncSession,
        reviewer_id: str,
        listing_id: str,
        data: ReviewCreate,
    ) -> Review:
        # Check listing existence
        listing_query = select(Listing).where(Listing.id == listing_id)
        listing_res = await db.execute(listing_query)
        listing = listing_res.scalars().first()
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found"
            )

        # Landlords cannot review their own listing
        if listing.landlord_id == reviewer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Landlords cannot review their own listing"
            )

        # Check for existing review by this user on this listing
        existing_query = select(Review).where(
            and_(Review.listing_id == listing_id, Review.reviewer_id == reviewer_id)
        )
        existing_res = await db.execute(existing_query)
        if existing_res.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already submitted a review for this listing"
            )

        # Check if reviewer has an accepted/completed booking for this listing
        booking_query = select(BookingRequest).where(
            and_(
                BookingRequest.listing_id == listing_id,
                BookingRequest.student_id == reviewer_id,
                BookingRequest.status == BookingStatus.ACCEPTED.value,
            )
        )
        booking_res = await db.execute(booking_query)
        has_accepted_booking = booking_res.scalars().first() is not None

        review = Review(
            listing_id=listing_id,
            reviewer_id=reviewer_id,
            rating=data.rating,
            title=data.title,
            body=data.body,
            is_verified=has_accepted_booking,
        )
        db.add(review)
        await db.commit()
        await db.refresh(review)
        return review

    @staticmethod
    async def get_listing_reviews(
        db: AsyncSession,
        listing_id: str,
    ) -> ListingReviewsSummaryResponse:
        query = (
            select(Review)
            .where(Review.listing_id == listing_id)
            .order_by(Review.created_at.desc())
        )
        result = await db.execute(query)
        reviews = result.scalars().all()

        total = len(reviews)
        breakdown: Dict[int, int] = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        total_rating_sum = 0

        review_responses: List[ReviewResponse] = []
        for r in reviews:
            breakdown[r.rating] = breakdown.get(r.rating, 0) + 1
            total_rating_sum += r.rating
            review_responses.append(ReviewResponse.model_validate(r))

        avg_rating = round(total_rating_sum / total, 1) if total > 0 else 0.0

        return ListingReviewsSummaryResponse(
            reviews=review_responses,
            average_rating=avg_rating,
            total_reviews=total,
            rating_breakdown=breakdown,
        )
