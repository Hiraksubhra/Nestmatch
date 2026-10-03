import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.init_db import seed_amenities
from app.models.user import User


@pytest.mark.asyncio
async def test_reporting_students_and_landlords(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)

    # 1. Register landlord
    landlord_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "landlord_rep@test.com",
            "password": "Password123!",
            "full_name": "Ramesh Landlord",
            "role": "LANDLORD",
        }
    )
    assert landlord_res.status_code == 201
    landlord_data = landlord_res.json()["data"]["user"]
    landlord_id = landlord_data["id"]
    landlord_token = landlord_res.json()["data"]["access_token"]
    landlord_headers = {"Authorization": f"Bearer {landlord_token}"}

    # 2. Register student 1
    student1_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "student1_rep@test.com",
            "password": "Password123!",
            "full_name": "Aarav Student",
            "role": "STUDENT",
        }
    )
    assert student1_res.status_code == 201
    student1_data = student1_res.json()["data"]["user"]
    student1_id = student1_data["id"]
    student1_token = student1_res.json()["data"]["access_token"]
    student1_headers = {"Authorization": f"Bearer {student1_token}"}

    # 3. Register student 2
    student2_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "student2_rep@test.com",
            "password": "Password123!",
            "full_name": "Diya Student",
            "role": "STUDENT",
        }
    )
    assert student2_res.status_code == 201
    student2_data = student2_res.json()["data"]["user"]
    student2_id = student2_data["id"]
    student2_token = student2_res.json()["data"]["access_token"]
    student2_headers = {"Authorization": f"Bearer {student2_token}"}

    # 4. Test GET /reports/reasons
    reasons_res = await client.get("/api/v1/reports/reasons")
    assert reasons_res.status_code == 200
    reasons = reasons_res.json()["data"]
    assert len(reasons) >= 5
    assert any(r["key"] == "INAPPROPRIATE_BEHAVIOUR" for r in reasons)
    assert any(r["key"] == "FRAUD_OR_SCAM" for r in reasons)

    # 5. Student 1 reports Landlord for fraudulent behaviour
    report_landlord_res = await client.post(
        "/api/v1/reports",
        headers=student1_headers,
        json={
            "reported_user_id": landlord_id,
            "reason": "FRAUD_OR_SCAM",
            "details": "Landlord demanded an offline cash deposit before viewings.",
        }
    )
    assert report_landlord_res.status_code == 201
    report_landlord_data = report_landlord_res.json()["data"]
    assert report_landlord_data["reporter_id"] == student1_id
    assert report_landlord_data["reported_user_id"] == landlord_id
    assert report_landlord_data["reason"] == "FRAUD_OR_SCAM"
    assert report_landlord_data["status"] == "PENDING"

    # 6. Duplicate pending report prevention
    dup_res = await client.post(
        "/api/v1/reports",
        headers=student1_headers,
        json={
            "reported_user_id": landlord_id,
            "reason": "FRAUD_OR_SCAM",
            "details": "Trying again immediately.",
        }
    )
    assert dup_res.status_code == 400
    assert "already submitted a pending report" in dup_res.json()["error"]["message"]

    # 7. Student 1 reports Student 2 for inappropriate behaviour
    report_student_res = await client.post(
        "/api/v1/reports",
        headers=student1_headers,
        json={
            "reported_user_id": student2_id,
            "reason": "INAPPROPRIATE_BEHAVIOUR",
            "details": "Sent offensive and abusive messages in chat.",
        }
    )
    assert report_student_res.status_code == 201
    report_student_data = report_student_res.json()["data"]
    assert report_student_data["reporter_id"] == student1_id
    assert report_student_data["reported_user_id"] == student2_id
    assert report_student_data["reason"] == "INAPPROPRIATE_BEHAVIOUR"

    # 8. Landlord reports Student 1 for inappropriate behaviour
    landlord_report_res = await client.post(
        "/api/v1/reports",
        headers=landlord_headers,
        json={
            "reported_user_id": student1_id,
            "reason": "SPAM",
            "details": "Promoting unrelated commercial links.",
        }
    )
    assert landlord_report_res.status_code == 201

    # 9. Self-reporting is prevented
    self_report_res = await client.post(
        "/api/v1/reports",
        headers=student1_headers,
        json={
            "reported_user_id": student1_id,
            "reason": "INAPPROPRIATE_BEHAVIOUR",
        }
    )
    assert self_report_res.status_code == 400
    assert "cannot report your own profile" in self_report_res.json()["error"]["message"]

    # 10. Non-existent user reporting fails with 404
    missing_user_res = await client.post(
        "/api/v1/reports",
        headers=student1_headers,
        json={
            "reported_user_id": "00000000-0000-0000-0000-000000000000",
            "reason": "OTHER",
        }
    )
    assert missing_user_res.status_code == 404

    # 11. Unauthenticated request fails with 401
    unauth_res = await client.post(
        "/api/v1/reports",
        json={
            "reported_user_id": landlord_id,
            "reason": "OTHER",
        }
    )
    assert unauth_res.status_code == 401


