from typing import Callable
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    if not token:
        raise UnauthorizedException(
            message="Authentication credentials were not provided",
            code="NOT_AUTHENTICATED"
        )
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise UnauthorizedException(message="Invalid token type", code="INVALID_TOKEN")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException(message="Token payload invalid", code="INVALID_TOKEN")
    except Exception:
        raise UnauthorizedException(
            message="Could not validate credentials",
            code="INVALID_TOKEN"
        )

    user = await AuthService.get_by_id(session, user_id=user_id)
    if user is None:
        raise UnauthorizedException(message="User does not exist", code="USER_NOT_FOUND")
    if not user.is_active:
        raise UnauthorizedException(message="User account is deactivated", code="ACCOUNT_INACTIVE")

    return user


async def get_optional_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            return None
        user_id = payload.get("sub")
        if not user_id:
            return None
        user = await AuthService.get_by_id(session, user_id=user_id)
        if not user or not user.is_active:
            return None
        return user
    except Exception:
        return None


def require_role(*roles: str) -> Callable:
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenException(
                message=f"Action requires one of the following roles: {', '.join(roles)}",
                code="INSUFFICIENT_PERMISSIONS"
            )
        return current_user
    return role_checker

