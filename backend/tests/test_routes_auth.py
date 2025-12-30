"""Tests for authentication API routes."""

import pytest
from httpx import AsyncClient


class TestRegisterEndpoint:
    """Test suite for POST /api/auth/register endpoint."""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient, sample_user_data: dict):
        """Test successful user registration."""
        response = await client.post("/api/auth/register", json=sample_user_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == sample_user_data["email"]
        assert "password" not in data
        assert "password_hash" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, sample_user_data: dict):
        """Test registration with duplicate email."""
        # First registration
        await client.post("/api/auth/register", json=sample_user_data)

        # Second registration with same email
        response = await client.post("/api/auth/register", json=sample_user_data)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email format."""
        invalid_data = {
            "email": "not-an-email",
            "password": "SecurePass123!",
        }
        response = await client.post("/api/auth/register", json=invalid_data)

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_email(self, client: AsyncClient):
        """Test registration without email."""
        response = await client.post(
            "/api/auth/register",
            json={"password": "SecurePass123!"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_password(self, client: AsyncClient):
        """Test registration without password."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "test@example.com"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_short_password(self, client: AsyncClient):
        """Test registration with too short password."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "test@example.com", "password": "123"}
        )

        assert response.status_code == 422


class TestLoginEndpoint:
    """Test suite for POST /api/auth/login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, sample_user_data: dict):
        """Test successful login."""
        # Register first
        await client.post("/api/auth/register", json=sample_user_data)

        # Login
        response = await client.post("/api/auth/login", json=sample_user_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, sample_user_data: dict):
        """Test login with wrong password."""
        # Register first
        await client.post("/api/auth/register", json=sample_user_data)

        # Login with wrong password
        wrong_data = {
            "email": sample_user_data["email"],
            "password": "WrongPassword123!",
        }
        response = await client.post("/api/auth/login", json=wrong_data)

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, client: AsyncClient):
        """Test login with non-existent user."""
        response = await client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_missing_fields(self, client: AsyncClient):
        """Test login with missing fields."""
        response = await client.post("/api/auth/login", json={})

        assert response.status_code == 422


class TestMeEndpoint:
    """Test suite for GET /api/auth/me endpoint."""

    @pytest.mark.asyncio
    async def test_me_authenticated(self, client: AsyncClient, sample_user_data: dict):
        """Test getting current user when authenticated."""
        # Register and login
        await client.post("/api/auth/register", json=sample_user_data)
        login_response = await client.post("/api/auth/login", json=sample_user_data)
        token = login_response.json()["access_token"]

        # Get current user
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert "password" not in data
        assert "password_hash" not in data

    @pytest.mark.asyncio
    async def test_me_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/auth/me")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_me_malformed_auth_header(self, client: AsyncClient):
        """Test getting current user with malformed auth header."""
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "NotBearer token"}
        )

        assert response.status_code == 401
