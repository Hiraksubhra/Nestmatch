from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserResponse


class FlatmateProfileBase(BaseModel):
    budget_min: Optional[Decimal] = Field(None, ge=0)
    budget_max: Decimal = Field(..., gt=0)
    preferred_city: Optional[str] = Field(None, max_length=100)
    preferred_university: Optional[str] = Field(None, max_length=200)
    preferred_locality: Optional[str] = Field(None, max_length=150)
    move_in_date: Optional[date] = None
    move_in_flexibility: int = Field(7, ge=0, le=90)
    gender: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=280)
    lifestyle_tags: List[str] = Field(default_factory=list)


class FlatmateProfileCreate(FlatmateProfileBase):
    pass


class FlatmateProfileUpdate(BaseModel):
    budget_min: Optional[Decimal] = Field(None, ge=0)
    budget_max: Optional[Decimal] = Field(None, gt=0)
    preferred_city: Optional[str] = Field(None, max_length=100)
    preferred_university: Optional[str] = Field(None, max_length=200)
    preferred_locality: Optional[str] = Field(None, max_length=150)
    move_in_date: Optional[date] = None
    move_in_flexibility: Optional[int] = Field(None, ge=0, le=90)
    gender: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=280)
    lifestyle_tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class FlatmateProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    budget_min: Optional[Decimal] = None
    budget_max: Decimal
    preferred_city: Optional[str] = None
    preferred_university: Optional[str] = None
    preferred_locality: Optional[str] = None
    move_in_date: Optional[date] = None
    move_in_flexibility: int = 7
    gender: Optional[str] = None
    bio: Optional[str] = None
    lifestyle_tags: List[str] = []
    is_active: bool = True
    compatibility_score: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None


class PaginatedFlatmateProfilesResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: List[FlatmateProfileResponse]
