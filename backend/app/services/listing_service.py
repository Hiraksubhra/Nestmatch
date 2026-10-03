import uuid
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.listing import (
    Listing,
    ListingPhoto,
    Amenity,
    listing_amenities,
    ListingStatus,
    PropertyType,
    GenderPreference,
    FurnishedStatus,
)
from app.models.user import User
from app.schemas.listing import ListingCreate, ListingUpdate
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException,
)


class ListingService:
    @staticmethod
    async def get_all_amenities(session: AsyncSession) -> List[Amenity]:
        result = await session.execute(select(Amenity).order_by(Amenity.id))
        return list(result.scalars().all())

    @staticmethod
    async def create_listing(
        session: AsyncSession,
        landlord_id: str,
        data: ListingCreate
    ) -> Listing:
        listing_dict = data.model_dump(exclude={"amenity_ids"})
        new_listing = Listing(
            landlord_id=landlord_id,
            status=ListingStatus.PENDING_VERIFICATION.value,
            **listing_dict
        )

        # Attach amenities
        if data.amenity_ids:
            amenities_res = await session.execute(
                select(Amenity).where(Amenity.id.in_(data.amenity_ids))
            )
            new_listing.amenities = list(amenities_res.scalars().all())

        session.add(new_listing)
        await session.commit()
        await session.refresh(new_listing)
        return await ListingService.get_by_id(session, new_listing.id)

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        listing_id: str,
        increment_view: bool = False
    ) -> Listing:
        stmt = (
            select(Listing)
            .where(Listing.id == listing_id)
            .options(
                selectinload(Listing.photos),
                selectinload(Listing.amenities),
                selectinload(Listing.landlord),
            )
        )
        result = await session.execute(stmt)
        listing = result.scalars().first()

        if not listing:
            raise NotFoundException(message="Listing not found", code="LISTING_NOT_FOUND")

        if increment_view:
            listing.views_count += 1
            await session.commit()
            await session.refresh(listing)

        return listing

    @staticmethod
    async def update_listing(
        session: AsyncSession,
        listing: Listing,
        data: ListingUpdate
    ) -> Listing:
        update_data = data.model_dump(exclude_unset=True)

        if "amenity_ids" in update_data:
            amenity_ids = update_data.pop("amenity_ids")
            if amenity_ids is not None:
                amenities_res = await session.execute(
                    select(Amenity).where(Amenity.id.in_(amenity_ids))
                )
                listing.amenities = list(amenities_res.scalars().all())

        for key, value in update_data.items():
            if hasattr(listing, key) and value is not None:
                setattr(listing, key, value)

        await session.commit()
        await session.refresh(listing)
        return await ListingService.get_by_id(session, listing.id)

    @staticmethod
    async def search_listings(
        session: AsyncSession,
        city: Optional[str] = None,
        locality: Optional[str] = None,
        property_type: Optional[str] = None,
        gender_preference: Optional[str] = None,
        furnished_status: Optional[str] = None,
        min_rent: Optional[Decimal] = None,
        max_rent: Optional[Decimal] = None,
        amenity_ids: Optional[List[int]] = None,
        search_query: Optional[str] = None,
        status: Optional[str] = ListingStatus.ACTIVE.value,
        sort: str = "newest",
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        conditions = []

        if status:
            conditions.append(Listing.status == status)

        # Shadow-ban exclusion: suppress listings from shadow-banned accounts in public search
        conditions.append(Listing.landlord.has(or_(User.is_shadow_banned == False, User.is_shadow_banned.is_(None))))

        if city:
            conditions.append(func.lower(Listing.city) == city.strip().lower())

        if locality:
            conditions.append(func.lower(Listing.locality).like(f"%{locality.strip().lower()}%"))

        if property_type:
            conditions.append(Listing.property_type == property_type)

        if gender_preference and gender_preference != "ANY":
            conditions.append(
                or_(
                    Listing.gender_preference == gender_preference,
                    Listing.gender_preference == "ANY"
                )
            )

        if furnished_status:
            conditions.append(Listing.furnished_status == furnished_status)

        if min_rent is not None:
            conditions.append(Listing.rent_amount >= min_rent)

        if max_rent is not None:
            conditions.append(Listing.rent_amount <= max_rent)

        if search_query:
            term = f"%{search_query.strip().lower()}%"
            conditions.append(
                or_(
                    func.lower(Listing.title).like(term),
                    func.lower(Listing.description).like(term),
                    func.lower(Listing.locality).like(term),
                    func.lower(Listing.city).like(term),
                )
            )

        if amenity_ids:
            for aid in amenity_ids:
                subq = (
                    select(listing_amenities.c.listing_id)
                    .where(listing_amenities.c.amenity_id == aid)
                )
                conditions.append(Listing.id.in_(subq))

        # Count total
        count_stmt = select(func.count(Listing.id)).where(and_(*conditions))
        total_count = (await session.execute(count_stmt)).scalar() or 0

        # Base query with ordering
        stmt = (
            select(Listing)
            .where(and_(*conditions))
            .options(
                selectinload(Listing.photos),
                selectinload(Listing.amenities),
                selectinload(Listing.landlord),
            )
        )

        if sort == "price_asc":
            stmt = stmt.order_by(asc(Listing.rent_amount))
        elif sort == "price_desc":
            stmt = stmt.order_by(desc(Listing.rent_amount))
        elif sort == "views":
            stmt = stmt.order_by(desc(Listing.views_count))
        else:  # newest
            stmt = stmt.order_by(desc(Listing.created_at))

        # Pagination
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)

        result = await session.execute(stmt)
        listings = result.scalars().all()

        pages = (total_count + limit - 1) // limit if limit > 0 else 1

        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": pages,
            "items": list(listings),
        }

    @staticmethod
    async def get_landlord_listings(
        session: AsyncSession,
        landlord_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        count_stmt = select(func.count(Listing.id)).where(Listing.landlord_id == landlord_id)
        total_count = (await session.execute(count_stmt)).scalar() or 0

        stmt = (
            select(Listing)
            .where(Listing.landlord_id == landlord_id)
            .options(
                selectinload(Listing.photos),
                selectinload(Listing.amenities),
                selectinload(Listing.landlord),
            )
            .order_by(desc(Listing.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        result = await session.execute(stmt)
        listings = result.scalars().all()
        pages = (total_count + limit - 1) // limit if limit > 0 else 1

        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": pages,
            "items": list(listings),
        }

    @staticmethod
    async def add_photo(
        session: AsyncSession,
        listing_id: str,
        url: str,
        public_id: Optional[str] = None,
        is_cover: bool = False,
        sort_order: int = 0
    ) -> ListingPhoto:
        photo = ListingPhoto(
            listing_id=listing_id,
            url=url,
            public_id=public_id,
            is_cover=is_cover,
            sort_order=sort_order
        )
        session.add(photo)
        await session.commit()
        await session.refresh(photo)
        return photo

    @staticmethod
    async def delete_photo(
        session: AsyncSession,
        listing_id: str,
        photo_id: str
    ) -> None:
        stmt = select(ListingPhoto).where(
            and_(ListingPhoto.id == photo_id, ListingPhoto.listing_id == listing_id)
        )
        result = await session.execute(stmt)
        photo = result.scalars().first()
        if not photo:
            raise NotFoundException(message="Photo not found", code="PHOTO_NOT_FOUND")

        await session.delete(photo)
        await session.commit()

    @staticmethod
    async def get_pending_listings(
        session: AsyncSession,
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        count_stmt = select(func.count(Listing.id)).where(
            Listing.status == ListingStatus.PENDING_VERIFICATION.value
        )
        total_count = (await session.execute(count_stmt)).scalar() or 0

        stmt = (
            select(Listing)
            .where(Listing.status == ListingStatus.PENDING_VERIFICATION.value)
            .options(
                selectinload(Listing.photos),
                selectinload(Listing.amenities),
                selectinload(Listing.landlord),
            )
            .order_by(asc(Listing.created_at))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        result = await session.execute(stmt)
        listings = result.scalars().all()
        pages = (total_count + limit - 1) // limit if limit > 0 else 1

        return {
            "total": total_count,
            "page": page,
            "limit": limit,
            "pages": pages,
            "items": list(listings),
        }

    @staticmethod
    async def admin_approve_listing(
        session: AsyncSession,
        listing_id: str
    ) -> Listing:
        listing = await ListingService.get_by_id(session, listing_id)
        listing.status = ListingStatus.ACTIVE.value
        listing.rejection_reason = None
        await session.commit()
        await session.refresh(listing)
        return listing

    @staticmethod
    async def admin_reject_listing(
        session: AsyncSession,
        listing_id: str,
        reason: str
    ) -> Listing:
        listing = await ListingService.get_by_id(session, listing_id)
        listing.status = ListingStatus.REJECTED.value
        listing.rejection_reason = reason
        await session.commit()
        await session.refresh(listing)
        return listing
