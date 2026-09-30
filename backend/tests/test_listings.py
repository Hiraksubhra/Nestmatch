import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.listing import Amenity, ListingStatus
from app.db.init_db import seed_amenities


@pytest.mark.asyncio
async def test_amenities_list(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)
    response = await client.get("/api/v1/listings/amenities")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) >= 10


@pytest.mark.asyncio
async def test_create_and_manage_listing(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)

    # 1. Register landlord
    landlord_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "landlord@test.com",
            "password": "Password123!",
            "full_name": "Ramesh Sharma",
            "role": "LANDLORD",
        }
    )
    assert landlord_res.status_code == 201
    landlord_token = landlord_res.json()["data"]["access_token"]
    landlord_headers = {"Authorization": f"Bearer {landlord_token}"}

    # 2. Register student
    student_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "student@test.com",
            "password": "Password123!",
            "full_name": "Aarav Patel",
            "role": "STUDENT",
        }
    )
    student_token = student_res.json()["data"]["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 3. Register admin
    admin_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin@test.com",
            "password": "Password123!",
            "full_name": "Admin User",
            "role": "ADMIN",
        }
    )
    admin_token = admin_res.json()["data"]["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 4. Student tries to create listing -> 403 Forbidden
    payload = {
        "title": "Cozy Single Room near FC College",
        "description": "Spacious room with balcony and attached bath.",
        "property_type": "PG",
        "rent_amount": 8500.0,
        "deposit_amount": 15000.0,
        "rent_period": "MONTHLY",
        "address_line1": "Fergusson College Road, Shivajinagar",
        "city": "Pune",
        "locality": "Shivajinagar",
        "state": "Maharashtra",
        "pincode": "411004",
        "gender_preference": "MALE",
        "furnished_status": "FURNISHED",
        "min_stay_months": 3,
        "max_occupancy": 1,
        "amenity_ids": [1, 2, 4],
    }
    forbidden_res = await client.post("/api/v1/listings", json=payload, headers=student_headers)
    assert forbidden_res.status_code == 403

    # 5. Landlord creates listing -> 201 Created
    create_res = await client.post("/api/v1/listings", json=payload, headers=landlord_headers)
    assert create_res.status_code == 201
    listing_data = create_res.json()["data"]
    listing_id = listing_data["id"]
    assert listing_data["title"] == payload["title"]
    assert listing_data["status"] == ListingStatus.PENDING_VERIFICATION.value
    assert len(listing_data["amenities"]) == 3

    # 6. Landlord checks /listings/my
    my_res = await client.get("/api/v1/listings/my", headers=landlord_headers)
    assert my_res.status_code == 200
    assert len(my_res.json()["data"]) == 1

    # 7. Public search should NOT show pending listing
    search_res = await client.get("/api/v1/listings?city=Pune")
    assert search_res.status_code == 200
    assert len(search_res.json()["data"]) == 0

    # 8. Admin views pending queue
    pending_res = await client.get("/api/v1/admin/listings/pending", headers=admin_headers)
    assert pending_res.status_code == 200
    assert len(pending_res.json()["data"]) == 1

    # 9. Admin approves listing
    approve_res = await client.put(f"/api/v1/admin/listings/{listing_id}/approve", headers=admin_headers)
    assert approve_res.status_code == 200
    assert approve_res.json()["data"]["status"] == ListingStatus.ACTIVE.value

    # 10. Public search now returns the active listing
    search_res2 = await client.get("/api/v1/listings?city=Pune&min_rent=5000&max_rent=10000")
    assert search_res2.status_code == 200
    assert len(search_res2.json()["data"]) == 1
    assert search_res2.json()["data"][0]["id"] == listing_id

    # 11. View listing detail -> checks view increment
    detail_res = await client.get(f"/api/v1/listings/{listing_id}")
    assert detail_res.status_code == 200
    assert detail_res.json()["data"]["views_count"] == 1
