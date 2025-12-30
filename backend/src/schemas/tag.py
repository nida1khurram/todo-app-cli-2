"""Tag schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TagCreate(BaseModel):
    """Schema for creating a new tag."""

    name: str = Field(min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """Validate and clean tag name."""
        v = v.strip().lower()
        if not v:
            raise ValueError("Tag name cannot be empty or whitespace")
        return v


class TagResponse(BaseModel):
    """Schema for tag response."""

    id: int
    user_id: int
    name: str
    created_at: datetime

    model_config = {"from_attributes": True}
