import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.core.security import decode_token
from app.models.user import User
from app.models.message import MessageType
from app.schemas.message import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from app.schemas.user import UserResponse
from app.schemas.listing import ListingResponse
from app.services.messaging_service import MessagingService, manager
from app.services.auth_service import AuthService
from app.core.exceptions import (
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["Messaging"])


def serialize_conversation_item(item: dict) -> dict:
    conv = item["conversation"]
    last_msg = item["last_message"]
    unread = item["unread_count"]

    return {
        "id": conv.id,
        "listing_id": conv.listing_id,
        "student_id": conv.student_id,
        "landlord_id": conv.landlord_id,
        "status": conv.status,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
        "student": UserResponse.model_validate(conv.student).model_dump() if conv.student else None,
        "landlord": UserResponse.model_validate(conv.landlord).model_dump() if conv.landlord else None,
        "listing": ListingResponse.model_validate(conv.listing).model_dump() if conv.listing else None,
        "last_message": MessageResponse.model_validate(last_msg).model_dump() if last_msg else None,
        "unread_count": unread
    }


@router.get("", status_code=status.HTTP_200_OK, summary="List user's conversations")
async def list_conversations(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    items = await MessagingService.list_user_conversations(session, current_user.id)
    return {
        "success": True,
        "data": [serialize_conversation_item(item) for item in items]
    }


@router.post("", status_code=status.HTTP_201_CREATED, summary="Start or get conversation")
async def start_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    conv = await MessagingService.get_or_create_conversation(
        session=session,
        student_id=current_user.id,
        listing_id=data.listing_id,
        landlord_id=data.landlord_id,
        initial_message=data.initial_message
    )
    last_msg = conv.messages[-1] if conv.messages else None
    return {
        "success": True,
        "data": serialize_conversation_item({
            "conversation": conv,
            "last_message": last_msg,
            "unread_count": 0
        })
    }


@router.get("/{conversation_id}", status_code=status.HTTP_200_OK, summary="Get conversation detail")
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    conv = await MessagingService.get_conversation_by_id(session, conversation_id, current_user.id)
    last_msg = conv.messages[-1] if conv.messages else None
    unread = sum(1 for m in conv.messages if not m.is_read and m.sender_id != current_user.id)

    return {
        "success": True,
        "data": serialize_conversation_item({
            "conversation": conv,
            "last_message": last_msg,
            "unread_count": unread
        })
    }


@router.get("/{conversation_id}/messages", status_code=status.HTTP_200_OK, summary="Get message history")
async def get_messages(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    messages = await MessagingService.get_messages(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
    return {
        "success": True,
        "data": [
            {
                "id": m.id,
                "conversation_id": m.conversation_id,
                "sender_id": m.sender_id,
                "content": m.content,
                "message_type": m.message_type,
                "is_read": m.is_read,
                "created_at": m.created_at,
                "sender": UserResponse.model_validate(m.sender).model_dump() if m.sender else None
            }
            for m in messages
        ]
    }


@router.post("/{conversation_id}/messages", status_code=status.HTTP_201_CREATED, summary="Send message")
async def send_message(
    conversation_id: str,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    msg = await MessagingService.send_message(
        session=session,
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=data.content,
        message_type=data.message_type
    )
    return {
        "success": True,
        "data": {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "sender_id": msg.sender_id,
            "content": msg.content,
            "message_type": msg.message_type,
            "is_read": msg.is_read,
            "created_at": msg.created_at,
            "sender": UserResponse.model_validate(msg.sender).model_dump() if msg.sender else None
        }
    }


@router.put("/{conversation_id}/read", status_code=status.HTTP_200_OK, summary="Mark messages as read")
async def mark_messages_read(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    count = await MessagingService.mark_messages_read(session, conversation_id, current_user.id)
    return {
        "success": True,
        "data": {"marked_read_count": count}
    }


@router.websocket("/ws/{conversation_id}")
async def websocket_chat(
    websocket: WebSocket,
    conversation_id: str,
    token: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_db)
):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user = await AuthService.get_by_id(session, user_id=user_id)
        if not user or not user.is_active:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Check participant
        await MessagingService.get_conversation_by_id(session, conversation_id, user.id)
    except Exception as e:
        logger.warning(f"[WS] Auth failed for conversation {conversation_id}: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(conversation_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")

            if action == "SEND_MESSAGE":
                content = data.get("content", "").strip()
                if content:
                    await MessagingService.send_message(
                        session=session,
                        conversation_id=conversation_id,
                        sender_id=user.id,
                        content=content,
                        message_type=MessageType.TEXT.value
                    )
            elif action == "MARK_READ":
                await MessagingService.mark_messages_read(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=user.id
                )
            elif action == "TYPING":
                await manager.broadcast(conversation_id, {
                    "type": "TYPING",
                    "user_id": user.id,
                    "is_typing": bool(data.get("is_typing", True))
                })
    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)
    except Exception as e:
        logger.error(f"[WS] Unexpected error in conversation {conversation_id}: {e}")
        manager.disconnect(conversation_id, websocket)
