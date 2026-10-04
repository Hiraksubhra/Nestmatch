
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
from app.models.campus import Campus
from app.services.campus_service import CampusService
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

        # 1.8 Seed Verified University Campuses (PostGIS Geotracking Anchors)
        campuses_seed = [
            # Pune
            {
                "id": "c-coep-pune",
                "name": "COEP Technological University",
                "short_name": "COEP Tech",
                "city": "Pune",
                "locality": "Shivajinagar",
                "latitude": Decimal("18.5293000"),
                "longitude": Decimal("73.8565000"),
            },
            {
                "id": "c-sppu-pune",
                "name": "Savitribai Phule Pune University",
                "short_name": "Pune University",
                "city": "Pune",
                "locality": "Ganeshkhind",
                "latitude": Decimal("18.5529000"),
                "longitude": Decimal("73.8227000"),
            },
            {
                "id": "c-symbiosis-viman",
                "name": "Symbiosis International University (Viman Nagar)",
                "short_name": "Symbiosis Viman Nagar",
                "city": "Pune",
                "locality": "Viman Nagar",
                "latitude": Decimal("18.5636000"),
                "longitude": Decimal("73.9114000"),
            },
            {
                "id": "c-fergusson-pune",
                "name": "Fergusson College",
                "short_name": "Fergusson",
                "city": "Pune",
                "locality": "Shivajinagar",
                "latitude": Decimal("18.5222000"),
                "longitude": Decimal("73.8407000"),
            },
            {
                "id": "c-mit-wpu-pune",
                "name": "MIT World Peace University",
                "short_name": "MIT-WPU",
                "city": "Pune",
                "locality": "Kothrud",
                "latitude": Decimal("18.5186000"),
                "longitude": Decimal("73.8154000"),
            },
            {
                "id": "c-bharati-pune",
                "name": "Bharati Vidyapeeth Deemed University",
                "short_name": "Bharati Vidyapeeth",
                "city": "Pune",
                "locality": "Dhankawadi",
                "latitude": Decimal("18.4575000"),
                "longitude": Decimal("73.8508000"),
            },
            # Mumbai
            {
                "id": "c-iit-bombay",
                "name": "IIT Bombay",
                "short_name": "IIT Bombay",
                "city": "Mumbai",
                "locality": "Powai",
                "latitude": Decimal("19.1334000"),
                "longitude": Decimal("72.9133000"),
            },
            {
                "id": "c-mu-kalina",
                "name": "Mumbai University (Kalina Campus)",
                "short_name": "Mumbai University",
                "city": "Mumbai",
                "locality": "Santacruz East",
                "latitude": Decimal("19.0728000"),
                "longitude": Decimal("72.8596000"),
            },
            {
                "id": "c-nmims-mumbai",
                "name": "NMIMS Mumbai",
                "short_name": "NMIMS",
                "city": "Mumbai",
                "locality": "Vile Parle West",
                "latitude": Decimal("19.1032000"),
                "longitude": Decimal("72.8370000"),
            },
            # Bangalore
            {
                "id": "c-iisc-bangalore",
                "name": "Indian Institute of Science (IISc)",
                "short_name": "IISc Bangalore",
                "city": "Bangalore",
                "locality": "Malleshwaram",
                "latitude": Decimal("13.0219000"),
                "longitude": Decimal("77.5671000"),
            },
            {
                "id": "c-christ-bangalore",
                "name": "Christ University (Central Campus)",
                "short_name": "Christ University",
                "city": "Bangalore",
                "locality": "Hosur Road",
                "latitude": Decimal("12.9344000"),
                "longitude": Decimal("77.6060000"),
            },
            {
                "id": "c-nift-bangalore",
                "name": "National Institute of Fashion Technology",
                "short_name": "NIFT Bengaluru",
                "city": "Bangalore",
                "locality": "HSR Layout",
                "latitude": Decimal("12.9128000"),
                "longitude": Decimal("77.6517000"),
            },
            # Delhi
            {
                "id": "c-du-north",
                "name": "Delhi University (North Campus)",
                "short_name": "DU North Campus",
                "city": "Delhi",
                "locality": "University Enclave",
                "latitude": Decimal("28.6892000"),
                "longitude": Decimal("77.2096000"),
            },
            {
                "id": "c-iit-delhi",
                "name": "IIT Delhi",
                "short_name": "IIT Delhi",
                "city": "Delhi",
                "locality": "Hauz Khas",
                "latitude": Decimal("28.5450000"),
                "longitude": Decimal("77.1926000"),
            },
        ]

        for c_data in campuses_seed:
            existing_c = (await session.execute(select(Campus).where(Campus.id == c_data["id"]))).scalars().first()
            if not existing_c:
                c_obj = Campus(
                    id=c_data["id"],
                    name=c_data["name"],
                    short_name=c_data["short_name"],
                    city=c_data["city"],
                    locality=c_data["locality"],
                    latitude=c_data["latitude"],
                    longitude=c_data["longitude"],
                    location=f"POINT({c_data['longitude']} {c_data['latitude']})",
                )
                session.add(c_obj)
                print(f"Created Campus: {c_data['name']} in {c_data['city']}")
            else:
                existing_c.latitude = c_data["latitude"]
                existing_c.longitude = c_data["longitude"]
                existing_c.location = f"POINT({c_data['longitude']} {c_data['latitude']})"

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
                "latitude": Decimal("18.5678000"),
                "longitude": Decimal("73.9142000"),
                "gender_preference": GenderPreference.FEMALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 84,
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
                "latitude": Decimal("18.5245000"),
                "longitude": Decimal("73.8420000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 128,
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
                "latitude": Decimal("18.5610000"),
                "longitude": Decimal("73.8115000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 67,
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
                "latitude": Decimal("12.9385000"),
                "longitude": Decimal("77.6110000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 210,
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
                "latitude": Decimal("12.9165000"),
                "longitude": Decimal("77.6440000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.SEMI.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 55,
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
                "latitude": Decimal("28.6815000"),
                "longitude": Decimal("77.2030000"),
                "gender_preference": GenderPreference.FEMALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 315,
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
                "latitude": Decimal("19.1280000"),
                "longitude": Decimal("72.9090000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 182,
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
                "latitude": Decimal("25.1388000"),
                "longitude": Decimal("75.8450000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 9,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 94,
                "amenities": ["wifi", "food_included", "study_desk", "ro_water", "security", "geyser"],
                "photos": PHOTOS_MAP["cozy_room"],
            },
            # 1. COEP Tech (Pune)
            {
                "landlord_id": rajesh.id,
                "title": "COEP Engineers Hub - Twin Sharing Study Rooms",
                "description": "Designed specifically for engineering students at COEP. Located just 300 meters from the COEP main academic wing. High-speed 300 Mbps fiber internet, ergonomic study desks with reading lamps, power backup for continuous project work, and quiet study hours.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("8000.00"),
                "deposit_amount": Decimal("15000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Shivajinagar",
                "address_line1": "Near Sancheti Hospital, Shivajinagar",
                "state": "Maharashtra",
                "pincode": "411005",
                "latitude": Decimal("18.5310000"),
                "longitude": Decimal("73.8540000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 142,
                "amenities": ["wifi", "study_desk", "power_backup", "laundry", "ro_water", "security"],
                "photos": PHOTOS_MAP["pg_modern"],
            },
            # 2. MIT-WPU (Pune)
            {
                "landlord_id": sunita.id,
                "title": "MIT-WPU Scholars Nest - Furnished 1BHK",
                "description": "Bright and airy 1BHK apartment situated 4 minutes walk from MIT World Peace University campus. Fully equipped kitchen, private balcony, silent reading environment, and high security society with CCTV surveillance.",
                "property_type": PropertyType.APARTMENT.value,
                "rent_amount": Decimal("12500.00"),
                "deposit_amount": Decimal("25000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Kothrud",
                "address_line1": "Near MIT School Gate, Paud Road, Kothrud",
                "state": "Maharashtra",
                "pincode": "411038",
                "latitude": Decimal("18.5165000"),
                "longitude": Decimal("73.8175000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 188,
                "amenities": ["wifi", "attached_washroom", "refrigerator", "study_desk", "geyser", "parking"],
                "photos": PHOTOS_MAP["apartment"],
            },
            # 3. Bharati Vidyapeeth (Pune)
            {
                "landlord_id": rajesh.id,
                "title": "Bharati Vidyapeeth Medico & Tech PG",
                "description": "Homely PG accommodation walking distance from Bharati Vidyapeeth medical and engineering faculties. Includes 3 nutritious home-style meals daily, hot water 24/7, high speed Wi-Fi, and regular housekeeping.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("7500.00"),
                "deposit_amount": Decimal("12000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Dhankawadi",
                "address_line1": "Near Bharati Hospital, Katraj-Dhankawadi Road",
                "state": "Maharashtra",
                "pincode": "411043",
                "latitude": Decimal("18.4550000"),
                "longitude": Decimal("73.8525000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 98,
                "amenities": ["wifi", "food_included", "ro_water", "study_desk", "housekeeping", "security", "geyser"],
                "photos": PHOTOS_MAP["cozy_room"],
            },
            # 4. SPPU Pune University (Pune)
            {
                "landlord_id": sunita.id,
                "title": "University Gate Girls PG - Ganeshkhind",
                "description": "Safe, serene student accommodation right opposite Savitribai Phule Pune University main campus gate. Three vegetarian home-cooked meals included, biometric access, warden assistance, and spacious study tables.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("9500.00"),
                "deposit_amount": Decimal("15000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Pune",
                "locality": "Ganeshkhind",
                "address_line1": "Opposite SPPU Main Gate, Ganeshkhind Road",
                "state": "Maharashtra",
                "pincode": "411007",
                "latitude": Decimal("18.5510000"),
                "longitude": Decimal("73.8250000"),
                "gender_preference": GenderPreference.FEMALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 164,
                "amenities": ["wifi", "food_included", "security", "geyser", "study_desk", "housekeeping"],
                "photos": PHOTOS_MAP["pg_modern"],
            },
            # 5. Mumbai University Kalina (Mumbai)
            {
                "landlord_id": vikram.id,
                "title": "Kalina Campus Haven - Shared Student Flat",
                "description": "Modern flat within 5 minutes walking distance of Mumbai University Kalina campus. Ideal for law, arts, and science graduate students. Air conditioned bedrooms, high-speed Wi-Fi, washing machine, and 24/7 security.",
                "property_type": PropertyType.SHARED_ROOM.value,
                "rent_amount": Decimal("13000.00"),
                "deposit_amount": Decimal("25000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Mumbai",
                "locality": "Santacruz East",
                "address_line1": "CST Road, Kalina, Santacruz East",
                "state": "Maharashtra",
                "pincode": "400098",
                "latitude": Decimal("19.0750000"),
                "longitude": Decimal("72.8615000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 115,
                "amenities": ["wifi", "ac", "laundry", "security", "power_backup", "refrigerator"],
                "photos": PHOTOS_MAP["apartment"],
            },
            # 6. NMIMS Mumbai (Mumbai)
            {
                "landlord_id": vikram.id,
                "title": "NMIMS Executive Student Suites - AC Single Room",
                "description": "Luxury private studio accommodation tailored for NMIMS MBA and undergraduate scholars. 350 meters from NMIMS campus gate. Air-conditioned, daily housekeeping, high-speed fiber internet, and premium mattress.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("21000.00"),
                "deposit_amount": Decimal("35000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Mumbai",
                "locality": "Vile Parle West",
                "address_line1": "JVPD Scheme, Near NMIMS, Vile Parle West",
                "state": "Maharashtra",
                "pincode": "400056",
                "latitude": Decimal("19.1015000"),
                "longitude": Decimal("72.8355000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 275,
                "amenities": ["wifi", "ac", "housekeeping", "food_included", "gym", "security", "study_desk"],
                "photos": PHOTOS_MAP["studio"],
            },
            # 7. IIT Bombay (Mumbai)
            {
                "landlord_id": vikram.id,
                "title": "Powai Techies & Researchers Shared PG",
                "description": "Comfortable, quiet PG right outside IIT Bombay Y-Point gate. Zero commute time to laboratories and lecture halls. Includes fiber internet, nutritious breakfast and dinner, and dedicated silent study hours.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("11000.00"),
                "deposit_amount": Decimal("20000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Mumbai",
                "locality": "Powai",
                "address_line1": "Near IIT Main Gate, Powai",
                "state": "Maharashtra",
                "pincode": "400076",
                "latitude": Decimal("19.1315000"),
                "longitude": Decimal("72.9160000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 195,
                "amenities": ["wifi", "laundry", "food_included", "ro_water", "study_desk", "security"],
                "photos": PHOTOS_MAP["cozy_room"],
            },
            # 8. IISc Bangalore (Bangalore)
            {
                "landlord_id": sunita.id,
                "title": "IISc Research Scholars Studio - Malleshwaram",
                "description": "Quiet, green, independent studio apartment 400 meters from IISc Bangalore campus gate. Features dedicated work desk, uninterrupted power backup, high-speed WiFi, attached bath, and peaceful reading environment.",
                "property_type": PropertyType.STUDIO.value,
                "rent_amount": Decimal("16500.00"),
                "deposit_amount": Decimal("30000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Bengaluru",
                "locality": "Malleshwaram",
                "address_line1": "15th Cross, Near IISc Circle, Malleshwaram",
                "state": "Karnataka",
                "pincode": "560003",
                "latitude": Decimal("13.0195000"),
                "longitude": Decimal("77.5695000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 160,
                "amenities": ["wifi", "power_backup", "attached_washroom", "refrigerator", "study_desk", "ro_water"],
                "photos": PHOTOS_MAP["studio"],
            },
            # 9. Christ University (Bangalore)
            {
                "landlord_id": sunita.id,
                "title": "Christ Uni Campus Edge Boys Hostel",
                "description": "Directly facing Christ University Central Campus on Hosur Road. 2 minutes walk to morning lectures. Includes 3 South and North Indian meals, study room, laundry service, and biometric secure entry.",
                "property_type": PropertyType.PG.value,
                "rent_amount": Decimal("11000.00"),
                "deposit_amount": Decimal("18000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Bengaluru",
                "locality": "Hosur Road",
                "address_line1": "Opposite Christ University, Hosur Road",
                "state": "Karnataka",
                "pincode": "560029",
                "latitude": Decimal("12.9330000"),
                "longitude": Decimal("77.6045000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 230,
                "amenities": ["wifi", "food_included", "laundry", "study_desk", "ro_water", "security"],
                "photos": PHOTOS_MAP["pg_modern"],
            },
            # 10. NIFT Bangalore (Bangalore)
            {
                "landlord_id": sunita.id,
                "title": "NIFT Designers Creative Studio - Sector 1",
                "description": "Modern sunlit studio designed with ample floor and desk space for design portfolios and cutting mats. Located 200 meters from NIFT Bengaluru campus. Features split AC, fast WiFi, and attached washroom.",
                "property_type": PropertyType.STUDIO.value,
                "rent_amount": Decimal("15000.00"),
                "deposit_amount": Decimal("25000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Bengaluru",
                "locality": "HSR Layout",
                "address_line1": "19th Main, Sector 1, HSR Layout",
                "state": "Karnataka",
                "pincode": "560102",
                "latitude": Decimal("12.9115000"),
                "longitude": Decimal("77.6530000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 172,
                "amenities": ["wifi", "ac", "attached_washroom", "refrigerator", "parking", "power_backup"],
                "photos": PHOTOS_MAP["studio"],
            },
            # 11. DU North Campus (Delhi)
            {
                "landlord_id": vikram.id,
                "title": "Hudson Lane Student Flat - DU North Campus",
                "description": "Spacious shared student flat in vibrant Hudson Lane, 400m from Delhi University North Campus faculties (SRCC, Hindu, Hansraj, Kirori Mal). AC in all rooms, food delivery hubs nearby, and 24/7 power backup.",
                "property_type": PropertyType.APARTMENT.value,
                "rent_amount": Decimal("14500.00"),
                "deposit_amount": Decimal("20000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Delhi NCR",
                "locality": "Hudson Lane",
                "address_line1": "Hudson Lane, GTB Nagar",
                "state": "Delhi",
                "pincode": "110009",
                "latitude": Decimal("28.6920000"),
                "longitude": Decimal("77.2070000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 340,
                "amenities": ["wifi", "ac", "laundry", "power_backup", "study_desk", "geyser"],
                "photos": PHOTOS_MAP["apartment"],
            },
            # 12. IIT Delhi (Delhi)
            {
                "landlord_id": vikram.id,
                "title": "Hauz Khas Green Suite near IIT Delhi Gate 1",
                "description": "High-end student apartment directly across IIT Delhi Gate 1 and SDA Market. Fully air-conditioned, high-speed fiber internet, power backup, study desks, and serene greenery. 5 minutes walk to IIT lecture hall complex.",
                "property_type": PropertyType.APARTMENT.value,
                "rent_amount": Decimal("18500.00"),
                "deposit_amount": Decimal("35000.00"),
                "rent_period": RentPeriod.MONTHLY.value,
                "city": "Delhi NCR",
                "locality": "Hauz Khas",
                "address_line1": "C-Block, SDA, Hauz Khas",
                "state": "Delhi",
                "pincode": "110016",
                "latitude": Decimal("28.5475000"),
                "longitude": Decimal("77.1950000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.FURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 6,
                "max_occupancy": 2,
                "status": ListingStatus.ACTIVE.value,
                "views_count": 290,
                "amenities": ["wifi", "ac", "power_backup", "security", "laundry", "gym", "parking"],
                "photos": PHOTOS_MAP["apartment"],
            },
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
                "latitude": Decimal("18.5140000"),
                "longitude": Decimal("73.8110000"),
                "gender_preference": GenderPreference.ANY.value,
                "furnished_status": FurnishedStatus.SEMI.value,
                "available_from": date.today(),
                "min_stay_months": 3,
                "max_occupancy": 1,
                "status": ListingStatus.PENDING_VERIFICATION.value,
                "views_count": 4,
                "amenities": ["wifi", "water_purifier", "parking"],
                "photos": PHOTOS_MAP["local_assets"],
            },
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
                "latitude": Decimal("18.4610000"),
                "longitude": Decimal("73.8540000"),
                "gender_preference": GenderPreference.MALE.value,
                "furnished_status": FurnishedStatus.UNFURNISHED.value,
                "available_from": date.today(),
                "min_stay_months": 1,
                "max_occupancy": 1,
                "status": ListingStatus.REJECTED.value,
                "rejection_reason": "Listing rejected: basement lacks adequate natural ventilation and fire escape compliance.",
                "views_count": 2,
                "amenities": [],
                "photos": PHOTOS_MAP["cozy_room"],
            },
        ]

        for item in listings_seed:
            exists = (await session.execute(select(Listing).where(Listing.title == item["title"]))).scalars().first()
            if exists:
                if "latitude" in item and "longitude" in item:
                    exists.latitude = item["latitude"]
                    exists.longitude = item["longitude"]
                    exists.location = f"POINT({item['longitude']} {item['latitude']})"
                    await CampusService.enrich_listing_proximity(session, exists)
                    await session.flush()
                print(f"Listing updated/exists: {item['title']}")
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
                latitude=item.get("latitude"),
                longitude=item.get("longitude"),
                location=f"POINT({item['longitude']} {item['latitude']})" if "latitude" in item else None,
                gender_preference=item["gender_preference"],
                furnished_status=item["furnished_status"],
                available_from=item["available_from"],
                min_stay_months=item["min_stay_months"],
                max_occupancy=item["max_occupancy"],
                status=item["status"],
                rejection_reason=item.get("rejection_reason"),
                views_count=item["views_count"],
                amenities=amenity_objs,
            )
            session.add(new_listing)
            await session.flush()
            # Enrich dynamic campus proximity using PostGIS engine
            await CampusService.enrich_listing_proximity(session, new_listing)
            await session.flush()

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
