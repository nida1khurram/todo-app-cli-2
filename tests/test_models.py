"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from src.models import Task, TaskCreate, TaskUpdate


class TestTask:
    """Tests for Task model."""

    def test_task_creation_with_all_fields(self) -> None:
        """Test creating a task with all fields."""
        task = Task(id=1, title="Test task", description="Test description")
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.completed is False
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_creation_minimal(self) -> None:
        """Test creating a task with minimal required fields."""
        task = Task(id=1, title="Test task")
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description is None
        assert task.completed is False

    def test_task_title_min_length(self) -> None:
        """Test that title must be at least 1 character."""
        with pytest.raises(ValidationError):
            Task(id=1, title="")

    def test_task_title_max_length(self) -> None:
        """Test that title cannot exceed 200 characters."""
        with pytest.raises(ValidationError):
            Task(id=1, title="x" * 201)

    def test_task_description_max_length(self) -> None:
        """Test that description cannot exceed 1000 characters."""
        with pytest.raises(ValidationError):
            Task(id=1, title="Test", description="x" * 1001)

    def test_task_id_must_be_positive(self) -> None:
        """Test that task ID must be >= 1."""
        with pytest.raises(ValidationError):
            Task(id=0, title="Test")
        with pytest.raises(ValidationError):
            Task(id=-1, title="Test")


class TestTaskCreate:
    """Tests for TaskCreate model."""

    def test_task_create_with_description(self) -> None:
        """Test creating TaskCreate with description."""
        tc = TaskCreate(title="Test task", description="Test description")
        assert tc.title == "Test task"
        assert tc.description == "Test description"

    def test_task_create_without_description(self) -> None:
        """Test creating TaskCreate without description."""
        tc = TaskCreate(title="Test task")
        assert tc.title == "Test task"
        assert tc.description is None

    def test_task_create_empty_title(self) -> None:
        """Test that empty title raises ValidationError."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_task_create_title_too_long(self) -> None:
        """Test that title exceeding 200 chars raises ValidationError."""
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 201)

    def test_task_create_description_too_long(self) -> None:
        """Test that description exceeding 1000 chars raises ValidationError."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", description="x" * 1001)


class TestTaskUpdate:
    """Tests for TaskUpdate model."""

    def test_task_update_with_title(self) -> None:
        """Test TaskUpdate with only title."""
        tu = TaskUpdate(title="New title")
        assert tu.title == "New title"
        assert tu.description is None

    def test_task_update_with_description(self) -> None:
        """Test TaskUpdate with only description."""
        tu = TaskUpdate(description="New description")
        assert tu.title is None
        assert tu.description == "New description"

    def test_task_update_with_both(self) -> None:
        """Test TaskUpdate with both fields."""
        tu = TaskUpdate(title="New title", description="New description")
        assert tu.title == "New title"
        assert tu.description == "New description"

    def test_task_update_empty(self) -> None:
        """Test TaskUpdate with no fields (all None)."""
        tu = TaskUpdate()
        assert tu.title is None
        assert tu.description is None

    def test_task_update_title_too_long(self) -> None:
        """Test that title exceeding 200 chars raises ValidationError."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="x" * 201)
