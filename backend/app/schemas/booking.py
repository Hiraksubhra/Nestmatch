from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserResponse
from app.schemas.listing import ListingResponse


class BookingRequestCreate(BaseModel):
    listing_id: str
    move_in_date: date
    duration_months: int = Field(1, ge=1, le=60)
    message: Optional[str] = Field(None, max_length=2000)


class BookingRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    listing_id: str
    student_id: str
    landlord_id: str
    move_in_date: date
    duration_months: int
    status: str
    message: Optional[str] = None
    responded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    student: Optional[UserResponse] = None
    landlord: Optional[UserResponse] = None
    listing: Optional[ListingResponse] = None

    # Revealed contacts when ACCEPTED
    landlord_contact: Optional[dict] = None
    student_contact: Optional[dict] = None
