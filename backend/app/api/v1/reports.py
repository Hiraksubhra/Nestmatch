from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.report import (
    ReportCreateRequest,
    ReportResponse,
    ReportReasonsResponse,
)
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get(
    "/reasons",
    status_code=status.HTTP_200_OK,
    summary="Get available report reasons with descriptions"
)
async def get_report_reasons():
    """
    Retrieve the standard categorized reasons for reporting users.
    """
    reasons = ReportService.get_reasons()
    return {
        "success": True,
        "data": [r.model_dump() for r in reasons]
    }


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Report a student or landlord for inappropriate behaviour"
)
async def submit_report(
    data: ReportCreateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Submit a report flagging a user for inappropriate conduct, fraud, harassment, or scam.
    """
    report = await ReportService.create_report(session, current_user, data)
    return {
        "success": True,
        "message": "Report submitted successfully. Our team will review this report promptly.",
        "data": ReportResponse.model_validate(report).model_dump()
    }
