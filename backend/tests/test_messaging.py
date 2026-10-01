import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.init_db import seed_amenities


@pytest.mark.asyncio
async def test_messaging_flow(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)

    # 1. Register landlord
    landlord_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "landlord_msg@test.com",
            "password": "Password123!",
            "full_name": "Ramesh Landlord",
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
            "email": "student_msg@test.com",
            "password": "Password123!",
            "full_name": "Aarav Student",
            "role": "STUDENT",
        }
    )
    assert student_res.status_code == 201
    student_token = student_res.json()["data"]["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 3. Register another student (unauthorized third-party)
    other_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "other_student@test.com",
            "password": "Password123!",
            "full_name": "Other Student",
            "role": "STUDENT",
        }
    )
    other_token = other_res.json()["data"]["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}

    # 4. Landlord creates listing
    listing_res = await client.post(
        "/api/v1/listings",
        headers=landlord_headers,
        json={
            "title": "Kothrud Student PG Room",
            "property_type": "PG",
            "rent_amount": 7500.0,
            "city": "Pune",
            "locality": "Kothrud",
            "gender_preference": "ANY",
            "furnished_status": "FURNISHED",
            "min_stay_months": 3,
            "max_occupancy": 1,
        }
    )
    assert listing_res.status_code == 201
    listing_id = listing_res.json()["data"]["id"]

    # 5. Landlord cannot start conversation with self
    self_conv_res = await client.post(
        "/api/v1/conversations",
        headers=landlord_headers,
        json={"listing_id": listing_id}
    )
    assert self_conv_res.status_code == 400

    # 6. Student starts conversation
    conv_res = await client.post(
        "/api/v1/conversations",
        headers=student_headers,
        json={
            "listing_id": listing_id,
            "initial_message": "Hi, is this room still available for next semester?"
        }
    )
    assert conv_res.status_code == 201
    conv_data = conv_res.json()["data"]
    conv_id = conv_data["id"]
    assert conv_data["listing_id"] == listing_id

    # 7. Check message history has the initial message
    msgs_res = await client.get(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=student_headers
    )
    assert msgs_res.status_code == 200
    msgs = msgs_res.json()["data"]
    assert len(msgs) == 1
    assert msgs[0]["content"] == "Hi, is this room still available for next semester?"

    # 8. Landlord views conversation list and responds
    landlord_convs = await client.get("/api/v1/conversations", headers=landlord_headers)
    assert landlord_convs.status_code == 200
    assert len(landlord_convs.json()["data"]) == 1
    assert landlord_convs.json()["data"][0]["unread_count"] == 1

    reply_res = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=landlord_headers,
        json={"content": "Yes, it is! Would you like to schedule a visit?"}
    )
    assert reply_res.status_code == 201

    # 9. Mark messages as read by student
    read_res = await client.put(f"/api/v1/conversations/{conv_id}/read", headers=student_headers)
    assert read_res.status_code == 200

    # 10. Third-party student cannot view conversation or messages
    unauth_view = await client.get(f"/api/v1/conversations/{conv_id}", headers=other_headers)
    assert unauth_view.status_code == 403

    unauth_send = await client.post(
        f"/api/v1/conversations/{conv_id}/messages",
        headers=other_headers,
        json={"content": "I want to intrude!"}
    )
    assert unauth_send.status_code == 403
