"""Pytest fixtures for Todo CLI Application tests."""

import pytest

from src.models import Task, TaskCreate
from src.storage import TaskStorage


@pytest.fixture
def storage() -> TaskStorage:
    """Provide a fresh TaskStorage instance for each test."""
    return TaskStorage()


@pytest.fixture
def sample_task_create() -> TaskCreate:
    """Provide a sample TaskCreate instance."""
    return TaskCreate(title="Buy groceries", description="Milk, eggs, bread")


@pytest.fixture
def storage_with_tasks(storage: TaskStorage) -> TaskStorage:
    """Provide a TaskStorage with pre-populated tasks."""
    storage.add(TaskCreate(title="Task 1", description="First task"))
    storage.add(TaskCreate(title="Task 2", description="Second task"))
    storage.add(TaskCreate(title="Task 3"))  # No description
    return storage


@pytest.fixture
def sample_task(storage: TaskStorage, sample_task_create: TaskCreate) -> Task:
    """Provide a sample Task that has been added to storage."""
    return storage.add(sample_task_create)
