from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, RefreshTokenRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    """
    Register a new user (Student or Landlord).
    Generates access and refresh tokens upon successful creation.
    """
    user = await AuthService.register(session, user_in)
    token_response = AuthService.generate_token_response(user)
    return {
        "success": True,
        "message": "User registered successfully",
        "data": token_response.model_dump()
    }


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Log in with email and password"
)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and issue JWT access and refresh tokens.
    """
    user = await AuthService.authenticate(
        session,
        email=credentials.email,
        password=credentials.password
    )
    token_response = AuthService.generate_token_response(user)
    return {
        "success": True,
        "message": "Login successful",
        "data": token_response.model_dump()
    }


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token"
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_db)
):
    """
    Use a valid refresh token to obtain a new access & refresh token pair.
    """
    token_response = await AuthService.refresh(session, refresh_data.refresh_token)
    return {
        "success": True,
        "data": token_response.model_dump()
    }


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user"
)
async def logout():
    """
    Stateless JWT logout endpoint. In v1, clients discard their stored tokens.
    """
    return {
        "success": True,
        "message": "Logged out successfully"
    }
