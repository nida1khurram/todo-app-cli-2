"""Tests for JWT token creation and validation."""

import pytest
from datetime import timedelta

from src.auth.jwt import create_access_token, decode_token


class TestJWT:
    """Test suite for JWT functions."""

    def test_create_access_token_returns_string(self):
        """Test that create_access_token returns a JWT string."""
        token = create_access_token(data={"sub": "1"})

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_contains_subject(self):
        """Test that token contains the subject claim."""
        user_id = "123"
        token = create_access_token(data={"sub": user_id})
        payload = decode_token(token)

        assert payload is not None
        assert payload.get("sub") == user_id

    def test_decode_token_returns_payload(self):
        """Test that decode_token returns the payload."""
        data = {"sub": "456", "custom": "value"}
        token = create_access_token(data=data)
        payload = decode_token(token)

        assert payload is not None
        assert payload.get("sub") == "456"

    def test_decode_token_with_invalid_token(self):
        """Test that decode_token returns None for invalid token."""
        invalid_token = "invalid.jwt.token"
        payload = decode_token(invalid_token)

        assert payload is None

    def test_decode_token_with_empty_token(self):
        """Test that decode_token returns None for empty token."""
        payload = decode_token("")

        assert payload is None

    def test_create_access_token_with_custom_expiry(self):
        """Test creating token with custom expiry."""
        token = create_access_token(
            data={"sub": "789"},
            expires_delta=timedelta(hours=1)
        )
        payload = decode_token(token)

        assert payload is not None
        assert "exp" in payload

    def test_token_has_expiration_claim(self):
        """Test that generated token has expiration claim."""
        token = create_access_token(data={"sub": "test"})
        payload = decode_token(token)

        assert payload is not None
        assert "exp" in payload

    def test_decode_token_with_malformed_token(self):
        """Test decode_token with malformed JWT."""
        malformed_tokens = [
            "notavalidtoken",
            "only.two.parts.here.extra",
            "   ",
            None,
        ]

        for token in malformed_tokens:
            if token is not None:
                payload = decode_token(token)
                assert payload is None
