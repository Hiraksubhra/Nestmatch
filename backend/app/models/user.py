import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    LANDLORD = "LANDLORD"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    avatar_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )
    role: Mapped[str] = mapped_column(
        String(20),
        default=UserRole.STUDENT.value,
        nullable=False
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    is_shadow_banned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    shadow_banned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    shadow_ban_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    oauth_provider: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    oauth_id: Mapped[str] = mapped_column(
        String(255),
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