@pytest.mark.asyncio
async def test_shadow_ban_preparedness(client: AsyncClient, db_session: AsyncSession):
    await seed_amenities(db_session)

    # 1. Register landlord & admin
    landlord_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "shadow_landlord@test.com",
            "password": "Password123!",
            "full_name": "Shadow Landlord",
            "role": "LANDLORD",
        }
    )
    landlord_token = landlord_res.json()["data"]["access_token"]
    landlord_id = landlord_res.json()["data"]["user"]["id"]
    landlord_headers = {"Authorization": f"Bearer {landlord_token}"}

    admin_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin_shadow@test.com",
            "password": "Password123!",
            "full_name": "Admin Shadow",
            "role": "ADMIN",
        }
    )
    admin_token = admin_res.json()["data"]["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Create and approve listing
    listing_res = await client.post(
        "/api/v1/listings",
        headers=landlord_headers,
        json={
            "title": "Kothrud Student Haven",
            "description": "Clean PG near MIT",
            "property_type": "PG",
            "rent_amount": 9000,
            "city": "Pune",
            "locality": "Kothrud",
            "gender_preference": "ANY",
            "furnished_status": "FURNISHED",
            "min_stay_months": 3,
            "max_occupancy": 1,
        }
    )
    listing_id = listing_res.json()["data"]["id"]
    await client.put(f"/api/v1/admin/listings/{listing_id}/approve", headers=admin_headers)

    # Verify listing is in public search results
    search_res = await client.get("/api/v1/listings?city=Pune")
    assert search_res.status_code == 200
    listing_ids = [item["id"] for item in search_res.json()["data"]]
    assert listing_id in listing_ids

    # 3. Simulate future admin action: shadow-banning the landlord
    await db_session.execute(
        update(User)
        .where(User.id == landlord_id)
        .values(is_shadow_banned=True, shadow_ban_reason="Repeated scam reports")
    )
    await db_session.commit()

    # Now verify the listing is automatically hidden from public search!
    search_shadow_res = await client.get("/api/v1/listings?city=Pune")
    assert search_shadow_res.status_code == 200
    listing_ids_after = [item["id"] for item in search_shadow_res.json()["data"]]
    assert listing_id not in listing_ids_after

    # However, landlord still sees their own listing in /my (classic shadow ban)
    my_listings_res = await client.get("/api/v1/listings/my", headers=landlord_headers)
    assert my_listings_res.status_code == 200
    my_ids = [item["id"] for item in my_listings_res.json()["data"]]
    assert listing_id in my_ids

    # 4. Test student shadow-ban on Flatmates
    student_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "shadow_student@test.com",
            "password": "Password123!",
            "full_name": "Shadow Student",
            "role": "STUDENT",
        }
    )
    student_token = student_res.json()["data"]["access_token"]
    student_id = student_res.json()["data"]["user"]["id"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # Student creates flatmate profile
    create_prof_res = await client.post(
        "/api/v1/flatmates",
        headers=student_headers,
        json={
            "budget_min": 5000,
            "budget_max": 12000,
            "preferred_city": "Pune",
            "preferred_university": "Pune University",
            "gender": "ANY",
            "lifestyle_tags": ["studious", "non_smoker"],
        }
    )
    assert create_prof_res.status_code == 200

    # Another student searches flatmates
    viewer_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "viewer_student@test.com",
            "password": "Password123!",
            "full_name": "Viewer Student",
            "role": "STUDENT",
        }
    )
    viewer_token = viewer_res.json()["data"]["access_token"]
    viewer_headers = {"Authorization": f"Bearer {viewer_token}"}

    browse_res = await client.get("/api/v1/flatmates?city=Pune", headers=viewer_headers)
    assert browse_res.status_code == 200
    student_ids = [p["user_id"] for p in browse_res.json()["data"]]
    assert student_id in student_ids

    # Simulate future admin action: shadow banning the student
    await db_session.execute(
        update(User)
        .where(User.id == student_id)
        .values(is_shadow_banned=True, shadow_ban_reason="Inappropriate behavior")
    )
    await db_session.commit()

    # Verify shadow-banned student is hidden from public flatmate browse!
    browse_shadow_res = await client.get("/api/v1/flatmates?city=Pune", headers=viewer_headers)
    assert browse_shadow_res.status_code == 200
    student_ids_after = [p["user_id"] for p in browse_shadow_res.json()["data"]]
    assert student_id not in student_ids_after
