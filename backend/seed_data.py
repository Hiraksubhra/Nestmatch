
import asyncio
import sys
import uuid
from datetime import datetime, timezone, date, timedelta
from decimal import Decimal
from sqlalchemy import select

# Ensure backend root is on Python path
sys.path.insert(0, ".")

from app.db.session import async_session_maker, engine
from app.db.base import Base
from app.db.init_db import init_db
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.flatmate import FlatmateProfile
from app.models.listing import (
    Listing,
    ListingPhoto,
    Amenity,
    PropertyType,
    GenderPreference,
    FurnishedStatus,
    ListingStatus,
    RentPeriod,
)

# High quality student housing photos
PHOTOS_MAP = {
    "pg_modern": [
        "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=1000&q=80",
    ],
    "apartment": [
        "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1000&q=80",
    ],
    "studio": [
        "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=80",
    ],
    "cozy_room": [
        "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=1000&q=80",
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1000&q=80",
    ],
    "local_assets": [
        "/static/uploads/listings/6a402d17-ceed-4285-b415-588394b446fc/9c409b91-ce64-4e2a-b918-b790e975b0a3_house_listing_1.jpg",
        "/static/uploads/listings/6a402d17-ceed-4285-b415-588394b446fc/31325331-8c7d-43ef-9939-9bf863cb8d88_house_listing_2.jpg",
        "/static/uploads/listings/6a402d17-ceed-4285-b415-588394b446fc/2100e011-34fa-431e-860f-ef161fbfc84d_house_listing_3.jpg",
    ]
}


