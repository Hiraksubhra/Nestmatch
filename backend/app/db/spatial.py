"""
Spatial and PostGIS type definitions with cross-dialect compatibility.
Uses PostGIS Geography('POINT', srid=4326) on PostgreSQL, with clean fallback on SQLite.
"""
from typing import Optional, Any
from sqlalchemy import Text
from sqlalchemy.types import TypeDecorator

try:
    from geoalchemy2 import Geography
    HAS_GEOALCHEMY = True
except ImportError:
    HAS_GEOALCHEMY = False


class GeoPoint(TypeDecorator):
    """
    Cross-dialect spatial Geography point (SRID 4326).
    Maps to PostGIS `geography(POINT, 4326)` when connected to PostgreSQL,
    and fallback text representation on SQLite.
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql" and HAS_GEOALCHEMY:
            return dialect.type_descriptor(Geography(geometry_type="POINT", srid=4326, spatial_index=True))
        return dialect.type_descriptor(Text())

    def process_bind_param(self, value: Any, dialect: Any) -> Optional[str]:
        if value is None:
            return None
        # Support WKT string e.g. 'POINT(73.8565 18.5293)' or (lat, lng) tuple/dict
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)) and len(value) == 2:
            lng, lat = value
            return f"POINT({lng} {lat})"
        if isinstance(value, dict) and "longitude" in value and "latitude" in value:
            return f"POINT({value['longitude']} {value['latitude']})"
        return str(value)
