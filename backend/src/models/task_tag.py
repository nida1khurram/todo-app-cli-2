"""TaskTag junction table model."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class TaskTag(SQLModel, table=True):
    """Junction table for many-to-many relationship between tasks and tags."""

    __tablename__ = "task_tags"

    task_id: int = Field(
        foreign_key="tasks.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    tag_id: int = Field(
        foreign_key="tags.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
