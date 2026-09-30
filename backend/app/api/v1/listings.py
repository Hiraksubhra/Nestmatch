from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.listing import ListingStatus
from app.schemas.listing import (
    ListingCreate,
    ListingUpdate,
    ListingResponse,
    AmenityResponse,
    ListingPhotoResponse,
    PaginatedListingsResponse,
)
from app.services.listing_service import ListingService
from app.services.photo_service import PhotoService
from app.core.exceptions import ForbiddenException

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.get(
    "/amenities",
    status_code=status.HTTP_200_OK,
    summary="Get all available amenities"
)
async def get_amenities(
    session: AsyncSession = Depends(get_db)
):
    amenities = await ListingService.get_all_amenities(session)
    return {
        "success": True,
        "data": [AmenityResponse.model_validate(a).model_dump() for a in amenities]
    }


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Search and discover listings"
)
async def search_listings(
    city: Optional[str] = Query(None, description="City name (e.g. Pune, Bangalore)"),
    locality: Optional[str] = Query(None, description="Locality or neighborhood"),
    property_type: Optional[str] = Query(None, description="PG, APARTMENT, SHARED_ROOM, STUDIO"),
    gender_preference: Optional[str] = Query(None, description="ANY, MALE, FEMALE"),
    furnished_status: Optional[str] = Query(None, description="FURNISHED, SEMI, UNFURNISHED"),
    min_rent: Optional[Decimal] = Query(None, ge=0, description="Minimum rent amount"),
    max_rent: Optional[Decimal] = Query(None, ge=0, description="Maximum rent amount"),
    amenities: Optional[str] = Query(None, description="Comma-separated amenity IDs e.g. 1,2,3"),
    search: Optional[str] = Query(None, description="Free text search on title/desc/locality"),
    sort: Optional[str] = Query("newest", description="sort option: newest, price_asc, price_desc, views"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db)
):
    amenity_ids = None
    if amenities:
        try:
            amenity_ids = [int(a.strip()) for a in amenities.split(",") if a.strip()]
        except ValueError:
            pass

    results = await ListingService.search_listings(
        session=session,
        city=city,
        locality=locality,
        property_type=property_type,
        gender_preference=gender_preference,
        furnished_status=furnished_status,
        min_rent=min_rent,
        max_rent=max_rent,
        amenity_ids=amenity_ids,
        search_query=search,
        status=ListingStatus.ACTIVE.value,
        sort=sort,
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


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new listing (Landlord or Admin only)"
)
async def create_listing(
    data: ListingCreate,
    current_user: User = Depends(require_role(UserRole.LANDLORD.value, UserRole.ADMIN.value)),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.create_listing(
        session=session,
        landlord_id=current_user.id,
        data=data
    )
    return {
        "success": True,
        "message": "Listing submitted successfully. Awaiting verification.",
        "data": ListingResponse.model_validate(listing).model_dump()
    }


@router.get(
    "/my",
    status_code=status.HTTP_200_OK,
    summary="Get landlord's own listings"
)
async def get_my_listings(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_role(UserRole.LANDLORD.value, UserRole.ADMIN.value)),
    session: AsyncSession = Depends(get_db)
):
    results = await ListingService.get_landlord_listings(
        session=session,
        landlord_id=current_user.id,
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


@router.get(
    "/{listing_id}",
    status_code=status.HTTP_200_OK,
    summary="Get listing detail by ID"
)
async def get_listing_detail(
    listing_id: str,
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.get_by_id(session, listing_id, increment_view=True)
    return {
        "success": True,
        "data": ListingResponse.model_validate(listing).model_dump()
    }


@router.put(
    "/{listing_id}",
    status_code=status.HTTP_200_OK,
    summary="Update listing (Owner or Admin only)"
)
async def update_listing(
    listing_id: str,
    data: ListingUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.get_by_id(session, listing_id)
    if listing.landlord_id != current_user.id and current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException(message="Not authorized to edit this listing", code="FORBIDDEN")

    updated = await ListingService.update_listing(session, listing, data)
    return {
        "success": True,
        "message": "Listing updated successfully",
        "data": ListingResponse.model_validate(updated).model_dump()
    }


@router.delete(
    "/{listing_id}",
    status_code=status.HTTP_200_OK,
    summary="Archive listing (Owner or Admin only)"
)
async def archive_listing(
    listing_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.get_by_id(session, listing_id)
    if listing.landlord_id != current_user.id and current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException(message="Not authorized to archive this listing", code="FORBIDDEN")

    listing.status = ListingStatus.ARCHIVED.value
    await session.commit()
    return {
        "success": True,
        "message": "Listing archived successfully"
    }


@router.post(
    "/{listing_id}/photos",
    status_code=status.HTTP_201_CREATED,
    summary="Upload photo for a listing"
)
async def upload_listing_photo(
    listing_id: str,
    file: UploadFile = File(...),
    is_cover: bool = Query(False),
    sort_order: int = Query(0),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.get_by_id(session, listing_id)
    if listing.landlord_id != current_user.id and current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException(message="Not authorized to upload photos to this listing", code="FORBIDDEN")

    upload_data = await PhotoService.upload_image(file, folder=f"listings/{listing_id}")
    photo = await ListingService.add_photo(
        session=session,
        listing_id=listing_id,
        url=upload_data["url"],
        public_id=upload_data.get("public_id"),
        is_cover=is_cover,
        sort_order=sort_order,
    )

    return {
        "success": True,
        "message": "Photo uploaded successfully",
        "data": ListingPhotoResponse.model_validate(photo).model_dump()
    }


@router.delete(
    "/{listing_id}/photos/{photo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a photo from a listing"
)
async def delete_listing_photo(
    listing_id: str,
    photo_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    listing = await ListingService.get_by_id(session, listing_id)
    if listing.landlord_id != current_user.id and current_user.role != UserRole.ADMIN.value:
        raise ForbiddenException(message="Not authorized to delete photos from this listing", code="FORBIDDEN")

    await ListingService.delete_photo(session, listing_id, photo_id)
    return {
        "success": True,
        "message": "Photo deleted successfully"
    }
