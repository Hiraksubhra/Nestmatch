import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import seed_amenities


@pytest.mark.asyncio
async def test_booking_request_lifecycle(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)

    # 1. Register landlord
    landlord_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "landlord_book@test.com",
            "password": "Password123!",
            "full_name": "Suresh Landlord",
            "phone": "+91 98765 43210",
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
            "email": "student_book@test.com",
            "password": "Password123!",
            "full_name": "Rohan Student",
            "phone": "+91 91234 56789",
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
            "email": "admin_book@test.com",
            "password": "Password123!",
            "full_name": "Admin Controller",
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
            "title": "Viman Nagar Student Flat",
            "property_type": "APARTMENT",
            "rent_amount": 12000.0,
            "city": "Pune",
            "locality": "Viman Nagar",
            "gender_preference": "ANY",
            "furnished_status": "FURNISHED",
            "min_stay_months": 6,
            "max_occupancy": 2,
        }
    )
    assert listing_res.status_code == 201
    listing_id = listing_res.json()["data"]["id"]

    move_in = (date.today() + timedelta(days=14)).isoformat()

    # 5. Cannot book listing before approval
    book_fail_res = await client.post(
        "/api/v1/bookings",
        headers=student_headers,
        json={
            "listing_id": listing_id,
            "move_in_date": move_in,
            "duration_months": 6,
            "message": "Looking forward to moving in!"
        }
    )
    assert book_fail_res.status_code == 400

    # 6. Admin approves listing
    approve_res = await client.put(
        f"/api/v1/admin/listings/{listing_id}/approve",
        headers=admin_headers
    )
    assert approve_res.status_code == 200

    # 7. Landlord cannot book their own listing
    landlord_book = await client.post(
        "/api/v1/bookings",
        headers=landlord_headers,
        json={
            "listing_id": listing_id,
            "move_in_date": move_in,
            "duration_months": 6
        }
    )
    # Role checker restricts POST /bookings to STUDENT role
    assert landlord_book.status_code == 403

    # 8. Student books approved listing
    book_res = await client.post(
        "/api/v1/bookings",
        headers=student_headers,
        json={
            "listing_id": listing_id,
            "move_in_date": move_in,
            "duration_months": 6,
            "message": "Hi Suresh, excited about this place."
        }
    )
    assert book_res.status_code == 201
    booking_data = book_res.json()["data"]
    booking_id = booking_data["id"]
    assert booking_data["status"] == "PENDING"
    # Contacts should NOT be revealed while PENDING
    assert booking_data["landlord_contact"] is None

    # 9. Duplicate booking raises conflict
    dup_book = await client.post(
        "/api/v1/bookings",
        headers=student_headers,
        json={
            "listing_id": listing_id,
            "move_in_date": move_in,
            "duration_months": 6
        }
    )
    assert dup_book.status_code == 409

    # 10. Landlord views booking requests
    landlord_list = await client.get("/api/v1/bookings", headers=landlord_headers)
    assert landlord_list.status_code == 200
    assert len(landlord_list.json()["data"]) == 1

    # 11. Landlord accepts booking
    accept_res = await client.put(f"/api/v1/bookings/{booking_id}/accept", headers=landlord_headers)
    assert accept_res.status_code == 200
    accepted_data = accept_res.json()["data"]
    assert accepted_data["status"] == "ACCEPTED"
    assert accepted_data["responded_at"] is not None
    # Now contacts ARE revealed
    assert accepted_data["landlord_contact"]["email"] == "landlord_book@test.com"
    assert accepted_data["landlord_contact"]["phone"] == "+91 98765 43210"
    assert accepted_data["student_contact"]["email"] == "student_book@test.com"

    # 12. Check conversation has system message regarding booking
    convs = await client.get("/api/v1/conversations", headers=student_headers)
    assert convs.status_code == 200
    assert len(convs.json()["data"]) == 1
    conv_id = convs.json()["data"][0]["id"]

    msgs = await client.get(f"/api/v1/conversations/{conv_id}/messages", headers=student_headers)
    assert msgs.status_code == 200
    contents = [m["content"] for m in msgs.json()["data"]]
    assert any("New Booking Request" in c for c in contents)
    assert any("Booking Request Accepted" in c for c in contents)
