from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Bad request",
        code: str = "BAD_REQUEST",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Could not validate credentials",
        code: str = "UNAUTHORIZED",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "You do not have permission to access this resource",
        code: str = "FORBIDDEN",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource already exists",
        code: str = "CONFLICT",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


def format_error_response(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {}
        }
    }


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(exc.code, exc.message, exc.details)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(p) for p in err.get("loc", [])])
        errors.append({"field": loc, "message": err.get("msg")})

    detail_msg = "; ".join([f"{e['field']}: {e['message']}" for e in errors])
    print(f"[ValidationError] {detail_msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=format_error_response(
            code="VALIDATION_ERROR",
            message=f"Invalid request data: {detail_msg}",
            details={"validation_errors": errors}
        )
    )
