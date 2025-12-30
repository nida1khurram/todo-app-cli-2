"""Tests for Task model validation."""

import pytest
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.task import Task


class TestTaskModel:
    """Test suite for Task model."""

    @pytest.mark.asyncio
    async def test_create_task_with_valid_data(self, db_session: AsyncSession):
        """Test creating a task with valid data."""
        # Create user first
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Create task
        task = Task(
            user_id=user.id,
            title="Test Task",
            description="Test description",
            priority="medium",
        )
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.id is not None
        assert task.user_id == user.id
        assert task.title == "Test Task"
        assert task.is_completed is False
        assert task.priority == "medium"

    @pytest.mark.asyncio
    async def test_task_has_timestamps(self, db_session: AsyncSession):
        """Test that task has created_at and updated_at timestamps."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.created_at is not None
        assert task.updated_at is not None

    @pytest.mark.asyncio
    async def test_task_default_priority_is_medium(self, db_session: AsyncSession):
        """Test that task default priority is medium."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.priority == "medium"

    @pytest.mark.asyncio
    async def test_task_default_is_completed_is_false(self, db_session: AsyncSession):
        """Test that task default is_completed is False."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.is_completed is False

    @pytest.mark.asyncio
    async def test_task_title_max_length(self, db_session: AsyncSession):
        """Test task title accepts up to max length."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        long_title = "A" * 200
        task = Task(user_id=user.id, title=long_title)
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.title == long_title

    @pytest.mark.asyncio
    async def test_task_description_optional(self, db_session: AsyncSession):
        """Test that task description is optional."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.description is None
