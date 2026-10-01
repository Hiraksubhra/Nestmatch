import uuid
from datetime import datetime, timezone, date
from decimal import Decimal
from typing import Optional, List, Any
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Date,
    Numeric,
    Integer,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class FlatmateProfile(Base):
    __tablename__ = "flatmate_profiles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    budget_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    budget_max: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    preferred_city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    preferred_university: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    preferred_locality: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    move_in_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    move_in_flexibility: Mapped[int] = mapped_column(Integer, default=7, nullable=False)  # in days
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String(280), nullable=True)
    lifestyle_tags: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
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
    user: Mapped["User"] = relationship("User", lazy="selectin")
