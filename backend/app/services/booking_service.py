import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.booking import BookingRequest, BookingStatus
from app.models.listing import Listing, ListingPhoto, ListingStatus
from app.models.user import User, UserRole
from app.models.message import Conversation, ConversationStatus
from app.schemas.booking import BookingRequestCreate
from app.services.messaging_service import MessagingService
from app.services.email_service import email_service
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException,
    ConflictException,
)

logger = logging.getLogger(__name__)


def format_booking_response(booking: BookingRequest, current_user_id: Optional[str] = None) -> Dict[str, Any]:
    # Format contacts: Revealed ONLY if status == ACCEPTED
    landlord_contact = None
    student_contact = None

    if booking.status == BookingStatus.ACCEPTED.value:
        if booking.landlord:
            landlord_contact = {
                "full_name": booking.landlord.full_name,
                "email": booking.landlord.email,
                "phone": booking.landlord.phone or "Not provided"
            }
        if booking.student:
            student_contact = {
                "full_name": booking.student.full_name,
                "email": booking.student.email,
                "phone": booking.student.phone or "Not provided"
            }

    return {
        "id": booking.id,
        "listing_id": booking.listing_id,
        "student_id": booking.student_id,
        "landlord_id": booking.landlord_id,
        "move_in_date": booking.move_in_date,
        "duration_months": booking.duration_months,
        "status": booking.status,
        "message": booking.message,
        "responded_at": booking.responded_at,
        "created_at": booking.created_at,
        "updated_at": booking.updated_at,
        "student": booking.student,
        "landlord": booking.landlord,
        "listing": booking.listing,
        "landlord_contact": landlord_contact,
        "student_contact": student_contact
    }


