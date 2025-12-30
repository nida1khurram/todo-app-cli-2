"""Tests for Tag model validation."""

import pytest
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.tag import Tag


class TestTagModel:
    """Test suite for Tag model."""

    @pytest.mark.asyncio
    async def test_create_tag_with_valid_data(self, db_session: AsyncSession):
        """Test creating a tag with valid data."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        tag = Tag(user_id=user.id, name="work")
        db_session.add(tag)
        await db_session.commit()
        await db_session.refresh(tag)

        assert tag.id is not None
        assert tag.user_id == user.id
        assert tag.name == "work"
        assert tag.created_at is not None

    @pytest.mark.asyncio
    async def test_tag_unique_per_user(self, db_session: AsyncSession):
        """Test that tag names are unique per user."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        tag1 = Tag(user_id=user.id, name="work")
        db_session.add(tag1)
        await db_session.commit()

        # Same tag name for same user should fail
        tag2 = Tag(user_id=user.id, name="work")
        db_session.add(tag2)

        with pytest.raises(Exception):  # IntegrityError
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_different_users_can_have_same_tag_name(self, db_session: AsyncSession):
        """Test that different users can have tags with same name."""
        user1 = User(email="user1@example.com", password_hash="hashed")
        user2 = User(email="user2@example.com", password_hash="hashed")
        db_session.add(user1)
        db_session.add(user2)
        await db_session.commit()
        await db_session.refresh(user1)
        await db_session.refresh(user2)

        tag1 = Tag(user_id=user1.id, name="work")
        tag2 = Tag(user_id=user2.id, name="work")
        db_session.add(tag1)
        db_session.add(tag2)
        await db_session.commit()

        # Both should exist
        result = await db_session.execute(select(Tag).where(Tag.name == "work"))
        tags = result.scalars().all()
        assert len(tags) == 2

    @pytest.mark.asyncio
    async def test_tag_name_max_length(self, db_session: AsyncSession):
        """Test tag name accepts up to max length."""
        user = User(email="test@example.com", password_hash="hashed")
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        tag = Tag(user_id=user.id, name="a" * 50)
        db_session.add(tag)
        await db_session.commit()
        await db_session.refresh(tag)

        assert len(tag.name) == 50
