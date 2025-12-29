"""Tests for CompleteTaskCommand."""

from unittest.mock import patch

from src.commands.complete import CompleteTaskCommand
from src.models import TaskCreate
from src.storage import TaskStorage


class TestCompleteTaskCommandSuccess:
    """Tests for successful task completion."""

    def test_complete_pending_task(self, storage: TaskStorage) -> None:
        """Test marking a pending task as complete."""
        storage.add(TaskCreate(title="Test task"))
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_success") as mock_success:
                mock_console.input.return_value = "1"
                result = command.execute()

        assert result is not None
        assert result.completed is True
        mock_success.assert_called_once()

    def test_complete_updates_storage(self, storage: TaskStorage) -> None:
        """Test that completing task updates storage."""
        storage.add(TaskCreate(title="Test task"))
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_success"):
                mock_console.input.return_value = "1"
                command.execute()

        # Verify storage was updated
        task = storage.get(1)
        assert task.completed is True


class TestCompleteTaskCommandAlreadyComplete:
    """Tests for already completed tasks."""

    def test_already_completed_shows_info(self, storage: TaskStorage) -> None:
        """Test that already completed task shows info message."""
        storage.add(TaskCreate(title="Test task"))
        storage.mark_complete(1)
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_info") as mock_info:
                mock_console.input.return_value = "1"
                result = command.execute()

        assert result is not None
        assert result.completed is True
        mock_info.assert_called_once()
        assert "already completed" in str(mock_info.call_args)


class TestCompleteTaskCommandNotFound:
    """Tests for task not found scenarios."""

    def test_nonexistent_task_shows_error(self, storage: TaskStorage) -> None:
        """Test that nonexistent task ID shows error."""
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_error") as mock_error:
                mock_console.input.return_value = "999"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Task not found with ID: 999")

    def test_invalid_id_non_numeric_shows_error(self, storage: TaskStorage) -> None:
        """Test that non-numeric ID shows error."""
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_error") as mock_error:
                mock_console.input.return_value = "abc"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_zero_shows_error(self, storage: TaskStorage) -> None:
        """Test that zero ID shows error."""
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_error") as mock_error:
                mock_console.input.return_value = "0"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_negative_shows_error(self, storage: TaskStorage) -> None:
        """Test that negative ID shows error."""
        command = CompleteTaskCommand(storage)

        with patch("src.commands.complete.console") as mock_console:
            with patch("src.commands.complete.display_error") as mock_error:
                mock_console.input.return_value = "-1"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")
