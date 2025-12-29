"""Tests for ListTasksCommand."""

from unittest.mock import patch

from src.commands.list import ListTasksCommand
from src.models import TaskCreate
from src.storage import TaskStorage


class TestListTasksCommandWithTasks:
    """Tests for listing tasks when tasks exist."""

    def test_list_returns_all_tasks(self, storage_with_tasks: TaskStorage) -> None:
        """Test that list returns all tasks."""
        command = ListTasksCommand(storage_with_tasks)
        with patch("src.commands.list.display_task_table"):
            result = command.execute()

        assert len(result) == 3

    def test_list_calls_display_function(self, storage_with_tasks: TaskStorage) -> None:
        """Test that list calls display_task_table."""
        command = ListTasksCommand(storage_with_tasks)
        with patch("src.commands.list.display_task_table") as mock_display:
            command.execute()

        mock_display.assert_called_once()

    def test_list_shows_correct_task_data(self, storage: TaskStorage) -> None:
        """Test that list shows tasks with correct data."""
        storage.add(TaskCreate(title="Task 1", description="First task"))
        command = ListTasksCommand(storage)
        with patch("src.commands.list.display_task_table"):
            result = command.execute()

        assert result[0].title == "Task 1"
        assert result[0].description == "First task"

    def test_list_shows_mixed_completion_status(self, storage: TaskStorage) -> None:
        """Test that list shows tasks with different completion statuses."""
        storage.add(TaskCreate(title="Task 1"))
        storage.add(TaskCreate(title="Task 2"))
        storage.mark_complete(1)

        command = ListTasksCommand(storage)
        with patch("src.commands.list.display_task_table"):
            result = command.execute()

        completed = [t for t in result if t.completed]
        pending = [t for t in result if not t.completed]
        assert len(completed) == 1
        assert len(pending) == 1


class TestListTasksCommandEmpty:
    """Tests for listing tasks when no tasks exist."""

    def test_list_empty_returns_empty_list(self, storage: TaskStorage) -> None:
        """Test that list returns empty list when no tasks."""
        command = ListTasksCommand(storage)
        with patch("src.commands.list.display_task_table"):
            result = command.execute()

        assert result == []

    def test_list_empty_calls_display_function(self, storage: TaskStorage) -> None:
        """Test that display is called even when empty."""
        command = ListTasksCommand(storage)
        with patch("src.commands.list.display_task_table") as mock_display:
            command.execute()

        mock_display.assert_called_once_with([])
