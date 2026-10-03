from sqlalchemy import select, inspect, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base
from app.db.session import engine, async_session_maker
from app.models.listing import Amenity
# Import all models to ensure they are registered with Base.metadata
import app.models  # noqa: F401

DEFAULT_AMENITIES = [
    {"name": "wifi", "label": "High-Speed Wi-Fi", "icon": "wifi"},
    {"name": "ac", "label": "Air Conditioner", "icon": "wind"},
    {"name": "food_included", "label": "Mess / Food Included", "icon": "utensils"},
    {"name": "laundry", "label": "Washing Machine / Laundry", "icon": "shirt"},
    {"name": "power_backup", "label": "Power Backup", "icon": "zap"},
    {"name": "ro_water", "label": "RO Purified Water", "icon": "droplets"},
    {"name": "security", "label": "CCTV & Security Guard", "icon": "shield-check"},
    {"name": "geyser", "label": "Hot Water / Geyser", "icon": "flame"},
    {"name": "housekeeping", "label": "Regular Housekeeping", "icon": "sparkles"},
    {"name": "parking", "label": "Two-Wheeler / Car Parking", "icon": "car"},
    {"name": "refrigerator", "label": "Refrigerator", "icon": "refrigerator"},
    {"name": "study_desk", "label": "Study Table & Chair", "icon": "book-open"},
    {"name": "attached_washroom", "label": "Attached Washroom", "icon": "bath"},
    {"name": "gym", "label": "Gym / Fitness Center", "icon": "dumbbell"},
]


async def seed_amenities(session: AsyncSession) -> None:
    result = await session.execute(select(Amenity).limit(1))
    if result.scalars().first() is None:
        for item in DEFAULT_AMENITIES:
            session.add(Amenity(name=item["name"], label=item["label"], icon=item["icon"]))
        await session.commit()


def check_and_add_user_columns(connection):
    inspector = inspect(connection)
    if "users" in inspector.get_table_names():
        columns = [c["name"] for c in inspector.get_columns("users")]
        if "is_shadow_banned" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN is_shadow_banned BOOLEAN DEFAULT 0 NOT NULL"))
        if "shadow_banned_at" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN shadow_banned_at DATETIME"))
        if "shadow_ban_reason" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN shadow_ban_reason VARCHAR(255)"))


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(check_and_add_user_columns)

    async with async_session_maker() as session:
        await seed_amenities(session)
