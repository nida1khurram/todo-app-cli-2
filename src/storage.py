"""In-memory storage for Todo CLI Application."""

from datetime import datetime
from typing import Optional

from src.models import Task, TaskCreate, TaskUpdate


class TaskStorage:
    """In-memory storage for tasks using dictionary.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for auto-incrementing IDs
    """

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_create: TaskCreate) -> Task:
        """Add a new task and return it with assigned ID.

        Args:
            task_create: Task creation data

        Returns:
            Created Task with ID and timestamps
        """
        now = datetime.now()
        task = Task(
            id=self._next_id,
            title=task_create.title,
            description=task_create.description,
            completed=False,
            created_at=now,
            updated_at=now,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The task ID to look up

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Get all tasks ordered by ID.

        Returns:
            List of all tasks sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task's title and/or description.

        Args:
            task_id: The task ID to update
            task_update: Fields to update

        Returns:
            Updated Task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        # Check if any changes are being made
        has_changes = False
        new_title = task.title
        new_description = task.description

        if task_update.title is not None:
            new_title = task_update.title
            has_changes = True

        if task_update.description is not None:
            new_description = task_update.description
            has_changes = True

        if not has_changes:
            return task

        # Create updated task
        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=datetime.now(),
        )
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> Optional[Task]:
        """Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            Deleted Task if found, None otherwise
        """
        return self._tasks.pop(task_id, None)

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed.

        Args:
            task_id: The task ID to mark complete

        Returns:
            Updated Task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        # Create updated task with completed=True
        completed_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=True,
            created_at=task.created_at,
            updated_at=datetime.now(),
        )
        self._tasks[task_id] = completed_task
        return completed_task
