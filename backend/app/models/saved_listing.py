from datetime import datetime, timezone
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class SavedListing(Base):
    __tablename__ = "saved_listings"

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )
    listing_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("listings.id", ondelete="CASCADE"),
        primary_key=True,
        index=True
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "listing_id"),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], lazy="selectin")
    listing: Mapped["Listing"] = relationship("Listing", foreign_keys=[listing_id], lazy="selectin")
