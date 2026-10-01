import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.booking import (
    BookingRequestCreate,
    BookingRequestResponse,
)
from app.schemas.user import UserResponse
from app.schemas.listing import ListingResponse
from app.services.booking_service import BookingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


def serialize_booking_dict(data: dict) -> dict:
    return {
        "id": data["id"],
        "listing_id": data["listing_id"],
        "student_id": data["student_id"],
        "landlord_id": data["landlord_id"],
        "move_in_date": data["move_in_date"].isoformat() if hasattr(data["move_in_date"], "isoformat") else data["move_in_date"],
        "duration_months": data["duration_months"],
        "status": data["status"],
        "message": data["message"],
        "responded_at": data["responded_at"],
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "student": UserResponse.model_validate(data["student"]).model_dump() if data.get("student") else None,
        "landlord": UserResponse.model_validate(data["landlord"]).model_dump() if data.get("landlord") else None,
        "listing": ListingResponse.model_validate(data["listing"]).model_dump() if data.get("listing") else None,
        "landlord_contact": data.get("landlord_contact"),
        "student_contact": data.get("student_contact")
    }


@router.post("", status_code=status.HTTP_201_CREATED, summary="Create booking request")
async def create_booking_request(
    data: BookingRequestCreate,
    current_user: User = Depends(require_role(UserRole.STUDENT.value)),
    session: AsyncSession = Depends(get_db)
):
    booking = await BookingService.create_booking_request(session, current_user, data)
    return {
        "success": True,
        "data": serialize_booking_dict(booking)
    }


@router.get("", status_code=status.HTTP_200_OK, summary="List my booking requests")
async def list_bookings(
    status_filter: Optional[str] = Query(None, alias="status", description="PENDING, ACCEPTED, DECLINED, CANCELLED"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    bookings = await BookingService.list_bookings(
        session=session,
        user_id=current_user.id,
        role=current_user.role,
        status=status_filter
    )
    return {
        "success": True,
        "data": [serialize_booking_dict(b) for b in bookings]
    }


@router.get("/{booking_id}", status_code=status.HTTP_200_OK, summary="Get booking detail")
async def get_booking(
    booking_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    booking = await BookingService.get_booking_by_id(
        session=session,
        booking_id=booking_id,
        user_id=current_user.id,
        role=current_user.role
    )
    return {
        "success": True,
        "data": serialize_booking_dict(booking)
    }


@router.put("/{booking_id}/accept", status_code=status.HTTP_200_OK, summary="Landlord accepts booking")
async def accept_booking(
    booking_id: str,
    current_user: User = Depends(require_role(UserRole.LANDLORD.value)),
    session: AsyncSession = Depends(get_db)
):
    booking = await BookingService.accept_booking(session, booking_id, current_user.id)
    return {
        "success": True,
        "data": serialize_booking_dict(booking)
    }


@router.put("/{booking_id}/decline", status_code=status.HTTP_200_OK, summary="Landlord declines booking")
async def decline_booking(
    booking_id: str,
    current_user: User = Depends(require_role(UserRole.LANDLORD.value)),
    session: AsyncSession = Depends(get_db)
):
    booking = await BookingService.decline_booking(session, booking_id, current_user.id)
    return {
        "success": True,
        "data": serialize_booking_dict(booking)
    }


@router.put("/{booking_id}/cancel", status_code=status.HTTP_200_OK, summary="Student cancels booking")
async def cancel_booking(
    booking_id: str,
    current_user: User = Depends(require_role(UserRole.STUDENT.value)),
    session: AsyncSession = Depends(get_db)
):
    booking = await BookingService.cancel_booking(session, booking_id, current_user.id)
    return {
        "success": True,
        "data": serialize_booking_dict(booking)
    }
