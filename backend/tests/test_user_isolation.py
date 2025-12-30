"""Tests for user data isolation and security."""

import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, email: str, password: str = "SecurePass123!") -> str:
    """Helper to register and login a user, returning the auth token."""
    await client.post("/api/auth/register", json={"email": email, "password": password})
    response = await client.post("/api/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


class TestUserIsolation:
    """Test suite for user data isolation."""

    @pytest.mark.asyncio
    async def test_user_cannot_see_other_user_tasks(self, client: AsyncClient):
        """Test that users cannot see other users' tasks."""
        # User 1 creates tasks
        token1 = await get_auth_token(client, "user1@example.com")
        await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )

        # User 2 should see no tasks
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 200
        assert len(response.json()) == 0

    @pytest.mark.asyncio
    async def test_user_cannot_update_other_user_task(self, client: AsyncClient):
        """Test that users cannot update other users' tasks."""
        # User 1 creates task
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to update
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hacked"},
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_user_cannot_delete_other_user_task(self, client: AsyncClient):
        """Test that users cannot delete other users' tasks."""
        # User 1 creates task
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to delete
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 404

        # Verify task still exists for user 1
        get_response = await client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert get_response.status_code == 200

    @pytest.mark.asyncio
    async def test_user_cannot_toggle_other_user_task(self, client: AsyncClient):
        """Test that users cannot toggle other users' task completion."""
        # User 1 creates task
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = create_response.json()["id"]

        # User 2 tries to toggle
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.patch(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_user_cannot_see_other_user_tags(self, client: AsyncClient):
        """Test that users cannot see other users' tags."""
        # User 1 creates tags
        token1 = await get_auth_token(client, "user1@example.com")
        await client.post(
            "/api/tags",
            json={"name": "user1tag"},
            headers={"Authorization": f"Bearer {token1}"}
        )

        # User 2 should see no tags
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.get(
            "/api/tags",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 200
        assert len(response.json()) == 0

    @pytest.mark.asyncio
    async def test_user_cannot_delete_other_user_tag(self, client: AsyncClient):
        """Test that users cannot delete other users' tags."""
        # User 1 creates tag
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tags",
            json={"name": "user1tag"},
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


class TestUnauthorizedAccess:
    """Test suite for unauthorized access attempts."""

    @pytest.mark.asyncio
    async def test_unauthorized_get_tasks(self, client: AsyncClient):
        """Test that unauthenticated requests return 401."""
        response = await client.get("/api/tasks")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_unauthorized_create_task(self, client: AsyncClient):
        """Test that unauthenticated task creation returns 401."""
        response = await client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_unauthorized_update_task(self, client: AsyncClient):
        """Test that unauthenticated task update returns 401."""
        response = await client.put("/api/tasks/1", json={"title": "Test"})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_unauthorized_delete_task(self, client: AsyncClient):
        """Test that unauthenticated task deletion returns 401."""
        response = await client.delete("/api/tasks/1")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_unauthorized_get_tags(self, client: AsyncClient):
        """Test that unauthenticated tag request returns 401."""
        response = await client.get("/api/tags")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_invalid_token_rejected(self, client: AsyncClient):
        """Test that invalid tokens are rejected."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_malformed_auth_header_rejected(self, client: AsyncClient):
        """Test that malformed auth headers are rejected."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "NotBearer token"}
        )
        assert response.status_code == 401
