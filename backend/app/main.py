from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
)
from app.db.init_db import init_db
from app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # In development/test mode, auto-create database tables
    if settings.APP_ENV in ["development", "test"]:
        await init_db()
    yield


app = FastAPI(
    title="NestMatch API",
    description="Student-first housing platform API powering discovery, roommate matching, and verified listings.",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|172\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Custom Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Mount static files for local uploads fallback
import os
from fastapi.staticfiles import StaticFiles
static_dir = os.path.join(os.getcwd(), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API v1 Router
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    return {
        "success": True,
        "message": "Welcome to NestMatch API",
        "version": settings.VERSION
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.APP_ENV
    }
