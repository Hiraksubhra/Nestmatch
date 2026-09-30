import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {
        "email": "aanya@example.com",
        "password": "Password123!",
        "full_name": "Aanya Sharma",
        "role": "STUDENT",
        "phone": "+919876543210"
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert "data" in body
    assert body["data"]["user"]["email"] == "aanya@example.com"
    assert body["data"]["user"]["role"] == "STUDENT"
    assert "access_token" in body["data"]
    assert "refresh_token" in body["data"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123!",
        "full_name": "Test User",
        "role": "STUDENT"
    }
    # First registration
    res1 = await client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    # Second registration should conflict
    res2 = await client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 409
    body = res2.json()
    assert body["success"] is False
    assert body["error"]["code"] == "EMAIL_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_login_flow(client: AsyncClient):
    # Register user first
    reg_payload = {
        "email": "rakesh@example.com",
        "password": "SecurePassword123",
        "full_name": "Rakesh Patel",
        "role": "LANDLORD"
    }
    await client.post("/api/v1/auth/register", json=reg_payload)

    # Login with valid credentials
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "rakesh@example.com",
        "password": "SecurePassword123"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["success"] is True
    access_token = login_data["data"]["access_token"]
    refresh_token = login_data["data"]["refresh_token"]

    # Login with invalid password
    bad_login = await client.post("/api/v1/auth/login", json={
        "email": "rakesh@example.com",
        "password": "WrongPassword"
    })
    assert bad_login.status_code == 401
    assert bad_login.json()["error"]["code"] == "INVALID_CREDENTIALS"

    # Refresh token
    refresh_res = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()["data"]

    # Access current user profile with access token
    headers = {"Authorization": f"Bearer {access_token}"}
    me_res = await client.get("/api/v1/users/me", headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["success"] is True
    assert me_data["data"]["email"] == "rakesh@example.com"
    assert me_data["data"]["role"] == "LANDLORD"

    # Update profile
    update_res = await client.put(
        "/api/v1/users/me",
        headers=headers,
        json={"full_name": "Rakesh K. Patel", "phone": "+919999888877"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["data"]["full_name"] == "Rakesh K. Patel"
    assert update_res.json()["data"]["phone"] == "+919999888877"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "NOT_AUTHENTICATED"
