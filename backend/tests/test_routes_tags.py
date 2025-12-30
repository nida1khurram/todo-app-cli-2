"""Tests for tags API routes."""

import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, email: str = "test@example.com", password: str = "SecurePass123!") -> str:
    """Helper to register and login a user, returning the auth token."""
    await client.post("/api/auth/register", json={"email": email, "password": password})
    response = await client.post("/api/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


class TestGetTagsEndpoint:
    """Test suite for GET /api/tags endpoint."""

    @pytest.mark.asyncio
    async def test_get_tags_empty_list(self, client: AsyncClient):
        """Test getting tags when none exist."""
        token = await get_auth_token(client)

        response = await client.get(
            "/api/tags",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_tags_returns_user_tags(self, client: AsyncClient):
        """Test getting tags returns only user's tags."""
        token = await get_auth_token(client)

        # Create a tag
        await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token}"}
        )

        response = await client.get(
            "/api/tags",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tags = response.json()
        assert len(tags) == 1
        assert tags[0]["name"] == "work"

    @pytest.mark.asyncio
    async def test_get_tags_with_search(self, client: AsyncClient):
        """Test searching tags by prefix."""
        token = await get_auth_token(client)

        # Create tags
        await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token}"}
        )
        await client.post(
            "/api/tags",
            json={"name": "workout"},
            headers={"Authorization": f"Bearer {token}"}
        )
        await client.post(
            "/api/tags",
            json={"name": "personal"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Search for "work"
        response = await client.get(
            "/api/tags?search=work",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tags = response.json()
        assert len(tags) == 2

    @pytest.mark.asyncio
    async def test_get_tags_unauthorized(self, client: AsyncClient):
        """Test getting tags without authentication."""
        response = await client.get("/api/tags")

        assert response.status_code == 401


class TestCreateTagEndpoint:
    """Test suite for POST /api/tags endpoint."""

    @pytest.mark.asyncio
    async def test_create_tag_success(self, client: AsyncClient):
        """Test successful tag creation."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "work"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_tag_duplicate(self, client: AsyncClient):
        """Test creating duplicate tag."""
        token = await get_auth_token(client)

        # First tag
        await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Duplicate
        response = await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 409

    @pytest.mark.asyncio
    async def test_create_tag_normalizes_name(self, client: AsyncClient):
        """Test that tag names are normalized (lowercase, trimmed)."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tags",
            json={"name": "  WORK  "},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        assert response.json()["name"] == "work"

    @pytest.mark.asyncio
    async def test_create_tag_empty_name(self, client: AsyncClient):
        """Test creating tag with empty name."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tags",
            json={"name": "   "},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422


class TestDeleteTagEndpoint:
    """Test suite for DELETE /api/tags/{tag_id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_tag_success(self, client: AsyncClient):
        """Test successful tag deletion."""
        token = await get_auth_token(client)

        # Create tag
        create_response = await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token}"}
        )
        tag_id = create_response.json()["id"]

        # Delete tag
        response = await client.delete(
            f"/api/tags/{tag_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_tag_not_found(self, client: AsyncClient):
        """Test deleting non-existent tag."""
        token = await get_auth_token(client)

        response = await client.delete(
            "/api/tags/99999",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_tag_other_user(self, client: AsyncClient):
        """Test deleting another user's tag."""
        # User 1 creates tag
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tags",
            json={"name": "work"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        tag_id = create_response.json()["id"]

        # User 2 tries to delete
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.delete(
            f"/api/tags/{tag_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 404