async def seed():
    print("=" * 60)
    print("SEEDING NESTMATCH DATABASE WITH COMPLETE DEMO DATA")
    print("=" * 60)

    await init_db()

    async with async_session_maker() as session:
        # Load all amenities
        amenities_res = await session.execute(select(Amenity))
        all_amenities = {a.name: a for a in amenities_res.scalars().all()}
        print(f"Loaded {len(all_amenities)} system amenities.")

        # 1. Create Users
        users_data = [
            # Landlords
            {
                "email": "landlord@nestmatch.in",
                "password": "Landlord123!",
                "full_name": "Rajesh Sharma",
                "role": UserRole.LANDLORD.value,
                "phone": "+91 98220 12345",
            },
            {
                "email": "sunita.landlord@nestmatch.in",
                "password": "Landlord123!",
                "full_name": "Sunita Deshmukh",
                "role": UserRole.LANDLORD.value,
                "phone": "+91 98220 54321",
            },
            {
                "email": "vikram.pg@nestmatch.in",
                "password": "Landlord123!",
                "full_name": "Vikram Malhotra",
                "role": UserRole.LANDLORD.value,
                "phone": "+91 98111 99887",
            },
            # Students
            {
                "email": "student@nestmatch.in",
                "password": "Student123!",
                "full_name": "Aarav Patel",
                "role": UserRole.STUDENT.value,
                "phone": "+91 97654 32100",
            },
            {
                "email": "priya.student@nestmatch.in",
                "password": "Student123!",
                "full_name": "Priya Nair",
                "role": UserRole.STUDENT.value,
                "phone": "+91 98765 11223",
            },
            {
                "email": "kabir.student@nestmatch.in",
                "password": "Student123!",
                "full_name": "Kabir Mehta",
                "role": UserRole.STUDENT.value,
                "phone": "+91 99887 76655",
            },
            {
                "email": "aanya_s3@test.com",
                "password": "Student123!",
                "full_name": "Aanya Sharma",
                "role": UserRole.STUDENT.value,
                "phone": "+91 98230 44556",
            },
            {
                "email": "priya_s3@test.com",
                "password": "Student123!",
                "full_name": "Priya Patel",
                "role": UserRole.STUDENT.value,
                "phone": "+91 98231 66778",
            },
            # Admin
            {
                "email": "admin@nestmatch.in",
                "password": "Admin123!",
                "full_name": "Platform Administrator",
                "role": UserRole.ADMIN.value,
                "phone": "+91 90000 00001",
            },
        ]

        created_users = {}
        for u in users_data:
            existing = (await session.execute(select(User).where(User.email == u["email"]))).scalars().first()
            if not existing:
                new_u = User(
                    email=u["email"],
                    password_hash=hash_password(u["password"]),
                    full_name=u["full_name"],
                    role=u["role"],
                    phone=u["phone"],
                    is_active=True,
                    is_verified=True,
                )
                session.add(new_u)
                await session.flush()
                await session.refresh(new_u)
                created_users[u["email"]] = new_u
                print(f"Created User: {u['full_name']} ({u['role']}) -> {u['email']}")
            else:
                created_users[u["email"]] = existing
                print(f"User exists: {u['email']}")

        # 1.5 Seed Student Flatmate Profiles
        today = date.today()
        next_month = today + timedelta(days=30)
        flatmates_seed = [
            {
                "email": "aanya_s3@test.com",
                "budget_min": Decimal("7000.00"),
                "budget_max": Decimal("13000.00"),
                "city": "Pune",
                "uni": "Pune University",
                "locality": "Kothrud",
                "move_in": next_month,
                "flex": 7,
                "gender": "FEMALE",
                "bio": "First year CS undergrad at Pune University looking for a clean, vegetarian flatmate. Early sleeper and studious.",
                "tags": ["early_riser", "vegetarian", "non_smoker", "studious", "quiet"]
            },
            {
                "email": "priya_s3@test.com",
                "budget_min": Decimal("8000.00"),
                "budget_max": Decimal("14000.00"),
                "city": "Pune",
                "uni": "Pune University",
                "locality": "Viman Nagar",
                "move_in": next_month,
                "flex": 10,
                "gender": "FEMALE",
                "bio": "Engineering student looking for a friendly roommate to share an apartment near Viman Nagar. Loves good food and weekend study sessions.",
                "tags": ["early_riser", "vegetarian", "studious", "social"]
            },
            {
                "email": "priya.student@nestmatch.in",
                "budget_min": Decimal("10000.00"),
                "budget_max": Decimal("18000.00"),
                "city": "Pune",
                "uni": "Symbiosis International University",
                "locality": "Senapati Bapat Road",
                "move_in": next_month + timedelta(days=15),
                "flex": 14,
                "gender": "FEMALE",
                "bio": "Master's student at Symbiosis looking for a neat and peaceful flat. Morning jogger, non-smoker, and pet-friendly.",
                "tags": ["early_riser", "non_smoker", "fitness", "pet_friendly", "clean_freak"]
            },
            {
                "email": "student@nestmatch.in",
                "budget_min": Decimal("8000.00"),
                "budget_max": Decimal("15000.00"),
                "city": "Pune",
                "uni": "COEP Tech",
                "locality": "Shivajinagar",
                "move_in": next_month,
                "flex": 7,
                "gender": "MALE",
                "bio": "COEP engineering undergrad looking for flatmates for a 2BHK/3BHK in Shivajinagar. Love fitness and listening to indie music.",
                "tags": ["night_owl", "music_lover", "fitness", "non_smoker"]
            },
            {
                "email": "kabir.student@nestmatch.in",
                "budget_min": Decimal("9000.00"),
                "budget_max": Decimal("16000.00"),
                "city": "Pune",
                "uni": "MIT World Peace University",
                "locality": "Kothrud",
                "move_in": today + timedelta(days=60),
                "flex": 14,
                "gender": "MALE",
                "bio": "Design & tech student at MIT-WPU. Chill, clean, vegetarian, mostly work on projects in the evening.",
                "tags": ["night_owl", "vegetarian", "studious", "music_lover"]
            },
        ]

        for fp_data in flatmates_seed:
            user_obj = created_users.get(fp_data["email"])
            if not user_obj:
                continue
            existing_fp = (await session.execute(select(FlatmateProfile).where(FlatmateProfile.user_id == user_obj.id))).scalars().first()
            if not existing_fp:
                fp = FlatmateProfile(
                    user_id=user_obj.id,
                    budget_min=fp_data["budget_min"],
                    budget_max=fp_data["budget_max"],
                    preferred_city=fp_data["city"],
                    preferred_university=fp_data["uni"],
                    preferred_locality=fp_data["locality"],
                    move_in_date=fp_data["move_in"],
                    move_in_flexibility=fp_data["flex"],
                    gender=fp_data["gender"],
                    bio=fp_data["bio"],
                    lifestyle_tags=fp_data["tags"],
                    is_active=True,
                )
                session.add(fp)
                print(f"Created Flatmate Profile for {user_obj.full_name}")

        rajesh = created_users["landlord@nestmatch.in"]
        sunita = created_users["sunita.landlord@nestmatch.in"]
        vikram = created_users["vikram.pg@nestmatch.in"]

        # 2. Create Rich Listings
        listings_seed = [
            {
                "landlord_id": rajesh.id,
                "title": "Symbiosis Scholar PG - Single AC Room",
                "description": "Premium student PG accommodation walking distance from Symbiosis Viman Nagar campus. Includes 3-time hygienic home meals, high-speed fiber Wi-Fi, air conditioning, daily housekeeping, and 24/7 security guard.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("11500.00"),
                "deposit_amount": Decimal("20000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Viman Nagar",
                "address_line1": "Plot 42, Clover Park, Viman Nagar",
                "state": "Maharashtra",
                "pincode": "411014",
                "gender_preference": GenderPreference.FEMALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 84,
                "university_proximity": [{"name": "Symbiosis International (Viman Nagar)", "distance_km": 0.6}],
                "amenities": ["wifi", "ac", "food_included", "laundry", "security", "geyser", "housekeeping", "study_desk"],
                "photos": PHOTOS_MAP["pg_modern"],
            },
            {
                "landlord_id": rajesh.id,
                "title": "Shivaji Nagar 2BHK Student Shared Flat",
                "description": "Spacious flat right next to Fergusson College Road. Ideal for students studying at FC, BMCC, or COEP. Large study desks, refrigerator, washing machine, and bike parking included.",
                "property_type": PropertyType.APARTMENT.value,
                "rent_amount": Decimal("8500.00"),
                "deposit_amount": Decimal("15000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Shivajinagar",
                "address_line1": "FC Road, Behind Goodluck Cafe",
                "state": "Maharashtra",
                "pincode": "411004",
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 128,
                "university_proximity": [{"name": "Fergusson College", "distance_km": 0.3}, {"name": "COEP Tech", "distance_km": 1.8}],
                "amenities": ["wifi", "refrigerator", "laundry", "parking", "geyser", "study_desk"],
                "photos": PHOTOS_MAP["apartment"],
            },
            {
                "landlord_id": sunita.id,
                "title": "Cozy Studio near Pune University & Aundh",
                "description": "Private studio apartment with attached washroom and kitchenette. Peaceful residential society with backup power, RO water, and high-speed internet. Ideal for postgraduate or research students.",
                "property_type": PropertyType.STUDIO.value,
                "rent_amount": Decimal("14000.00"),
                "deposit_amount": Decimal("25000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Aundh",
                "address_line1": "DP Road, Aundh",
                "state": "Maharashtra",
                "pincode": "411007",
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 67,
                "university_proximity": [{"name": "Savitribai Phule Pune University", "distance_km": 1.5}],
                "amenities": ["wifi", "ac", "power_backup", "ro_water", "attached_washroom", "security", "refrigerator"],
                "photos": PHOTOS_MAP["studio"],
            },
            {
                "landlord_id": sunita.id,
                "title": "Koramangala Tech & Student PG with Food",
                "description": "Modern co-living space located near Christ University central campus. Includes North & South Indian mess, gym access, game room, biometric security, and high-speed Wi-Fi.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("13500.00"),
                "deposit_amount": Decimal("20000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Bengaluru",
                "locality": "Koramangala",
                "address_line1": "8th Block, Koramangala",
                "state": "Karnataka",
                "pincode": "560095",
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 210,
                "university_proximity": [{"name": "Christ University (Central Campus)", "distance_km": 0.9}],
                "amenities": ["wifi", "food_included", "ac", "gym", "laundry", "security", "housekeeping"],
                "photos": PHOTOS_MAP["pg_modern"],
            },
            {
                "landlord_id": vikram.id,
                "title": "HSR Layout Shared 3BHK for Students",
                "description": "Comfortable twin-sharing rooms in a breezy 3BHK apartment in HSR Sector 2. Well-connected to NIFT, St. John's, and IT hubs. Dedicated quiet hours for studying.",
                "property_type": PropertyType.SHARED_ROOM.value,
                "rent_amount": Decimal("8500.00"),
                "deposit_amount": Decimal("15000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Bengaluru",
                "locality": "HSR Layout",
                "address_line1": "Sector 2, HSR Layout",
                "state": "Karnataka",
                "pincode": "560102",
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.SEMI.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 55,
                "university_proximity": [{"name": "NIFT Bengaluru", "distance_km": 1.4}],
                "amenities": ["wifi", "power_backup", "ro_water", "laundry", "parking"],
                "photos": PHOTOS_MAP["cozy_room"],
            },
            {
                "landlord_id": vikram.id,
                "title": "North Campus Girls PG - Kamla Nagar",
                "description": "Exclusive girls PG in the heart of Delhi University North Campus. AC rooms, 4-time home-style meals, 24/7 female warden, biometric gate access, and library study zone.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("12500.00"),
                "deposit_amount": Decimal("15000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Delhi NCR",
                "locality": "Kamla Nagar",
                "address_line1": "Bada Gol Chakkar, Kamla Nagar",
                "state": "Delhi",
                "pincode": "110007",
                "gender_preference": GenderPreference.FEMALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 315,
                "university_proximity": [{"name": "Delhi University North Campus / Hansraj / SRCC", "distance_km": 0.5}],
                "amenities": ["wifi", "ac", "food_included", "security", "geyser", "study_desk", "ro_water"],
                "photos": PHOTOS_MAP["pg_modern"],
            },
            {
                "landlord_id": vikram.id,
                "title": "Powai High-Rise Suite near IIT Bombay",
                "description": "High-end student shared flat in Powai overlooking the lake. 5 minutes from IIT Bombay main gate. High security, club house, swimming pool, and study lounge.",
                "property_type": PropertyType.APARTMENT.value,
                "rent_amount": Decimal("22000.00"),
                "deposit_amount": Decimal("40000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Mumbai",
                "locality": "Powai",
                "address_line1": "Hiranandani Gardens, Powai",
                "state": "Maharashtra",
                "pincode": "400076",
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 182,
                "university_proximity": [{"name": "IIT Bombay", "distance_km": 0.8}],
                "amenities": ["wifi", "ac", "gym", "security", "power_backup", "parking", "laundry"],
                "photos": PHOTOS_MAP["apartment"],
            },
            {
                "landlord_id": rajesh.id,
                "title": "Allen Coaching Hub Boys PG with Mess",
                "description": "Strict study environment with zero distractions for JEE/NEET aspirants. Includes 3 nutritional meals, study table with lamp, silent curfew hours, and power backup.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("7500.00"),
                "deposit_amount": Decimal("10000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Kota",
                "locality": "Landmark City",
                "address_line1": "Kunhari, Landmark City",
                "state": "Rajasthan",
                "pincode": "324008",
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 9,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 94,
                "university_proximity": [{"name": "Allen Samyak / Career Point", "distance_km": 0.4}],
                "amenities": ["wifi", "food_included", "study_desk", "ro_water", "security", "geyser"],
                "photos": PHOTOS_MAP["cozy_room"],
            },
            # Pending verification listing (Visible in landlord dashboard as Under Verification)
            {
                "landlord_id": rajesh.id,
                "title": "Affordable 1RK Room in Kothrud near MIT",
                "description": "Newly renovated 1RK room with kitchen counter and separate washroom. Awaiting verification team review.",
                "property_type": PropertyType.STUDIO.value,
                "rent_amount": Decimal("6500.00"),
                "deposit_amount": Decimal("12000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Kothrud",
                "address_line1": "Paud Road, Kothrud",
                "state": "Maharashtra",
                "pincode": "411038",
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.SEMI.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.PENDING_VERIFICATION.value,
                "views_count": 4,
                "university_proximity": [{"name": "MIT World Peace University", "distance_km": 1.1}],
                "amenities": ["wifi", "water_purifier", "parking"],
                "photos": PHOTOS_MAP["local_assets"],
            },
            # Rejected listing test case
            {
                "landlord_id": rajesh.id,
                "title": "Basement Storage Unit Converted to Room",
                "description": "Budget space in underground floor.",
                "property_type": PropertyType.SHARED_ROOM.value,
                "rent_amount": Decimal("4000.00"),
                "deposit_amount": Decimal("5000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Katraj",
                "address_line1": "Katraj Bypass",
                "state": "Maharashtra",
                "pincode": "411046",
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.UNFURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 1,
                "max_occupancy": 1,
                "status": ListingStatus.REJECTED.value,
                "rejection_reason": "Listing rejected: basement lacks adequate natural ventilation and fire escape compliance.",
                "views_count": 2,
                "university_proximity": [{"name": "Bharati Vidyapeeth", "distance_km": 2.5}],
                "amenities": [],
                "photos": PHOTOS_MAP["cozy_room"],
            },
        ]

        for item in listings_seed:
            # Check if title already seeded
            exists = (await session.execute(select(Listing).where(Listing.title == item["title"]))).scalars().first()
            if exists:
                print(f"Listing exists: {item['title']}")
                continue

            amenity_objs = [all_amenities[a_name] for a_name in item["amenities"] if a_name in all_amenities]
            new_listing = Listing(
                landlord_id=item["landlord_id"],
                title=item["title"],
                description=item["description"],
                property_type=item["property_type"],
                rent_amount=item["rent_amount"],
                deposit_amount=item["deposit_amount"],
                rent_period=item["rent_period"],
                city=item["city"],
                locality=item["locality"],
                address_line1=item["address_line1"],
                state=item["state"],
                pincode=item["pincode"],
                gender_preference=item["gender_preference"],
                furnished_status=item["furnished_status"],
                available_from=item["available_from"],
                min_stay_months=item["min_stay_months"],
                max_occupancy=item["max_occupancy"],
                status=item["status"],
                rejection_reason=item.get("rejection_reason"),
                views_count=item["views_count"],
                university_proximity=item["university_proximity"],
                amenities=amenity_objs,
            )
            session.add(new_listing)
            await session.flush()
            await session.refresh(new_listing)

            # Add photos
            for idx, photo_url in enumerate(item["photos"]):
                p = ListingPhoto(
                    listing_id=new_listing.id,
                    url=photo_url,
                    is_cover=(idx == 0),
                    sort_order=idx,
                )
                session.add(p)

            print(f"Created Listing: {item['title']} in {item['city']} ({len(item['photos'])} photos)")

        await session.commit()

    print("=" * 60)
    print("DEMO DATA SEEDING COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(seed())
