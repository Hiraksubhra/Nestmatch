from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from app.models.report import ReportReason, ReportStatus


class ReportReasonItem(BaseModel):
    key: str
    label: str
    description: str


class ReportCreateRequest(BaseModel):
    reported_user_id: str = Field(..., min_length=1, max_length=36, description="ID of the user being reported")
    reason: ReportReason = Field(..., description="Categorized reason for reporting")
    details: Optional[str] = Field(None, max_length=1000, description="Additional context or details regarding the report")


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    reporter_id: str
    reported_user_id: str
    reason: str
    details: Optional[str] = None
    status: str
    created_at: datetime


class ReportReasonsResponse(BaseModel):
    reasons: List[ReportReasonItem]
