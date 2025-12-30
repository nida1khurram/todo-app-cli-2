"""Tests for tasks API routes."""

import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient, email: str = "test@example.com", password: str = "SecurePass123!") -> str:
    """Helper to register and login a user, returning the auth token."""
    await client.post("/api/auth/register", json={"email": email, "password": password})
    response = await client.post("/api/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


class TestGetTasksEndpoint:
    """Test suite for GET /api/tasks endpoint."""

    @pytest.mark.asyncio
    async def test_get_tasks_empty_list(self, client: AsyncClient):
        """Test getting tasks when none exist."""
        token = await get_auth_token(client)

        response = await client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_tasks_returns_user_tasks(self, client: AsyncClient, sample_task_data: dict):
        """Test getting tasks returns only user's tasks."""
        token = await get_auth_token(client)

        # Create a task
        await client.post(
            "/api/tasks",
            json=sample_task_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        response = await client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == sample_task_data["title"]

    @pytest.mark.asyncio
    async def test_get_tasks_user_isolation(self, client: AsyncClient, sample_task_data: dict):
        """Test that users can only see their own tasks."""
        # User 1 creates a task
        token1 = await get_auth_token(client, "user1@example.com")
        await client.post(
            "/api/tasks",
            json=sample_task_data,
            headers={"Authorization": f"Bearer {token1}"}
        )

        # User 2 should see no tasks
        token2 = await get_auth_token(client, "user2@example.com")
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_get_tasks_unauthorized(self, client: AsyncClient):
        """Test getting tasks without authentication."""
        response = await client.get("/api/tasks")

        assert response.status_code == 401


class TestCreateTaskEndpoint:
    """Test suite for POST /api/tasks endpoint."""

    @pytest.mark.asyncio
    async def test_create_task_success(self, client: AsyncClient, sample_task_data: dict):
        """Test successful task creation."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tasks",
            json=sample_task_data,
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["priority"] == sample_task_data["priority"]
        assert data["is_completed"] is False
        assert "id" in data

    @pytest.mark.asyncio
    async def test_create_task_minimal_data(self, client: AsyncClient):
        """Test creating task with only required fields."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tasks",
            json={"title": "Minimal Task"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["priority"] == "medium"  # Default

    @pytest.mark.asyncio
    async def test_create_task_missing_title(self, client: AsyncClient):
        """Test creating task without title."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tasks",
            json={"description": "No title"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_empty_title(self, client: AsyncClient):
        """Test creating task with empty title."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tasks",
            json={"title": "   "},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_unauthorized(self, client: AsyncClient, sample_task_data: dict):
        """Test creating task without authentication."""
        response = await client.post("/api/tasks", json=sample_task_data)

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_task_with_tags(self, client: AsyncClient):
        """Test creating task with tags."""
        token = await get_auth_token(client)

        response = await client.post(
            "/api/tasks",
            json={"title": "Tagged Task", "tags": ["work", "urgent"]},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 201
        data = response.json()
        assert "work" in data["tags"]
        assert "urgent" in data["tags"]


class TestUpdateTaskEndpoint:
    """Test suite for PUT /api/tasks/{task_id} endpoint."""

    @pytest.mark.asyncio
    async def test_update_task_success(self, client: AsyncClient, sample_task_data: dict):
        """Test successful task update."""
        token = await get_auth_token(client)

        # Create task
        create_response = await client.post(
            "/api/tasks",
            json=sample_task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]

        # Update task
        response = await client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title", "priority": "high"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["priority"] == "high"

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, client: AsyncClient):
        """Test updating non-existent task."""
        token = await get_auth_token(client)

        response = await client.put(
            "/api/tasks/99999",
            json={"title": "Updated"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task_unauthorized(self, client: AsyncClient, sample_task_data: dict):
        """Test updating task without authentication."""
        response = await client.put("/api/tasks/1", json={"title": "Updated"})

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_task_other_user(self, client: AsyncClient, sample_task_data: dict):
        """Test updating another user's task."""
        # User 1 creates task
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tasks",
            json=sample_task_data,
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


class TestDeleteTaskEndpoint:
    """Test suite for DELETE /api/tasks/{task_id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, client: AsyncClient, sample_task_data: dict):
        """Test successful task deletion."""
        token = await get_auth_token(client)

        # Create task
        create_response = await client.post(
            "/api/tasks",
            json=sample_task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 204

        # Verify deleted
        get_response = await client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, client: AsyncClient):
        """Test deleting non-existent task."""
        token = await get_auth_token(client)

        response = await client.delete(
            "/api/tasks/99999",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_other_user(self, client: AsyncClient, sample_task_data: dict):
        """Test deleting another user's task."""
        # User 1 creates task
        token1 = await get_auth_token(client, "user1@example.com")
        create_response = await client.post(
            "/api/tasks",
            json=sample_task_data,
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


class TestToggleTaskComplete:
    """Test suite for PATCH /api/tasks/{task_id} endpoint."""

    @pytest.mark.asyncio
    async def test_toggle_complete_success(self, client: AsyncClient, sample_task_data: dict):
        """Test toggling task completion."""
        token = await get_auth_token(client)

        # Create task
        create_response = await client.post(
            "/api/tasks",
            json=sample_task_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]
        assert create_response.json()["is_completed"] is False

        # Toggle to complete
        response = await client.patch(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["is_completed"] is True

        # Toggle back to incomplete
        response = await client.patch(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["is_completed"] is False

    @pytest.mark.asyncio
    async def test_toggle_complete_unauthorized(self, client: AsyncClient):
        """Test toggling without authentication."""
        response = await client.patch("/api/tasks/1")

        assert response.status_code == 401


class TestTaskFilters:
    """Test suite for task filtering."""

    @pytest.mark.asyncio
    async def test_filter_by_status_completed(self, client: AsyncClient):
        """Test filtering by completed status."""
        token = await get_auth_token(client)

        # Create and complete a task
        create_response = await client.post(
            "/api/tasks",
            json={"title": "Completed Task"},
            headers={"Authorization": f"Bearer {token}"}
        )
        task_id = create_response.json()["id"]
        await client.patch(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Create incomplete task
        await client.post(
            "/api/tasks",
            json={"title": "Pending Task"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Filter completed
        response = await client.get(
            "/api/tasks?status_filter=completed",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Completed Task"

    @pytest.mark.asyncio
    async def test_filter_by_priority(self, client: AsyncClient):
        """Test filtering by priority."""
        token = await get_auth_token(client)

        # Create tasks with different priorities
        await client.post(
            "/api/tasks",
            json={"title": "High Priority", "priority": "high"},
            headers={"Authorization": f"Bearer {token}"}
        )
        await client.post(
            "/api/tasks",
            json={"title": "Low Priority", "priority": "low"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Filter by high priority
        response = await client.get(
            "/api/tasks?priority=high",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["priority"] == "high"

    @pytest.mark.asyncio
    async def test_search_tasks(self, client: AsyncClient):
        """Test searching tasks by keyword."""
        token = await get_auth_token(client)

        # Create tasks
        await client.post(
            "/api/tasks",
            json={"title": "Buy groceries"},
            headers={"Authorization": f"Bearer {token}"}
        )
        await client.post(
            "/api/tasks",
            json={"title": "Write code"},
            headers={"Authorization": f"Bearer {token}"}
        )

        # Search
        response = await client.get(
            "/api/tasks?search=groceries",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert "groceries" in tasks[0]["title"].lower()


class TestTaskSorting:
    """Test suite for task sorting."""

    @pytest.mark.asyncio
    async def test_sort_by_created_at_desc(self, client: AsyncClient):
        """Test sorting by created_at descending (default)."""
        token = await get_auth_token(client)

        # Create tasks
        await client.post(
            "/api/tasks",
            json={"title": "First Task"},
            headers={"Authorization": f"Bearer {token}"}
        )
        await client.post(
            "/api/tasks",
            json={"title": "Second Task"},
            headers={"Authorization": f"Bearer {token}"}
        )

        response = await client.get(
            "/api/tasks?sort_by=created_at&sort_order=desc",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2
        # Most recent first
        assert tasks[0]["title"] == "Second Task"

    @pytest.mark.asyncio
    async def test_sort_by_title_asc(self, client: AsyncClient):
        """Test sorting by title ascending."""
        token = await get_auth_token(client)

        # Create tasks
        await client.post(
            "/api/tasks",
            json={"title": "Zebra"},
            headers={"Authorization": f"Bearer {token}"}
        )
        await client.post(
            "/api/tasks",
            json={"title": "Apple"},
            headers={"Authorization": f"Bearer {token}"}
        )

        response = await client.get(
            "/api/tasks?sort_by=title&sort_order=asc",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        tasks = response.json()
        assert tasks[0]["title"] == "Apple"
        assert tasks[1]["title"] == "Zebra"
