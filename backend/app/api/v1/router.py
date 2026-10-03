from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.listings import router as listings_router
from app.api.v1.admin import router as admin_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.flatmates import router as flatmates_router
from app.api.v1.reports import router as reports_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(listings_router)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(conversations_router)
api_v1_router.include_router(bookings_router)
api_v1_router.include_router(flatmates_router)
api_v1_router.include_router(reports_router)

