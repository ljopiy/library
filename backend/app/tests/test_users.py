import pytest
from starlette import status

@pytest.mark.asyncio
async def test_register_success(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "123456",
            "full_name": "Test User",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client):
    await async_client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "123456",
            "full_name": "Test User",
        },
    )
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "123456",
            "full_name": "Another User",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] in (
        "Email already registered",
        "User with this email already exists",
    )


@pytest.mark.asyncio
async def test_login_success(async_client):
    await async_client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "mypassword",
            "full_name": "Login User",
        },
    )
    response = await async_client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "mypassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client):
    await async_client.post(
        "/auth/register",
        json={
            "email": "wrongpass@example.com",
            "password": "correctpass",
            "full_name": "Wrong Pass",
        },
    )
    response = await async_client.post(
        "/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "wrongpass",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] in (
        "Invalid credentials",
        "Incorrect email or password",
    )
