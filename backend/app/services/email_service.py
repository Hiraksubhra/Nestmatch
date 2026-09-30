import logging
from typing import Optional

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def send_new_message_notification(
        self,
        recipient_email: str,
        sender_name: str,
        message_preview: str,
        conversation_id: str
    ) -> bool:
        logger.info(
            f"[Email Notification] New message for {recipient_email} from {sender_name}: '{message_preview[:50]}...' (Conv: {conversation_id})"
        )
        return True

    async def send_booking_request_notification(
        self,
        landlord_email: str,
        student_name: str,
        listing_title: str,
        booking_id: str
    ) -> bool:
        logger.info(
            f"[Email Notification] New booking request for landlord {landlord_email} from {student_name} on listing '{listing_title}' (Booking: {booking_id})"
        )
        return True

    async def send_booking_status_notification(
        self,
        student_email: str,
        listing_title: str,
        status: str,
        landlord_name: str
    ) -> bool:
        logger.info(
            f"[Email Notification] Booking {status} notification sent to {student_email} for listing '{listing_title}' by {landlord_name}"
        )
        return True


email_service = EmailService()
