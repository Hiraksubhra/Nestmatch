from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, TokenResponse, UserResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import ConflictException, UnauthorizedException, NotFoundException


class AuthService:
    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email.lower()))
        return result.scalars().first()

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @classmethod
    async def register(cls, session: AsyncSession, user_in: UserCreate) -> User:
        existing = await cls.get_by_email(session, user_in.email)
        if existing:
            raise ConflictException(
                message="An account with this email already exists",
                code="EMAIL_ALREADY_EXISTS"
            )

        hashed_pw = hash_password(user_in.password)
        db_user = User(
            email=user_in.email.lower(),
            password_hash=hashed_pw,
            full_name=user_in.full_name,
            role=user_in.role.value,
            phone=user_in.phone,
            is_active=True,
            is_verified=False,
        )
        session.add(db_user)
        await session.flush()
        await session.refresh(db_user)
        return db_user

    @classmethod
    async def authenticate(cls, session: AsyncSession, email: str, password: str) -> User:
        user = await cls.get_by_email(session, email)
        if not user or not user.password_hash:
            raise UnauthorizedException(
                message="Invalid email or password",
                code="INVALID_CREDENTIALS"
            )

        if not verify_password(password, user.password_hash):
            raise UnauthorizedException(
                message="Invalid email or password",
                code="INVALID_CREDENTIALS"
            )

        if not user.is_active:
            raise UnauthorizedException(
                message="Your account has been deactivated",
                code="ACCOUNT_INACTIVE"
            )

        return user

    @classmethod
    def generate_token_response(cls, user: User) -> TokenResponse:
        access_token = create_access_token(
            subject=user.id,
            extra_claims={"email": user.email, "role": user.role}
        )
        refresh_token = create_refresh_token(subject=user.id)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

    @classmethod
    async def refresh(cls, session: AsyncSession, refresh_token_str: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token_str)
            if payload.get("type") != "refresh":
                raise UnauthorizedException(message="Invalid token type", code="INVALID_TOKEN")
            user_id = payload.get("sub")
            if not user_id:
                raise UnauthorizedException(message="Token missing subject", code="INVALID_TOKEN")
        except Exception:
            raise UnauthorizedException(message="Invalid or expired refresh token", code="INVALID_TOKEN")

        user = await cls.get_by_id(session, user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(message="User not found or inactive", code="USER_NOT_FOUND")

        return cls.generate_token_response(user)

    @classmethod
    async def update_profile(cls, session: AsyncSession, user: User, update_data: UserUpdate) -> User:
        if update_data.full_name is not None:
            user.full_name = update_data.full_name
        if update_data.phone is not None:
            user.phone = update_data.phone
        if update_data.avatar_url is not None:
            user.avatar_url = update_data.avatar_url

        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user