class BookingService:
    @staticmethod
    async def create_booking_request(
        session: AsyncSession,
        student: User,
        data: BookingRequestCreate
    ) -> Dict[str, Any]:
        # Validate listing
        listing_stmt = select(Listing).where(Listing.id == data.listing_id).options(
            selectinload(Listing.photos)
        )
        res = await session.execute(listing_stmt)
        listing = res.scalar_one_or_none()
        if not listing:
            raise NotFoundException("Listing not found", "LISTING_NOT_FOUND")

        if listing.status != ListingStatus.ACTIVE.value:
            raise BadRequestException("Listing is not available for booking", "LISTING_NOT_AVAILABLE")

        if listing.landlord_id == student.id:
            raise BadRequestException("You cannot request to book your own listing", "SELF_BOOKING")

        # Check existing pending booking
        existing_stmt = select(BookingRequest).where(
            and_(
                BookingRequest.listing_id == data.listing_id,
                BookingRequest.student_id == student.id,
                BookingRequest.status == BookingStatus.PENDING.value
            )
        )
        existing = (await session.execute(existing_stmt)).scalar_one_or_none()
        if existing:
            raise ConflictException("You already have a pending booking request for this listing", "PENDING_REQUEST_EXISTS")

        booking = BookingRequest(
            listing_id=data.listing_id,
            student_id=student.id,
            landlord_id=listing.landlord_id,
            move_in_date=data.move_in_date,
            duration_months=data.duration_months,
            message=data.message,
            status=BookingStatus.PENDING.value
        )
        session.add(booking)
        await session.commit()
        await session.refresh(booking)

        # Get or create conversation thread and add system note
        conv = await MessagingService.get_or_create_conversation(
            session=session,
            student_id=student.id,
            listing_id=listing.id,
            landlord_id=listing.landlord_id
        )
        sys_msg = (
            f"📅 New Booking Request:\n"
            f"• Move-in Date: {data.move_in_date}\n"
            f"• Duration: {data.duration_months} month(s)\n"
            f"• Status: PENDING\n"
        )
        if data.message:
            sys_msg += f"• Note: \"{data.message}\""

        await MessagingService.inject_system_message(session, conv.id, sys_msg)

        # Send background email notification
        landlord_stmt = select(User).where(User.id == listing.landlord_id)
        landlord = (await session.execute(landlord_stmt)).scalar_one_or_none()
        if landlord:
            await email_service.send_booking_request_notification(
                landlord_email=landlord.email,
                student_name=student.full_name,
                listing_title=listing.title,
                booking_id=booking.id
            )

        return await BookingService.get_booking_by_id(session, booking.id, student.id, student.role)

    @staticmethod
    async def get_booking_by_id(
        session: AsyncSession,
        booking_id: str,
        user_id: str,
        role: str
    ) -> Dict[str, Any]:
        query = select(BookingRequest).where(BookingRequest.id == booking_id).options(
            selectinload(BookingRequest.student),
            selectinload(BookingRequest.landlord),
            selectinload(BookingRequest.listing).selectinload(Listing.photos)
        )
        result = await session.execute(query)
        booking = result.scalar_one_or_none()
        if not booking:
            raise NotFoundException("Booking request not found", "BOOKING_NOT_FOUND")

        if role != UserRole.ADMIN.value and booking.student_id != user_id and booking.landlord_id != user_id:
            raise ForbiddenException("You are not authorized to view this booking request", "FORBIDDEN")

        return format_booking_response(booking, user_id)

    @staticmethod
    async def list_bookings(
        session: AsyncSession,
        user_id: str,
        role: str,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = select(BookingRequest).options(
            selectinload(BookingRequest.student),
            selectinload(BookingRequest.landlord),
            selectinload(BookingRequest.listing).selectinload(Listing.photos)
        ).order_by(desc(BookingRequest.created_at))

        filters = []
        if role == UserRole.LANDLORD.value:
            filters.append(BookingRequest.landlord_id == user_id)
        elif role == UserRole.STUDENT.value:
            filters.append(BookingRequest.student_id == user_id)
        # Admin can view all or filtered by user_id

        if status:
            filters.append(BookingRequest.status == status.upper())

        if filters:
            query = query.where(and_(*filters))

        result = await session.execute(query)
        bookings = result.scalars().all()
        return [format_booking_response(b, user_id) for b in bookings]

    @staticmethod
    async def accept_booking(
        session: AsyncSession,
        booking_id: str,
        landlord_id: str
    ) -> Dict[str, Any]:
        stmt = select(BookingRequest).where(BookingRequest.id == booking_id).options(
            selectinload(BookingRequest.student),
            selectinload(BookingRequest.landlord),
            selectinload(BookingRequest.listing).selectinload(Listing.photos)
        )
        booking = (await session.execute(stmt)).scalar_one_or_none()
        if not booking:
            raise NotFoundException("Booking request not found", "BOOKING_NOT_FOUND")

        if booking.landlord_id != landlord_id:
            raise ForbiddenException("Only the listing landlord can accept this request", "FORBIDDEN")

        if booking.status != BookingStatus.PENDING.value:
            raise BadRequestException(f"Cannot accept booking in '{booking.status}' status", "INVALID_STATUS")

        booking.status = BookingStatus.ACCEPTED.value
        booking.responded_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(booking)

        # Notify via conversation system message
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.listing_id == booking.listing_id,
                Conversation.student_id == booking.student_id
            )
        )
        conv = (await session.execute(conv_stmt)).scalar_one_or_none()
        if conv:
            conv.status = ConversationStatus.BOOKED.value
            await session.commit()
            await MessagingService.inject_system_message(
                session,
                conv.id,
                "🎉 Booking Request Accepted! Contact details and move-in information are now confirmed and unlocked."
            )

        # Email notification
        if booking.student:
            await email_service.send_booking_status_notification(
                student_email=booking.student.email,
                listing_title=booking.listing.title if booking.listing else "Listing",
                status="ACCEPTED",
                landlord_name=booking.landlord.full_name if booking.landlord else "Landlord"
            )

        return format_booking_response(booking, landlord_id)

    @staticmethod
    async def decline_booking(
        session: AsyncSession,
        booking_id: str,
        landlord_id: str
    ) -> Dict[str, Any]:
        stmt = select(BookingRequest).where(BookingRequest.id == booking_id).options(
            selectinload(BookingRequest.student),
            selectinload(BookingRequest.landlord),
            selectinload(BookingRequest.listing).selectinload(Listing.photos)
        )
        booking = (await session.execute(stmt)).scalar_one_or_none()
        if not booking:
            raise NotFoundException("Booking request not found", "BOOKING_NOT_FOUND")

        if booking.landlord_id != landlord_id:
            raise ForbiddenException("Only the listing landlord can decline this request", "FORBIDDEN")

        if booking.status != BookingStatus.PENDING.value:
            raise BadRequestException(f"Cannot decline booking in '{booking.status}' status", "INVALID_STATUS")

        booking.status = BookingStatus.DECLINED.value
        booking.responded_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(booking)

        # Notify via conversation
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.listing_id == booking.listing_id,
                Conversation.student_id == booking.student_id
            )
        )
        conv = (await session.execute(conv_stmt)).scalar_one_or_none()
        if conv:
            await MessagingService.inject_system_message(
                session,
                conv.id,
                "❌ Landlord declined the booking request."
            )

        # Email notification
        if booking.student:
            await email_service.send_booking_status_notification(
                student_email=booking.student.email,
                listing_title=booking.listing.title if booking.listing else "Listing",
                status="DECLINED",
                landlord_name=booking.landlord.full_name if booking.landlord else "Landlord"
            )

        return format_booking_response(booking, landlord_id)

    @staticmethod
    async def cancel_booking(
        session: AsyncSession,
        booking_id: str,
        student_id: str
    ) -> Dict[str, Any]:
        stmt = select(BookingRequest).where(BookingRequest.id == booking_id).options(
            selectinload(BookingRequest.student),
            selectinload(BookingRequest.landlord),
            selectinload(BookingRequest.listing).selectinload(Listing.photos)
        )
        booking = (await session.execute(stmt)).scalar_one_or_none()
        if not booking:
            raise NotFoundException("Booking request not found", "BOOKING_NOT_FOUND")

        if booking.student_id != student_id:
            raise ForbiddenException("Only the requesting student can cancel this booking", "FORBIDDEN")

        if booking.status != BookingStatus.PENDING.value:
            raise BadRequestException(f"Cannot cancel booking in '{booking.status}' status", "INVALID_STATUS")

        booking.status = BookingStatus.CANCELLED.value
        booking.responded_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(booking)

        # Notify via conversation
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.listing_id == booking.listing_id,
                Conversation.student_id == booking.student_id
            )
        )
        conv = (await session.execute(conv_stmt)).scalar_one_or_none()
        if conv:
            await MessagingService.inject_system_message(
                session,
                conv.id,
                "ℹ️ Student cancelled the booking request."
            )

        return format_booking_response(booking, student_id)
