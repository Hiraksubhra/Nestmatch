import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_flatmate_profile_crud_and_search(client: AsyncClient, db_session: AsyncSession):
    # 1. Register student A
    user_a_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "student_a@test.com",
            "password": "Password123!",
            "full_name": "Aanya Sharma",
            "role": "STUDENT",
        }
    )
    assert user_a_res.status_code == 201
    token_a = user_a_res.json()["data"]["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Register student B
    user_b_res = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "student_b@test.com",
            "password": "Password123!",
            "full_name": "Priya Patel",
            "role": "STUDENT",
        }
    )
    assert user_b_res.status_code == 201
    token_b = user_b_res.json()["data"]["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. Student A creates flatmate profile
    profile_a_res = await client.post(
        "/api/v1/flatmates",
        headers=headers_a,
        json={
            "budget_min": 6000,
            "budget_max": 12000,
            "preferred_city": "Pune",
            "preferred_university": "Pune University",
            "preferred_locality": "Kothrud",
            "move_in_date": "2026-11-01",
            "move_in_flexibility": 7,
            "gender": "FEMALE",
            "bio": "First year CS undergrad looking for a clean, vegetarian flatmate.",
            "lifestyle_tags": ["early_riser", "vegetarian", "non_smoker", "studious"]
        }
    )
    assert profile_a_res.status_code == 200
    assert profile_a_res.json()["success"] is True
    data_a = profile_a_res.json()["data"]
    assert float(data_a["budget_max"]) == 12000.0
    assert data_a["preferred_city"] == "Pune"
    assert len(data_a["lifestyle_tags"]) == 4

    # 4. Fetch own profile via /flatmates/me
    my_profile_res = await client.get("/api/v1/flatmates/me", headers=headers_a)
    assert my_profile_res.status_code == 200
    assert my_profile_res.json()["data"]["user_id"] == data_a["user_id"]

    # 5. Student B creates profile with similar preferences
    profile_b_res = await client.post(
        "/api/v1/flatmates",
        headers=headers_b,
        json={
            "budget_min": 7000,
            "budget_max": 14000,
            "preferred_city": "Pune",
            "preferred_university": "Pune University",
            "preferred_locality": "Kothrud",
            "move_in_date": "2026-11-05",
            "move_in_flexibility": 10,
            "gender": "FEMALE",
            "bio": "Quiet, friendly master's student.",
            "lifestyle_tags": ["early_riser", "vegetarian", "studious"]
        }
    )
    assert profile_b_res.status_code == 200
    profile_b_id = profile_b_res.json()["data"]["id"]

    # 6. Student A searches flatmates -> should find Student B with high compatibility score
    search_res = await client.get("/api/v1/flatmates?city=Pune", headers=headers_a)
    assert search_res.status_code == 200
    results = search_res.json()["data"]
    assert len(results) == 1
    matched = results[0]
    assert matched["id"] == profile_b_id
    # High score due to shared city, uni, overlapping budget, and 3 shared tags
    assert matched["compatibility_score"] is not None
    assert matched["compatibility_score"] >= 70

    # 7. Student A views Student B's profile directly
    detail_res = await client.get(f"/api/v1/flatmates/{profile_b_id}", headers=headers_a)
    assert detail_res.status_code == 200
    assert detail_res.json()["data"]["compatibility_score"] >= 70

    # 8. Deactivate profile
    deactivate_res = await client.delete("/api/v1/flatmates/me", headers=headers_b)
    assert deactivate_res.status_code == 200

    # 9. Search again -> deactivated profile should not appear in active search
    search_after_res = await client.get("/api/v1/flatmates?city=Pune", headers=headers_a)
    assert len(search_after_res.json()["data"]) == 0
