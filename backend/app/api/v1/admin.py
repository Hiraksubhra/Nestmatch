from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import require_role
from app.models.user import User, UserRole
from app.schemas.listing import (
    ListingResponse,
    ListingRejectRequest,
)
from app.services.listing_service import ListingService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get(
    "/listings/pending",
    status_code=status.HTTP_200_OK,
    summary="Get pending listings awaiting verification (Admin only)"
)
async def get_pending_listings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_role(UserRole.ADMIN.value)),
    session: AsyncSession = Depends(get_db)
):
    results = await ListingService.get_pending_listings(
        session=session,
        page=page,
        limit=limit,
    )
    items_data = [ListingResponse.model_validate(item).model_dump() for item in results["items"]]
    return {
        "success": True,
        "data": items_data,
        "meta": {
            "total": results["total"],
            "page": results["page"],
            "limit": results["limit"],
            "pages": results["pages"],
        }
    }


@router.put(
    "/listings/{listing_id}/approve",
    status_code=status.HTTP_200_OK,
    summary="Approve listing (Admin only)"
)
async def approve_listing(
    listing_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN.value)),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.admin_approve_listing(session, listing_id)
    return {
        "success": True,
        "message": "Listing approved and is now active",
        "data": ListingResponse.model_validate(listing).model_dump()
    }


@router.put(
    "/listings/{listing_id}/reject",
    status_code=status.HTTP_200_OK,
    summary="Reject listing (Admin only)"
)
async def reject_listing(
    listing_id: str,
    data: ListingRejectRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN.value)),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.admin_reject_listing(session, listing_id, data.reason)
    return {
        "success": True,
        "message": "Listing rejected with reason",
        "data": ListingResponse.model_validate(listing).model_dump()
    }
