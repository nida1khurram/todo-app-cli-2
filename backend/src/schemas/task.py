"""Task schemas for request/response validation."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    priority: Literal["high", "medium", "low"] = "medium"
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty or whitespace")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate and clean tag names."""
        return [tag.strip().lower() for tag in v if tag.strip()]


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: Literal["high", "medium", "low"] | None = None
    is_completed: bool | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str | None) -> str | None:
        """Validate title is not empty or whitespace."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty or whitespace")
        return v


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: int
    user_id: int
    title: str
    description: str | None
    is_completed: bool
    priority: str
    created_at: datetime
    updated_at: datetime
    tags: list[str] = Field(default_factory=list)

    model_config = {"from_attributes": False}
