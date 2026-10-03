from typing import List, Dict, Any
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.report import UserReport, ReportReason, ReportStatus
from app.schemas.report import ReportCreateRequest, ReportReasonItem
from app.core.exceptions import BadRequestException, NotFoundException


REPORT_REASONS_METADATA: List[Dict[str, str]] = [
    {
        "key": ReportReason.INAPPROPRIATE_BEHAVIOUR.value,
        "label": "Inappropriate Behaviour",
        "description": "Rude, abusive, obscene language or inappropriate conduct.",
    },
    {
        "key": ReportReason.HARASSMENT.value,
        "label": "Harassment or Bullying",
        "description": "Threatening communication, intimidation, or persistent unwanted contact.",
    },
    {
        "key": ReportReason.FRAUD_OR_SCAM.value,
        "label": "Scam or Fraudulent Activity",
        "description": "Demanding cash deposits outside the platform, fake bank details, or deceptive charges.",
    },
    {
        "key": ReportReason.MISLEADING_OR_FAKE.value,
        "label": "Misleading or Fake Profile / Listing",
        "description": "Impersonation, fabricated credentials, fake listing photos, or inaccurate terms.",
    },
    {
        "key": ReportReason.SPAM.value,
        "label": "Spam or Advertising",
        "description": "Unsolicited promotional advertisements, commercial spam, or suspicious phishing links.",
    },
    {
        "key": ReportReason.OTHER.value,
        "label": "Other Safety Violation",
        "description": "Any other suspicious activity or concern violating community trust.",
    },
]


class ReportService:
    @staticmethod
    def get_reasons() -> List[ReportReasonItem]:
        """
        Return the list of standard report reasons with user-friendly descriptions.
        """
        return [ReportReasonItem(**item) for item in REPORT_REASONS_METADATA]

    @staticmethod
    async def create_report(
        session: AsyncSession,
        reporter: User,
        data: ReportCreateRequest,
    ) -> UserReport:
        """
        Create a new report flagging a student or landlord for inappropriate behaviour.
        """
        # Validate that the reporter is not reporting themselves
        if reporter.id == data.reported_user_id:
            raise BadRequestException(
                message="You cannot report your own profile.",
                code="CANNOT_REPORT_SELF"
            )

        # Validate that the reported user exists
        reported_user = await session.get(User, data.reported_user_id)
        if not reported_user:
            raise NotFoundException(
                message="The user you are trying to report does not exist.",
                code="USER_NOT_FOUND"
            )

        # Check for existing pending report by same reporter for this user
        stmt = (
            select(UserReport)
            .where(
                and_(
                    UserReport.reporter_id == reporter.id,
                    UserReport.reported_user_id == data.reported_user_id,
                    UserReport.status == ReportStatus.PENDING.value,
                )
            )
        )
        result = await session.execute(stmt)
        existing_report = result.scalars().first()

        if existing_report:
            raise BadRequestException(
                message="You have already submitted a pending report for this user. Our team is currently reviewing it.",
                code="REPORT_ALREADY_PENDING"
            )

        reason_str = data.reason.value if hasattr(data.reason, "value") else str(data.reason)

        new_report = UserReport(
            reporter_id=reporter.id,
            reported_user_id=data.reported_user_id,
            reason=reason_str,
            details=data.details.strip() if data.details else None,
            status=ReportStatus.PENDING.value,
        )

        session.add(new_report)
        await session.commit()
        await session.refresh(new_report)
        return new_report
