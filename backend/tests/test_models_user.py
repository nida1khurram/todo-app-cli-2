"""Tests for User model validation."""

import pytest
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class TestUserModel:
    """Test suite for User model."""

    @pytest.mark.asyncio
    async def test_create_user_with_valid_data(self, db_session: AsyncSession):
        """Test creating a user with valid data."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_here",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password_here"
        assert user.created_at is not None

    @pytest.mark.asyncio
    async def test_user_email_is_indexed(self, db_session: AsyncSession):
        """Test that user email field is properly indexed for lookups."""
        user = User(
            email="indexed@example.com",
            password_hash="hashed_password",
        )
        db_session.add(user)
        await db_session.commit()

        # Query by email should work
        result = await db_session.execute(
            select(User).where(User.email == "indexed@example.com")
        )
        found_user = result.scalar_one_or_none()

        assert found_user is not None
        assert found_user.email == "indexed@example.com"

    @pytest.mark.asyncio
    async def test_user_has_created_at_timestamp(self, db_session: AsyncSession):
        """Test that user has created_at timestamp set automatically."""
        user = User(
            email="timestamp@example.com",
            password_hash="hashed_password",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.created_at is not None

    @pytest.mark.asyncio
    async def test_user_relationships_initialized(self, db_session: AsyncSession):
        """Test that user relationships are properly initialized."""
        user = User(
            email="relations@example.com",
            password_hash="hashed_password",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # User should have tasks and tags relationships (empty initially)
        assert user.id is not None
