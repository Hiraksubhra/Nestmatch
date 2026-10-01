from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.listing import ListingResponse


class SavedListingToggleResponse(BaseModel):
    is_saved: bool
    listing_id: str
    message: str


class SavedListingItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str
    listing_id: str
    saved_at: datetime
    listing: Optional[ListingResponse] = None


class PaginatedSavedListingsResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: List[SavedListingItemResponse]
