import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class ReportReason(str, Enum):
    INAPPROPRIATE_BEHAVIOUR = "INAPPROPRIATE_BEHAVIOUR"
    HARASSMENT = "HARASSMENT"
    FRAUD_OR_SCAM = "FRAUD_OR_SCAM"
    MISLEADING_OR_FAKE = "MISLEADING_OR_FAKE"
    SPAM = "SPAM"
    OTHER = "OTHER"


class ReportStatus(str, Enum):
    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"


class UserReport(Base):
    __tablename__ = "user_reports"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    reporter_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    reported_user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    reason: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    details: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20),
        default=ReportStatus.PENDING.value,
        nullable=False,
        index=True
    )
    # Administrative tracking fields reserved for future admin capabilities
    admin_notes: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    action_taken: Mapped[Optional[str]] = mapped_column(
        String(50),
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
    reporter = relationship("User", foreign_keys=[reporter_id], backref="reports_submitted")
    reported_user = relationship("User", foreign_keys=[reported_user_id], backref="reports_received")
