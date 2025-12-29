"""Pydantic models for Todo CLI Application."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    """Represents a single todo task.

    Attributes:
        id: Unique identifier (auto-incremented)
        title: Short description (1-200 characters, required)
        description: Detailed description (max 1000 characters, optional)
        completed: Whether the task is done (default: False)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """

    id: int = Field(..., ge=1, description="Unique task identifier")
    title: str = Field(
        ..., min_length=1, max_length=200, description="Task title (required)"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Optional detailed description"
    )
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last modification timestamp"
    )


class TaskCreate(BaseModel):
    """Input model for creating a new task."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Task title (required)"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Optional detailed description"
    )


class TaskUpdate(BaseModel):
    """Input model for updating a task. All fields optional."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="New task title"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="New task description"
    )
