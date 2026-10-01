import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict
from fastapi import WebSocket
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.message import (
    Conversation,
    Message,
    MessageType,
    ConversationStatus,
)
from app.models.user import User
from app.models.listing import Listing, ListingPhoto
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        # Map conversation_id -> list of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, conversation_id: str, websocket: WebSocket):
        await websocket.accept()
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []
        self.active_connections[conversation_id].append(websocket)
        logger.info(f"[WS] Client connected to conversation {conversation_id}. Total: {len(self.active_connections[conversation_id])}")

    def disconnect(self, conversation_id: str, websocket: WebSocket):
        if conversation_id in self.active_connections:
            if websocket in self.active_connections[conversation_id]:
                self.active_connections[conversation_id].remove(websocket)
            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]
        logger.info(f"[WS] Client disconnected from conversation {conversation_id}.")

    async def broadcast(self, conversation_id: str, data: dict):
        if conversation_id in self.active_connections:
            disconnected = []
            for ws in self.active_connections[conversation_id]:
                try:
                    await ws.send_json(data)
                except Exception as e:
                    logger.warning(f"[WS] Error sending message: {e}")
                    disconnected.append(ws)
            for ws in disconnected:
                self.disconnect(conversation_id, ws)


manager = ConnectionManager()


class MessagingService:
    @staticmethod
    async def get_or_create_conversation(
        session: AsyncSession,
        student_id: str,
        listing_id: Optional[str] = None,
        landlord_id: Optional[str] = None,
        initial_message: Optional[str] = None,
    ) -> Conversation:
        # If listing_id provided, look up listing and its landlord
        if listing_id:
            listing_stmt = select(Listing).where(Listing.id == listing_id)
            res = await session.execute(listing_stmt)
            listing = res.scalar_one_or_none()
            if not listing:
                raise NotFoundException("Listing not found", "LISTING_NOT_FOUND")
            landlord_id = listing.landlord_id

            if student_id == landlord_id:
                raise BadRequestException("You cannot start a conversation with yourself", "SELF_CONVERSATION")

            # Check if conversation already exists for (listing_id, student_id)
            query = select(Conversation).where(
                and_(
                    Conversation.listing_id == listing_id,
                    Conversation.student_id == student_id
                )
            ).options(
                selectinload(Conversation.student),
                selectinload(Conversation.landlord),
                selectinload(Conversation.listing).selectinload(Listing.photos),
                selectinload(Conversation.messages)
            )
            result = await session.execute(query)
            conv = result.scalar_one_or_none()
            if conv:
                if initial_message:
                    await MessagingService.send_message(session, conv.id, student_id, initial_message)
                return conv
        else:
            if not landlord_id:
                raise BadRequestException("Either listing_id or landlord_id must be provided", "INVALID_ARGUMENTS")
            if student_id == landlord_id:
                raise BadRequestException("You cannot start a conversation with yourself", "SELF_CONVERSATION")

            # Check if conversation exists without listing
            query = select(Conversation).where(
                and_(
                    Conversation.listing_id.is_(None),
                    Conversation.student_id == student_id,
                    Conversation.landlord_id == landlord_id
                )
            ).options(
                selectinload(Conversation.student),
                selectinload(Conversation.landlord),
                selectinload(Conversation.messages)
            )
            result = await session.execute(query)
            conv = result.scalar_one_or_none()
            if conv:
                if initial_message:
                    await MessagingService.send_message(session, conv.id, student_id, initial_message)
                return conv

        # Create new conversation
        new_conv = Conversation(
            listing_id=listing_id,
            student_id=student_id,
            landlord_id=landlord_id,
            status=ConversationStatus.OPEN.value,
        )
        session.add(new_conv)
        await session.commit()
        await session.refresh(new_conv)

        if initial_message:
            await MessagingService.send_message(session, new_conv.id, student_id, initial_message)

        return await MessagingService.get_conversation_by_id(session, new_conv.id, student_id)

    @staticmethod
    async def get_conversation_by_id(
        session: AsyncSession,
        conversation_id: str,
        user_id: str
    ) -> Conversation:
        query = select(Conversation).where(Conversation.id == conversation_id).options(
            selectinload(Conversation.student),
            selectinload(Conversation.landlord),
            selectinload(Conversation.listing).selectinload(Listing.photos),
            selectinload(Conversation.messages).selectinload(Message.sender)
        )
        result = await session.execute(query)
        conv = result.scalar_one_or_none()
        if not conv:
            raise NotFoundException("Conversation not found", "CONVERSATION_NOT_FOUND")

        if conv.student_id != user_id and conv.landlord_id != user_id:
            raise ForbiddenException("You are not a participant in this conversation", "FORBIDDEN")

        return conv

    @staticmethod
    async def list_user_conversations(
        session: AsyncSession,
        user_id: str
    ) -> List[Dict]:
        query = select(Conversation).where(
            or_(
                Conversation.student_id == user_id,
                Conversation.landlord_id == user_id
            )
        ).options(
            selectinload(Conversation.student),
            selectinload(Conversation.landlord),
            selectinload(Conversation.listing).selectinload(Listing.photos),
            selectinload(Conversation.messages).selectinload(Message.sender)
        ).order_by(desc(Conversation.updated_at))

        result = await session.execute(query)
        conversations = result.scalars().all()

        results = []
        for conv in conversations:
            messages = conv.messages
            last_message = messages[-1] if messages else None
            # count unread messages sent by the other party
            unread_count = sum(1 for m in messages if not m.is_read and m.sender_id != user_id)

            results.append({
                "conversation": conv,
                "last_message": last_message,
                "unread_count": unread_count
            })

        return results

    @staticmethod
    async def get_messages(
        session: AsyncSession,
        conversation_id: str,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        # Validate participation
        await MessagingService.get_conversation_by_id(session, conversation_id, user_id)

        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).options(
            selectinload(Message.sender)
        ).order_by(Message.created_at.asc()).offset(offset).limit(limit)

        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def send_message(
        session: AsyncSession,
        conversation_id: str,
        sender_id: str,
        content: str,
        message_type: str = MessageType.TEXT.value
    ) -> Message:
        # Verify sender is participant or system
        conv_stmt = select(Conversation).where(Conversation.id == conversation_id)
        conv_res = await session.execute(conv_stmt)
        conv = conv_res.scalar_one_or_none()
        if not conv:
            raise NotFoundException("Conversation not found", "CONVERSATION_NOT_FOUND")

        if message_type != MessageType.SYSTEM.value and conv.student_id != sender_id and conv.landlord_id != sender_id:
            raise ForbiddenException("You are not authorized to send messages in this conversation", "FORBIDDEN")

        msg = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content.strip(),
            message_type=message_type,
            is_read=False,
            created_at=datetime.now(timezone.utc)
        )
        session.add(msg)

        # Update conversation's updated_at
        conv.updated_at = datetime.now(timezone.utc)
        await session.commit()

        # Eager load sender for response
        msg_stmt = select(Message).where(Message.id == msg.id).options(selectinload(Message.sender))
        msg_loaded = (await session.execute(msg_stmt)).scalar_one()

        # Broadcast via WebSocket manager
        broadcast_payload = {
            "type": "NEW_MESSAGE",
            "message": {
                "id": msg_loaded.id,
                "conversation_id": msg_loaded.conversation_id,
                "sender_id": msg_loaded.sender_id,
                "content": msg_loaded.content,
                "message_type": msg_loaded.message_type,
                "is_read": msg_loaded.is_read,
                "created_at": msg_loaded.created_at.isoformat(),
                "sender": {
                    "id": msg_loaded.sender.id,
                    "full_name": msg_loaded.sender.full_name,
                    "avatar_url": msg_loaded.sender.avatar_url,
                    "role": msg_loaded.sender.role
                } if msg_loaded.sender else None
            }
        }
        await manager.broadcast(conversation_id, broadcast_payload)

        return msg_loaded

    @staticmethod
    async def mark_messages_read(
        session: AsyncSession,
        conversation_id: str,
        user_id: str
    ) -> int:
        conv = await MessagingService.get_conversation_by_id(session, conversation_id, user_id)
        
        # Select unread messages sent by the other party
        query = select(Message).where(
            and_(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.is_read.is_(False)
            )
        )
        res = await session.execute(query)
        unread_msgs = list(res.scalars().all())

        for msg in unread_msgs:
            msg.is_read = True

        if unread_msgs:
            await session.commit()
            # Broadcast read receipt
            await manager.broadcast(conversation_id, {
                "type": "MESSAGES_READ",
                "reader_id": user_id,
                "count": len(unread_msgs)
            })

        return len(unread_msgs)

    @staticmethod
    async def inject_system_message(
        session: AsyncSession,
        conversation_id: str,
        content: str
    ) -> Message:
        # System messages use landlord or student ID as sender or any participant, but marked as SYSTEM
        conv_stmt = select(Conversation).where(Conversation.id == conversation_id)
        conv_res = await session.execute(conv_stmt)
        conv = conv_res.scalar_one_or_none()
        if not conv:
            return None
        return await MessagingService.send_message(
            session=session,
            conversation_id=conversation_id,
            sender_id=conv.landlord_id,
            content=content,
            message_type=MessageType.SYSTEM.value
        )
