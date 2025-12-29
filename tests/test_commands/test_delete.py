"""Tests for DeleteTaskCommand."""

from unittest.mock import patch

from src.commands.delete import DeleteTaskCommand
from src.models import TaskCreate
from src.storage import TaskStorage


class TestDeleteTaskCommandSuccess:
    """Tests for successful task deletion."""

    def test_delete_existing_task(self, storage: TaskStorage) -> None:
        """Test deleting an existing task."""
        storage.add(TaskCreate(title="Test task"))
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_success") as mock_success:
                mock_console.input.return_value = "1"
                result = command.execute()

        assert result is True
        mock_success.assert_called_once()

    def test_delete_removes_from_storage(self, storage: TaskStorage) -> None:
        """Test that deletion removes task from storage."""
        storage.add(TaskCreate(title="Test task"))
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_success"):
                mock_console.input.return_value = "1"
                command.execute()

        # Verify task was removed
        task = storage.get(1)
        assert task is None

    def test_delete_specific_task_from_multiple(self, storage: TaskStorage) -> None:
        """Test deleting a specific task when multiple exist."""
        storage.add(TaskCreate(title="Task 1"))
        storage.add(TaskCreate(title="Task 2"))
        storage.add(TaskCreate(title="Task 3"))
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_success"):
                mock_console.input.return_value = "2"
                result = command.execute()

        assert result is True
        assert storage.get(1) is not None
        assert storage.get(2) is None
        assert storage.get(3) is not None

    def test_delete_shows_task_title_in_message(self, storage: TaskStorage) -> None:
        """Test that success message includes task title."""
        storage.add(TaskCreate(title="Important Task"))
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_success") as mock_success:
                mock_console.input.return_value = "1"
                command.execute()

        call_args = str(mock_success.call_args)
        assert "Important Task" in call_args


class TestDeleteTaskCommandNotFound:
    """Tests for task not found scenarios."""

    def test_nonexistent_task_shows_error(self, storage: TaskStorage) -> None:
        """Test that nonexistent task ID shows error."""
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_error") as mock_error:
                mock_console.input.return_value = "999"
                result = command.execute()

        assert result is False
        mock_error.assert_called_once_with("Task not found with ID: 999")

    def test_invalid_id_non_numeric_shows_error(self, storage: TaskStorage) -> None:
        """Test that non-numeric ID shows error."""
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_error") as mock_error:
                mock_console.input.return_value = "abc"
                result = command.execute()

        assert result is False
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_zero_shows_error(self, storage: TaskStorage) -> None:
        """Test that zero ID shows error."""
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_error") as mock_error:
                mock_console.input.return_value = "0"
                result = command.execute()

        assert result is False
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_negative_shows_error(self, storage: TaskStorage) -> None:
        """Test that negative ID shows error."""
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_error") as mock_error:
                mock_console.input.return_value = "-1"
                result = command.execute()

        assert result is False
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_empty_shows_error(self, storage: TaskStorage) -> None:
        """Test that empty ID shows error."""
        command = DeleteTaskCommand(storage)

        with patch("src.commands.delete.console") as mock_console:
            with patch("src.commands.delete.display_error") as mock_error:
                mock_console.input.return_value = ""
                result = command.execute()

        assert result is False
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")
