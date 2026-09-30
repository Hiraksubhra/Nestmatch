from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, ConfigDict, Field
from app.models.listing import (
    PropertyType,
    GenderPreference,
    FurnishedStatus,
    ListingStatus,
    RentPeriod,
)
from app.schemas.user import UserResponse


class AmenityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    label: str
    icon: Optional[str] = None


class ListingPhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    listing_id: str
    url: str
    public_id: Optional[str] = None
    is_cover: bool = False
    sort_order: int = 0
    created_at: datetime


class ListingBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=300)
    description: Optional[str] = Field(None, max_length=5000)
    property_type: PropertyType = PropertyType.PG
    rent_amount: Decimal = Field(..., gt=0)
    deposit_amount: Optional[Decimal] = Field(None, ge=0)
    rent_period: RentPeriod = RentPeriod.MONTHLY
    address_line1: Optional[str] = Field(None, max_length=300)
    city: str = Field(..., min_length=2, max_length=100)
    locality: Optional[str] = Field(None, max_length=150)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=10)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    university_proximity: Optional[List[Dict[str, Any]]] = None
    gender_preference: GenderPreference = GenderPreference.ANY
    furnished_status: FurnishedStatus = FurnishedStatus.FURNISHED
    available_from: Optional[date] = None
    min_stay_months: int = Field(3, ge=1, le=36)
    max_occupancy: int = Field(1, ge=1, le=10)
    amenity_ids: Optional[List[int]] = []


class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=300)
    description: Optional[str] = Field(None, max_length=5000)
    property_type: Optional[PropertyType] = None
    rent_amount: Optional[Decimal] = Field(None, gt=0)
    deposit_amount: Optional[Decimal] = Field(None, ge=0)
    rent_period: Optional[RentPeriod] = None
    address_line1: Optional[str] = Field(None, max_length=300)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    locality: Optional[str] = Field(None, max_length=150)
    state: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, max_length=10)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    university_proximity: Optional[List[Dict[str, Any]]] = None
    gender_preference: Optional[GenderPreference] = None
    furnished_status: Optional[FurnishedStatus] = None
    available_from: Optional[date] = None
    min_stay_months: Optional[int] = Field(None, ge=1, le=36)
    max_occupancy: Optional[int] = Field(None, ge=1, le=10)
    status: Optional[ListingStatus] = None
    amenity_ids: Optional[List[int]] = None


class ListingStatusUpdate(BaseModel):
    status: ListingStatus


class ListingRejectRequest(BaseModel):
    reason: str = Field(..., min_length=3, max_length=500)


class ListingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    landlord_id: str
    title: str
    description: Optional[str] = None
    property_type: str
    rent_amount: Decimal
    deposit_amount: Optional[Decimal] = None
    rent_period: str
    address_line1: Optional[str] = None
    city: str
    locality: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    university_proximity: Optional[Any] = None
    gender_preference: str
    furnished_status: str
    available_from: Optional[date] = None
    min_stay_months: int
    max_occupancy: int
    status: str
    rejection_reason: Optional[str] = None
    is_featured: bool
    views_count: int
    created_at: datetime
    updated_at: datetime

    landlord: Optional[UserResponse] = None
    photos: List[ListingPhotoResponse] = []
    amenities: List[AmenityResponse] = []


class PaginatedListingsResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    items: List[ListingResponse]
