"""AddTaskCommand implementation."""

from pydantic import ValidationError

from src.commands.base import Command
from src.models import Task, TaskCreate
from src.storage import TaskStorage
from src.ui import console, display_error, display_success


class AddTaskCommand(Command):
    """Command to add a new task.

    Prompts user for title and optional description,
    validates input, and adds task to storage.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize with storage instance.

        Args:
            storage: TaskStorage instance for persistence
        """
        self.storage = storage

    def execute(self) -> Task | None:
        """Execute the add task command.

        Prompts for title and description, validates input,
        and adds task to storage.

        Returns:
            Created Task if successful, None if validation fails
        """
        # Get title from user
        title = console.input("[bold]Enter task title:[/bold] ").strip()

        # Validate title is not empty
        if not title:
            display_error("Title is required (1-200 characters)")
            return None

        # Validate title length
        if len(title) > 200:
            display_error("Title must be 200 characters or less")
            return None

        # Get optional description
        description = console.input(
            "[bold]Enter description (optional, press Enter to skip):[/bold] "
        ).strip()

        # Convert empty description to None
        if not description:
            description = None

        # Validate description length if provided
        if description and len(description) > 1000:
            display_error("Description must be 1000 characters or less")
            return None

        try:
            # Create and add task
            task_create = TaskCreate(title=title, description=description)
            task = self.storage.add(task_create)
            display_success(f'Task added successfully: "{task.title}" (ID: {task.id})')
            return task
        except ValidationError as e:
            # Handle any validation errors from Pydantic
            display_error(str(e))
            return None
