"""Task schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Base task schema."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = False
    priority: str = "medium"


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    tags: list[str] = Field(default=[], description="List of tag names")


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[list[str]] = Field(default=None, description="List of tag names")


class TaskResponse(TaskBase):
    """Complete task schema for responses."""

    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    tags: list[str] = Field(default=[], description="List of tag names")

    model_config = ConfigDict(from_attributes=True)
