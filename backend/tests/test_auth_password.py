"""Tests for password hashing and verification."""

import pytest

from src.auth.password import hash_password, verify_password


class TestPasswordHashing:
    """Test suite for password hashing functions."""

    def test_hash_password_returns_hashed_string(self):
        """Test that hash_password returns a hashed string."""
        password = "SecurePassword123!"
        hashed = hash_password(password)

        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed != password  # Should not be plain text

    def test_hash_password_produces_different_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "SecurePassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # bcrypt uses random salt, so hashes should differ
        assert hash1 != hash2

    def test_verify_password_with_correct_password(self):
        """Test that verify_password returns True for correct password."""
        password = "SecurePassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_with_incorrect_password(self):
        """Test that verify_password returns False for incorrect password."""
        password = "SecurePassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_with_empty_password(self):
        """Test verify_password with empty password."""
        password = "SecurePassword123!"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False

    def test_hash_password_handles_special_characters(self):
        """Test that hash_password handles special characters."""
        password = "P@$$w0rd!#$%^&*()"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_password_handles_unicode(self):
        """Test that hash_password handles unicode characters."""
        password = "Pässwörd123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_password_handles_long_password(self):
        """Test that hash_password handles long passwords."""
        password = "A" * 100 + "123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True
