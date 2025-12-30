"""Tests for TaskTag junction model."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.user import User
from src.models.task import Task
from src.models.tag import Tag
from src.models.task_tag import TaskTag


class TestTaskTagModel:
    """Test suite for TaskTag junction model."""

    @pytest.mark.asyncio
    async def test_create_task_tag_association(self, db_session: AsyncSession):
        """Test creating a task-tag association."""
        # Create user
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Create task
        task = Task(user_id=user.id, title="Test Task")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        # Create tag
        tag = Tag(user_id=user.id, name="work")
        db_session.add(tag)
        await db_session.commit()
        await db_session.refresh(tag)

        # Create association
        task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
        db_session.add(task_tag)
        await db_session.commit()

        # Verify association exists
        result = await db_session.execute(
            select(TaskTag).where(
                TaskTag.task_id == task.id,
                TaskTag.tag_id == tag.id
            )
        )
        found = result.scalar_one_or_none()
        assert found is not None

    @pytest.mark.asyncio
    async def test_task_tag_has_created_at(self, db_session: AsyncSession):
        """Test that TaskTag has created_at timestamp."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        tag = Tag(user_id=user.id, name="work")
        db_session.add(task)
        db_session.add(tag)
        await db_session.commit()
        await db_session.refresh(task)
        await db_session.refresh(tag)

        task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
        db_session.add(task_tag)
        await db_session.commit()

        result = await db_session.execute(
            select(TaskTag).where(TaskTag.task_id == task.id)
        )
        found = result.scalar_one()
        assert found.created_at is not None

    @pytest.mark.asyncio
    async def test_multiple_tags_per_task(self, db_session: AsyncSession):
        """Test that a task can have multiple tags."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        db_session.add(task)

        tags = [
            Tag(user_id=user.id, name="work"),
            Tag(user_id=user.id, name="urgent"),
            Tag(user_id=user.id, name="project"),
        ]
        for tag in tags:
            db_session.add(tag)
        await db_session.commit()
        await db_session.refresh(task)

        for tag in tags:
            await db_session.refresh(tag)
            task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
            db_session.add(task_tag)
        await db_session.commit()

        result = await db_session.execute(
            select(TaskTag).where(TaskTag.task_id == task.id)
        )
        associations = result.scalars().all()
        assert len(associations) == 3

    @pytest.mark.asyncio
    async def test_multiple_tasks_per_tag(self, db_session: AsyncSession):
        """Test that a tag can be associated with multiple tasks."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        tag = Tag(user_id=user.id, name="work")
        db_session.add(tag)

        tasks = [
            Task(user_id=user.id, title="Task 1"),
            Task(user_id=user.id, title="Task 2"),
            Task(user_id=user.id, title="Task 3"),
        ]
        for task in tasks:
            db_session.add(task)
        await db_session.commit()
        await db_session.refresh(tag)

        for task in tasks:
            await db_session.refresh(task)
            task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
            db_session.add(task_tag)
        await db_session.commit()

        result = await db_session.execute(
            select(TaskTag).where(TaskTag.tag_id == tag.id)
        )
        associations = result.scalars().all()
        assert len(associations) == 3

    @pytest.mark.asyncio
    async def test_composite_primary_key(self, db_session: AsyncSession):
        """Test that task_id and tag_id form composite primary key."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        task = Task(user_id=user.id, title="Test Task")
        tag = Tag(user_id=user.id, name="work")
        db_session.add(task)
        db_session.add(tag)
        await db_session.commit()
        await db_session.refresh(task)
        await db_session.refresh(tag)

        # First association should succeed
        task_tag1 = TaskTag(task_id=task.id, tag_id=tag.id)
        db_session.add(task_tag1)
        await db_session.commit()

        # Duplicate should fail
        task_tag2 = TaskTag(task_id=task.id, tag_id=tag.id)
        db_session.add(task_tag2)

        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()
