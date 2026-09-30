from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import bcrypt
from jose import jwt, JWTError
from app.core.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def create_token(
    data: Dict[str, Any],
    expires_delta: timedelta,
    token_type: str = "access"
) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": token_type
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(
    subject: str,
    extra_claims: Optional[Dict[str, Any]] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {"sub": subject}
    if extra_claims:
        claims.update(extra_claims)
    return create_token(claims, expires_delta, token_type="access")


def create_refresh_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token({"sub": subject}, expires_delta, token_type="refresh")


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
