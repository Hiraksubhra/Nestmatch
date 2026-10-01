import uuid
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.listing import Listing


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"


class BookingRequest(Base):
    __tablename__ = "booking_requests"

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
    student_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    landlord_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    move_in_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    duration_months: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default=BookingStatus.PENDING.value,
        nullable=False
    )
    message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    responded_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
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
    listing: Mapped["Listing"] = relationship("Listing", foreign_keys=[listing_id])
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
    landlord: Mapped["User"] = relationship("User", foreign_keys=[landlord_id])
