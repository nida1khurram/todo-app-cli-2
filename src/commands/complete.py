"""CompleteTaskCommand implementation."""

from src.commands.base import Command
from src.models import Task
from src.storage import TaskStorage
from src.ui import console, display_error, display_info, display_success


class CompleteTaskCommand(Command):
    """Command to mark a task as complete.

    Prompts user for task ID and marks the task as completed.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize with storage instance.

        Args:
            storage: TaskStorage instance for persistence
        """
        self.storage = storage

    def execute(self) -> Task | None:
        """Execute the complete task command.

        Prompts for task ID and marks the task as complete.

        Returns:
            Updated Task if successful, None otherwise
        """
        # Get task ID from user
        id_input = console.input(
            "[bold]Enter task ID to mark complete:[/bold] "
        ).strip()

        # Validate input is a number
        try:
            task_id = int(id_input)
        except ValueError:
            display_error("Invalid task ID. Please enter a number.")
            return None

        # Validate ID is positive
        if task_id <= 0:
            display_error("Invalid task ID. Please enter a number.")
            return None

        # Check if task exists
        task = self.storage.get(task_id)
        if task is None:
            display_error(f"Task not found with ID: {task_id}")
            return None

        # Check if already completed
        if task.completed:
            display_info(f'Task is already completed: "{task.title}" (ID: {task.id})')
            return task

        # Mark as complete
        completed_task = self.storage.mark_complete(task_id)
        if completed_task:
            msg = f'Task marked as complete: "{completed_task.title}" '
            msg += f"(ID: {completed_task.id})"
            display_success(msg)
        return completed_task
