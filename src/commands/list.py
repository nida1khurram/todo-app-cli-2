"""ListTasksCommand implementation."""

from src.commands.base import Command
from src.models import Task
from src.storage import TaskStorage
from src.ui import display_task_table


class ListTasksCommand(Command):
    """Command to list all tasks.

    Displays all tasks in a formatted table with
    ID, status, title, and creation date.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize with storage instance.

        Args:
            storage: TaskStorage instance for persistence
        """
        self.storage = storage

    def execute(self) -> list[Task]:
        """Execute the list tasks command.

        Retrieves all tasks and displays them in a formatted table.

        Returns:
            List of all tasks
        """
        tasks = self.storage.get_all()
        display_task_table(tasks)
        return tasks
