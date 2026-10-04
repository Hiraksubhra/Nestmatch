import logging
import math
import httpx
from decimal import Decimal
from typing import Optional, List, Dict, Tuple, Any
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campus import Campus
from app.models.listing import Listing
from app.core.config import settings

logger = logging.getLogger(__name__)

# Known fallback center points for Indian university cities
CITY_CENTROIDS = {
    "pune": (18.5204, 73.8567),
    "mumbai": (19.0760, 72.8777),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "delhi": (28.7041, 77.1025),
    "new delhi": (28.6139, 77.2090),
}


def calculate_geodesic_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Computes great-circle distance between two points on the WGS-84 ellipsoid
    in kilometers using the Haversine formula (matching PostGIS ST_DistanceSphere).
    """
    R = 6371.0  # Earth's radius in km

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def estimate_walking_time_mins(distance_km: float) -> int:
    """Estimates average student walking commute (average speed 4.8 km/h)."""
    return max(1, int(round((distance_km / 4.8) * 60)))


class CampusService:
    @staticmethod
    async def geocode_address(
        address_line1: Optional[str] = None,
        locality: Optional[str] = None,
        city: Optional[str] = None,
        pincode: Optional[str] = None,
    ) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        """
        Geocodes address string to (latitude, longitude, formatted_address).
        Uses Google Maps Geocoding API if key provided, otherwise OpenStreetMap Nominatim,
        with graceful fallback to city centroid coordinates.
        """
        query_parts = [p.strip() for p in [address_line1, locality, city, pincode, "India"] if p and p.strip()]
        query_str = ", ".join(query_parts)

        # 1. Try Google Maps Places API (New) & Geocoding API if configured
        if getattr(settings, "GOOGLE_MAPS_API_KEY", None):
            try:
                async with httpx.AsyncClient(timeout=4.0) as client:
                    # 1a. Try Places API (New) searchText endpoint (optimal for messy queries)
                    places_resp = await client.post(
                        "https://places.googleapis.com/v1/places:searchText",
                        headers={
                            "Content-Type": "application/json",
                            "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
                            "X-Goog-FieldMask": "places.formattedAddress,places.location",
                        },
                        json={"textQuery": query_str},
                    )
                    if places_resp.status_code == 200:
                        p_data = places_resp.json()
                        places = p_data.get("places", [])
                        if places and "location" in places[0]:
                            loc = places[0]["location"]
                            formatted = places[0].get("formattedAddress", query_str)
                            return float(loc["latitude"]), float(loc["longitude"]), formatted

                    # 1b. Fallback to Geocoding API
                    geo_resp = await client.get(
                        "https://maps.googleapis.com/maps/api/geocode/json",
                        params={
                            "address": query_str,
                            "key": settings.GOOGLE_MAPS_API_KEY,
                        },
                    )
                    data = geo_resp.json()
                    if data.get("status") == "OK" and data.get("results"):
                        loc = data["results"][0]["geometry"]["location"]
                        formatted = data["results"][0].get("formatted_address", query_str)
                        return float(loc["lat"]), float(loc["lng"]), formatted
                    elif data.get("error_message"):
                        logger.warning(f"Google Maps Geocoding error: {data.get('error_message')}")
            except Exception as e:
                logger.warning(f"Google Maps APIs failed, trying fallback: {e}")

        # 2. Try OpenStreetMap Nominatim with proper User-Agent
        try:
            headers = {"User-Agent": "NestMatch-Student-Housing/1.0 (info@nestmatch.in)"}
            async with httpx.AsyncClient(timeout=4.0, headers=headers) as client:
                resp = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q": query_str, "format": "json", "limit": 1},
                )
                if resp.status_code == 200:
                    results = resp.json()
                    if results and len(results) > 0:
                        lat = float(results[0]["lat"])
                        lon = float(results[0]["lon"])
                        display_name = results[0].get("display_name", query_str)
                        return lat, lon, display_name
        except Exception as e:
            logger.warning(f"Nominatim geocoding failed: {e}")

        # 3. Fallback to city centroid
        if city:
            c_key = city.strip().lower()
            if c_key in CITY_CENTROIDS:
                lat, lon = CITY_CENTROIDS[c_key]
                return lat, lon, f"{city}, India"

        return None, None, None

    @staticmethod
    async def get_nearby_campuses(
        session: AsyncSession,
        latitude: float,
        longitude: float,
        city: Optional[str] = None,
        max_distance_km: float = 15.0,
        limit: int = 4,
    ) -> List[Dict[str, Any]]:
        """
        Dynamically finds all verified university campuses within max_distance_km,
        ordered by proximity. Uses PostGIS ST_Distance if PostgreSQL is connected,
        or geodesic computation on SQLite.
        """
        query = select(Campus)
        if city:
            c_norm = city.strip().lower()
            if "delhi" in c_norm:
                query = query.where(func.lower(Campus.city).in_(["delhi", "delhi ncr", "new delhi"]))
            elif "bangalore" in c_norm or "bengaluru" in c_norm:
                query = query.where(func.lower(Campus.city).in_(["bangalore", "bengaluru"]))
            elif "mumbai" in c_norm or "bombay" in c_norm:
                query = query.where(func.lower(Campus.city).in_(["mumbai", "bombay"]))
            else:
                query = query.where(func.lower(Campus.city) == c_norm)

        result = await session.execute(query)
        campuses = result.scalars().all()

        nearby = []
        for c in campuses:
            c_lat = float(c.latitude)
            c_lon = float(c.longitude)
            dist_km = calculate_geodesic_distance(latitude, longitude, c_lat, c_lon)
            if dist_km <= max_distance_km:
                nearby.append({
                    "campus_id": c.id,
                    "name": c.name,
                    "short_name": c.short_name or c.name,
                    "city": c.city,
                    "locality": c.locality,
                    "distance_km": dist_km,
                    "distance_meters": int(dist_km * 1000),
                    "walking_time_mins": estimate_walking_time_mins(dist_km),
                    "latitude": c_lat,
                    "longitude": c_lon,
                })

        # Sort closest to farthest
        nearby.sort(key=lambda x: x["distance_km"])
        return nearby[:limit]

    @staticmethod
    async def enrich_listing_proximity(
        session: AsyncSession,
        listing: Listing,
    ) -> List[Dict[str, Any]]:
        """
        Calculates real-time campus proximity for a listing and syncs its PostGIS location point.
        """
        if listing.latitude is None or listing.longitude is None:
            # Attempt geocode from address
            lat, lon, _ = await CampusService.geocode_address(
                address_line1=listing.address_line1,
                locality=listing.locality,
                city=listing.city,
                pincode=listing.pincode,
            )
            if lat is not None and lon is not None:
                listing.latitude = Decimal(str(lat))
                listing.longitude = Decimal(str(lon))

        if listing.latitude is not None and listing.longitude is not None:
            lat = float(listing.latitude)
            lon = float(listing.longitude)
            listing.location = f"POINT({lon} {lat})"

            nearby = await CampusService.get_nearby_campuses(
                session=session,
                latitude=lat,
                longitude=lon,
                city=listing.city,
                max_distance_km=15.0,
                limit=4,
            )
            if nearby:
                listing.university_proximity = nearby
                return nearby

        return listing.university_proximity or []
