import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Any
from sqlalchemy import String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.db.spatial import GeoPoint


class Campus(Base):
    __tablename__ = "campuses"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    short_name: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    locality: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False)

    # PostGIS Geography POINT(lng lat, 4326)
    location: Mapped[Optional[Any]] = mapped_column(GeoPoint, nullable=True)

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
