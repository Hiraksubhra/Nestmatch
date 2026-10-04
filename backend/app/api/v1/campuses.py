from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.campus import Campus
from app.schemas.campus import CampusResponse

router = APIRouter(prefix="/campuses", tags=["Campuses"])


@router.get("", status_code=status.HTTP_200_OK, summary="List university campuses")
async def list_campuses(
    city: Optional[str] = Query(None, description="Filter by city, e.g. Pune, Mumbai, Bangalore"),
    session: AsyncSession = Depends(get_db),
):
    query = select(Campus).order_by(Campus.city.asc(), Campus.name.asc())
    if city:
        query = query.where(func.lower(Campus.city) == city.strip().lower())

    result = await session.execute(query)
    campuses = result.scalars().all()
    return {
        "success": True,
        "data": [CampusResponse.model_validate(c).model_dump() for c in campuses],
    }


@router.get("/{campus_id}", status_code=status.HTTP_200_OK, summary="Get campus details")
async def get_campus(
    campus_id: str,
    session: AsyncSession = Depends(get_db),
):
    campus = await session.get(Campus, campus_id)
    if not campus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campus not found")
    return {
        "success": True,
        "data": CampusResponse.model_validate(campus).model_dump(),
    }
