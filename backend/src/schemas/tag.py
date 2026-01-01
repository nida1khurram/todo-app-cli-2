"""Tag schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    """Base tag schema."""

    name: str = Field(min_length=1, max_length=50)


class TagCreate(TagBase):
    """Schema for creating a tag."""

    pass


class TagUpdate(BaseModel):
    """Schema for updating a tag."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=50)


class TagResponse(TagBase):
    """Complete tag schema for responses."""

    id: int
    user_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
