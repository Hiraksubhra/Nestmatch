import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import seed_amenities


@pytest.mark.asyncio
async def test_reviews_and_saved_listings(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)

    # 1. Register landlord
    landlord_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "landlord_rev@test.com",
            "password": "Password123!",
            "full_name": "Rakesh Landlord",
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
            "email": "student_rev@test.com",
            "password": "Password123!",
            "full_name": "Kavya Student",
            "role": "STUDENT",
        }
    )
    assert student_res.status_code == 201
    student_token = student_res.json()["data"]["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 3. Register admin
    admin_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin_rev@test.com",
            "password": "Password123!",
            "full_name": "Admin Tester",
            "role": "ADMIN",
        }
    )
    admin_token = admin_res.json()["data"]["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 4. Landlord creates listing
    listing_res = await client.post(
        "/api/v1/listings",
        headers=landlord_headers,
        json={
            "title": "FC Road Premium Studio",
            "description": "Cozy single room near Fergusson College",
            "property_type": "STUDIO",
            "rent_amount": 11000,
            "city": "Pune",
            "locality": "FC Road",
            "gender_preference": "ANY",
            "furnished_status": "FURNISHED",
            "min_stay_months": 3,
            "max_occupancy": 1,
        }
    )
    assert listing_res.status_code == 201
    listing_id = listing_res.json()["data"]["id"]

    # 5. Admin approves listing
    approve_res = await client.put(f"/api/v1/admin/listings/{listing_id}/approve", headers=admin_headers)
    assert approve_res.status_code == 200

    # 6. Test Bookmarks (Saved Listings)
    # Check initial saved listings is empty
    saved_empty_res = await client.get("/api/v1/listings/saved", headers=student_headers)
    assert saved_empty_res.status_code == 200
    assert len(saved_empty_res.json()["data"]) == 0

    # Student saves the listing
    toggle_res = await client.post(f"/api/v1/listings/{listing_id}/save", headers=student_headers)
    assert toggle_res.status_code == 200
    assert toggle_res.json()["data"]["is_saved"] is True

    # Listing detail should now indicate is_saved: true
    detail_res = await client.get(f"/api/v1/listings/{listing_id}", headers=student_headers)
    assert detail_res.status_code == 200
    assert detail_res.json()["data"]["is_saved"] is True

    # Saved listings endpoint should now return 1 listing
    saved_res = await client.get("/api/v1/listings/saved", headers=student_headers)
    assert saved_res.status_code == 200
    assert len(saved_res.json()["data"]) == 1
    assert saved_res.json()["data"][0]["listing_id"] == listing_id

    # Toggle save again -> should unsave
    toggle_again_res = await client.post(f"/api/v1/listings/{listing_id}/save", headers=student_headers)
    assert toggle_again_res.status_code == 200
    assert toggle_again_res.json()["data"]["is_saved"] is False

    # 7. Test Reviews
    # Landlord cannot review own listing
    landlord_rev = await client.post(
        f"/api/v1/listings/{listing_id}/reviews",
        headers=landlord_headers,
        json={"rating": 5, "title": "My own place", "body": "It is great!"}
    )
    assert landlord_rev.status_code == 400

    # Student submits review without accepted booking -> is_verified = False
    review_res = await client.post(
        f"/api/v1/listings/{listing_id}/reviews",
        headers=student_headers,
        json={
            "rating": 5,
            "title": "Fantastic stay for college!",
            "body": "Clean, great high-speed internet, walking distance to campus."
        }
    )
    assert review_res.status_code == 201
    rev_data = review_res.json()["data"]
    assert rev_data["rating"] == 5
    assert rev_data["is_verified"] is False

    # Student tries to submit duplicate review -> 400
    dup_rev = await client.post(
        f"/api/v1/listings/{listing_id}/reviews",
        headers=student_headers,
        json={"rating": 4, "title": "Duplicate"}
    )
    assert dup_rev.status_code == 400

    # Fetch reviews summary for listing
    reviews_summary_res = await client.get(f"/api/v1/listings/{listing_id}/reviews")
    assert reviews_summary_res.status_code == 200
    summary = reviews_summary_res.json()["data"]
    assert summary["total_reviews"] == 1
    assert summary["average_rating"] == 5.0
    assert summary["rating_breakdown"]["5"] == 1 or summary["rating_breakdown"][5] == 1
