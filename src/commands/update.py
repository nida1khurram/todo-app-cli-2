"""UpdateTaskCommand implementation."""

from src.commands.base import Command
from src.models import Task, TaskUpdate
from src.storage import TaskStorage
from src.ui import console, display_error, display_info, display_success


class UpdateTaskCommand(Command):
    """Command to update a task's title and/or description.

    Prompts user for task ID and new values for title and description.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize with storage instance.

        Args:
            storage: TaskStorage instance for persistence
        """
        self.storage = storage

    def execute(self) -> Task | None:
        """Execute the update task command.

        Prompts for task ID and new values, validates input,
        and updates the task.

        Returns:
            Updated Task if successful, None otherwise
        """
        # Get task ID from user
        id_input = console.input("[bold]Enter task ID to update:[/bold] ").strip()

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

        # Get new title (optional)
        console.print(f'[dim]Current title: "{task.title}"[/dim]')
        new_title = console.input(
            "[bold]Enter new title (press Enter to keep current):[/bold] "
        ).strip()

        # Validate title length if provided
        if new_title and len(new_title) > 200:
            display_error("Title must be 200 characters or less")
            return None

        # Get new description (optional)
        current_desc = task.description or "(none)"
        console.print(f'[dim]Current description: "{current_desc}"[/dim]')
        new_description = console.input(
            "[bold]Enter new description (press Enter to keep current):[/bold] "
        ).strip()

        # Validate description length if provided
        if new_description and len(new_description) > 1000:
            display_error("Description must be 1000 characters or less")
            return None

        # Check if any changes were made
        if not new_title and not new_description:
            display_info("No changes made")
            return task

        # Build update model
        update_data = TaskUpdate(
            title=new_title if new_title else None,
            description=new_description if new_description else None,
        )

        # Update the task
        updated_task = self.storage.update(task_id, update_data)
        if updated_task:
            msg = f'Task updated successfully: "{updated_task.title}" '
            msg += f"(ID: {updated_task.id})"
            display_success(msg)
        return updated_task
