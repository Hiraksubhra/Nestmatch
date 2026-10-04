import uuid
from datetime import datetime, timezone, date
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Any
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Date,
    Numeric,
    Integer,
    Text,
    ForeignKey,
    JSON,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.spatial import GeoPoint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class PropertyType(str, Enum):
    PG = "PG"
    APARTMENT = "APARTMENT"
    SHARED_ROOM = "SHARED_ROOM"
    STUDIO = "STUDIO"


class GenderPreference(str, Enum):
    ANY = "ANY"
    MALE = "MALE"
    FEMALE = "FEMALE"


class FurnishedStatus(str, Enum):
    FURNISHED = "FURNISHED"
    SEMI = "SEMI"
    UNFURNISHED = "UNFURNISHED"


class ListingStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"
    REJECTED = "REJECTED"


class RentPeriod(str, Enum):
    MONTHLY = "MONTHLY"
    SEMESTER = "SEMESTER"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    YEARLY = "YEARLY"


# Association table for Listing <-> Amenity Many-to-Many
listing_amenities = Table(
    "listing_amenities",
    Base.metadata,
    Column("listing_id", String(36), ForeignKey("listings.id", ondelete="CASCADE"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenities.id", ondelete="CASCADE"), primary_key=True),
)


class Amenity(Base):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    listings: Mapped[List["Listing"]] = relationship(
        "Listing",
        secondary=listing_amenities,
        back_populates="amenities",
        lazy="selectin",
    )


class ListingPhoto(Base):
    __tablename__ = "listing_photos"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    listing_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("listings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    public_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_cover: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    listing: Mapped["Listing"] = relationship("Listing", back_populates="photos")


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    landlord_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    property_type: Mapped[str] = mapped_column(String(50), nullable=False, default=PropertyType.PG.value)
    rent_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    deposit_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    rent_period: Mapped[str] = mapped_column(String(20), default=RentPeriod.MONTHLY.value, nullable=False)
    address_line1: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    city: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    locality: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    location: Mapped[Optional[Any]] = mapped_column(GeoPoint, nullable=True)
    university_proximity: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    gender_preference: Mapped[str] = mapped_column(String(20), default=GenderPreference.ANY.value, nullable=False)
    furnished_status: Mapped[str] = mapped_column(String(20), default=FurnishedStatus.FURNISHED.value, nullable=False)
    available_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    min_stay_months: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    max_occupancy: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default=ListingStatus.PENDING_VERIFICATION.value, index=True, nullable=False)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    landlord: Mapped["User"] = relationship("User", foreign_keys=[landlord_id], lazy="selectin")
    photos: Mapped[List[ListingPhoto]] = relationship(
        "ListingPhoto",
        back_populates="listing",
        cascade="all, delete-orphan",
        order_by="ListingPhoto.sort_order",
        lazy="selectin",
    )
    amenities: Mapped[List[Amenity]] = relationship(
        "Amenity",
        secondary=listing_amenities,
        back_populates="listings",
        lazy="selectin",
    )
