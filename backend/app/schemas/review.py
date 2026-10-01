from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserResponse


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    body: Optional[str] = Field(None, max_length=2000)


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    listing_id: str
    reviewer_id: str
    rating: int
    title: Optional[str] = None
    body: Optional[str] = None
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime
    reviewer: Optional[UserResponse] = None


class ListingReviewsSummaryResponse(BaseModel):
    reviews: List[ReviewResponse]
    average_rating: float
    total_reviews: int
    rating_breakdown: Dict[int, int]  # {5: X, 4: Y, 3: Z, 2: W, 1: V}
