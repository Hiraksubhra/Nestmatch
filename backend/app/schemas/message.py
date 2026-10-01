from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserResponse
from app.schemas.listing import ListingResponse


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    message_type: str = Field("TEXT", pattern="^(TEXT|SYSTEM|MEDIA)$")


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    sender_id: str
    content: str
    message_type: str
    is_read: bool
    created_at: datetime
    sender: Optional[UserResponse] = None


class ConversationCreate(BaseModel):
    listing_id: Optional[str] = None
    landlord_id: Optional[str] = None
    initial_message: Optional[str] = Field(None, min_length=1, max_length=5000)


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    listing_id: Optional[str] = None
    student_id: str
    landlord_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    student: Optional[UserResponse] = None
    landlord: Optional[UserResponse] = None
    listing: Optional[ListingResponse] = None
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0
