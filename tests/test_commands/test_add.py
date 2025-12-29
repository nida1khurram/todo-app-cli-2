"""Tests for AddTaskCommand."""

from unittest.mock import patch

from src.commands.add import AddTaskCommand
from src.storage import TaskStorage


class TestAddTaskCommandSuccess:
    """Tests for successful task addition."""

    def test_add_task_with_title_only(self, storage: TaskStorage) -> None:
        """Test adding a task with only title."""
        command = AddTaskCommand(storage)
        with patch.object(command.storage, "add", wraps=storage.add):
            with patch("src.commands.add.console") as mock_console:
                mock_console.input.side_effect = ["Buy groceries", ""]
                result = command.execute()

        assert result is not None
        assert result.title == "Buy groceries"
        assert result.description is None
        assert result.id == 1

    def test_add_task_with_title_and_description(self, storage: TaskStorage) -> None:
        """Test adding a task with title and description."""
        command = AddTaskCommand(storage)
        with patch("src.commands.add.console") as mock_console:
            mock_console.input.side_effect = ["Buy groceries", "Milk, eggs, bread"]
            result = command.execute()

        assert result is not None
        assert result.title == "Buy groceries"
        assert result.description == "Milk, eggs, bread"

    def test_add_multiple_tasks(self, storage: TaskStorage) -> None:
        """Test adding multiple tasks increments ID."""
        command = AddTaskCommand(storage)
        with patch("src.commands.add.console") as mock_console:
            mock_console.input.side_effect = ["Task 1", "", "Task 2", ""]
            result1 = command.execute()
            result2 = command.execute()

        assert result1.id == 1
        assert result2.id == 2


class TestAddTaskCommandValidation:
    """Tests for validation error handling."""

    def test_empty_title_shows_error(self, storage: TaskStorage) -> None:
        """Test that empty title displays error."""
        command = AddTaskCommand(storage)
        with patch("src.commands.add.console") as mock_console:
            with patch("src.commands.add.display_error") as mock_error:
                mock_console.input.side_effect = ["", ""]
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Title is required (1-200 characters)")

    def test_title_too_long_shows_error(self, storage: TaskStorage) -> None:
        """Test that title exceeding 200 chars displays error."""
        command = AddTaskCommand(storage)
        long_title = "x" * 201
        with patch("src.commands.add.console") as mock_console:
            with patch("src.commands.add.display_error") as mock_error:
                mock_console.input.side_effect = [long_title, ""]
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Title must be 200 characters or less")

    def test_description_too_long_shows_error(self, storage: TaskStorage) -> None:
        """Test that description exceeding 1000 chars displays error."""
        command = AddTaskCommand(storage)
        long_description = "x" * 1001
        with patch("src.commands.add.console") as mock_console:
            with patch("src.commands.add.display_error") as mock_error:
                mock_console.input.side_effect = ["Valid title", long_description]
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with(
            "Description must be 1000 characters or less"
        )

    def test_whitespace_only_title_shows_error(self, storage: TaskStorage) -> None:
        """Test that whitespace-only title displays error."""
        command = AddTaskCommand(storage)
        with patch("src.commands.add.console") as mock_console:
            with patch("src.commands.add.display_error") as mock_error:
                mock_console.input.side_effect = ["   ", ""]
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Title is required (1-200 characters)")

    def test_title_at_max_length_succeeds(self, storage: TaskStorage) -> None:
        """Test that title at exactly 200 chars succeeds."""
        command = AddTaskCommand(storage)
        max_title = "x" * 200
        with patch("src.commands.add.console") as mock_console:
            mock_console.input.side_effect = [max_title, ""]
            result = command.execute()

        assert result is not None
        assert len(result.title) == 200

    def test_description_at_max_length_succeeds(self, storage: TaskStorage) -> None:
        """Test that description at exactly 1000 chars succeeds."""
        command = AddTaskCommand(storage)
        max_description = "x" * 1000
        with patch("src.commands.add.console") as mock_console:
            mock_console.input.side_effect = ["Valid title", max_description]
            result = command.execute()

        assert result is not None
        assert len(result.description) == 1000
