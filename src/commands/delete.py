"""DeleteTaskCommand implementation."""

from src.commands.base import Command
from src.storage import TaskStorage
from src.ui import console, display_error, display_success


class DeleteTaskCommand(Command):
    """Command to delete a task by ID.

    Prompts user for task ID and removes the task from storage.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize with storage instance.

        Args:
            storage: TaskStorage instance for persistence
        """
        self.storage = storage

    def execute(self) -> bool:
        """Execute the delete task command.

        Prompts for task ID and deletes the task.

        Returns:
            True if deletion successful, False otherwise
        """
        # Get task ID from user
        id_input = console.input("[bold]Enter task ID to delete:[/bold] ").strip()

        # Validate input is a number
        try:
            task_id = int(id_input)
        except ValueError:
            display_error("Invalid task ID. Please enter a number.")
            return False

        # Validate ID is positive
        if task_id <= 0:
            display_error("Invalid task ID. Please enter a number.")
            return False

        # Check if task exists
        task = self.storage.get(task_id)
        if task is None:
            display_error(f"Task not found with ID: {task_id}")
            return False

        # Store title for success message
        task_title = task.title

        # Delete the task
        deleted_task = self.storage.delete(task_id)
        if deleted_task:
            display_success(f'Task deleted: "{task_title}" (ID: {task_id})')
            return True
        return False
