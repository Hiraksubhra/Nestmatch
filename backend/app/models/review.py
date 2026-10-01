import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Integer,
    Text,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

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
    reviewer_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    title: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True
    )
    body: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
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

    __table_args__ = (
        UniqueConstraint("listing_id", "reviewer_id", name="uq_listing_reviewer"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range"),
    )

    # Relationships
    reviewer: Mapped["User"] = relationship("User", foreign_keys=[reviewer_id], lazy="selectin")
    listing: Mapped["Listing"] = relationship("Listing", foreign_keys=[listing_id], lazy="selectin")
