"""Tests for UpdateTaskCommand."""

from unittest.mock import patch

from src.commands.update import UpdateTaskCommand
from src.models import TaskCreate
from src.storage import TaskStorage


class TestUpdateTaskCommandSuccess:
    """Tests for successful task updates."""

    def test_update_title_only(self, storage: TaskStorage) -> None:
        """Test updating only the task title."""
        storage.add(TaskCreate(title="Original title"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success") as mock_success:
                mock_console.input.side_effect = ["1", "New title", ""]
                result = command.execute()

        assert result is not None
        assert result.title == "New title"
        mock_success.assert_called_once()

    def test_update_description_only(self, storage: TaskStorage) -> None:
        """Test updating only the task description."""
        storage.add(TaskCreate(title="Test task", description="Original desc"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success") as mock_success:
                mock_console.input.side_effect = ["1", "", "New description"]
                result = command.execute()

        assert result is not None
        assert result.description == "New description"
        mock_success.assert_called_once()

    def test_update_both_title_and_description(self, storage: TaskStorage) -> None:
        """Test updating both title and description."""
        storage.add(TaskCreate(title="Original", description="Original desc"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success") as mock_success:
                mock_console.input.side_effect = ["1", "New title", "New desc"]
                result = command.execute()

        assert result is not None
        assert result.title == "New title"
        assert result.description == "New desc"
        mock_success.assert_called_once()

    def test_update_persists_to_storage(self, storage: TaskStorage) -> None:
        """Test that updates are persisted to storage."""
        storage.add(TaskCreate(title="Original"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success"):
                mock_console.input.side_effect = ["1", "Updated title", ""]
                command.execute()

        # Verify storage was updated
        task = storage.get(1)
        assert task.title == "Updated title"


class TestUpdateTaskCommandPartialUpdate:
    """Tests for partial update scenarios."""

    def test_keeps_original_title_when_empty(self, storage: TaskStorage) -> None:
        """Test that original title is kept when empty input provided."""
        storage.add(TaskCreate(title="Original title", description="desc"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success"):
                mock_console.input.side_effect = ["1", "", "New description"]
                result = command.execute()

        assert result.title == "Original title"
        assert result.description == "New description"

    def test_keeps_original_description_when_empty(self, storage: TaskStorage) -> None:
        """Test that original description is kept when empty input provided."""
        storage.add(TaskCreate(title="Original", description="Original desc"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success"):
                mock_console.input.side_effect = ["1", "New title", ""]
                result = command.execute()

        assert result.title == "New title"
        assert result.description == "Original desc"


class TestUpdateTaskCommandNoChanges:
    """Tests for no-changes scenario."""

    def test_no_changes_shows_info(self, storage: TaskStorage) -> None:
        """Test that no changes shows info message."""
        storage.add(TaskCreate(title="Test task"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_info") as mock_info:
                mock_console.input.side_effect = ["1", "", ""]
                result = command.execute()

        assert result is not None
        mock_info.assert_called_once_with("No changes made")

    def test_no_changes_returns_original_task(self, storage: TaskStorage) -> None:
        """Test that no changes returns the original task."""
        storage.add(TaskCreate(title="Test task", description="Test desc"))
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_info"):
                mock_console.input.side_effect = ["1", "", ""]
                result = command.execute()

        assert result.title == "Test task"
        assert result.description == "Test desc"


class TestUpdateTaskCommandNotFound:
    """Tests for task not found scenarios."""

    def test_nonexistent_task_shows_error(self, storage: TaskStorage) -> None:
        """Test that nonexistent task ID shows error."""
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_error") as mock_error:
                mock_console.input.return_value = "999"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Task not found with ID: 999")

    def test_invalid_id_non_numeric_shows_error(self, storage: TaskStorage) -> None:
        """Test that non-numeric ID shows error."""
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_error") as mock_error:
                mock_console.input.return_value = "abc"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_zero_shows_error(self, storage: TaskStorage) -> None:
        """Test that zero ID shows error."""
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_error") as mock_error:
                mock_console.input.return_value = "0"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")

    def test_invalid_id_negative_shows_error(self, storage: TaskStorage) -> None:
        """Test that negative ID shows error."""
        command = UpdateTaskCommand(storage)

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_error") as mock_error:
                mock_console.input.return_value = "-1"
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Invalid task ID. Please enter a number.")


class TestUpdateTaskCommandValidation:
    """Tests for input validation."""

    def test_title_too_long_shows_error(self, storage: TaskStorage) -> None:
        """Test that title exceeding 200 chars shows error."""
        storage.add(TaskCreate(title="Test"))
        command = UpdateTaskCommand(storage)
        long_title = "x" * 201

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_error") as mock_error:
                mock_console.input.side_effect = ["1", long_title, ""]
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with("Title must be 200 characters or less")

    def test_description_too_long_shows_error(self, storage: TaskStorage) -> None:
        """Test that description exceeding 1000 chars shows error."""
        storage.add(TaskCreate(title="Test"))
        command = UpdateTaskCommand(storage)
        long_desc = "x" * 1001

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_error") as mock_error:
                mock_console.input.side_effect = ["1", "", long_desc]
                result = command.execute()

        assert result is None
        mock_error.assert_called_once_with(
            "Description must be 1000 characters or less"
        )

    def test_title_at_max_length_succeeds(self, storage: TaskStorage) -> None:
        """Test that title at exactly 200 chars succeeds."""
        storage.add(TaskCreate(title="Test"))
        command = UpdateTaskCommand(storage)
        max_title = "x" * 200

        with patch("src.commands.update.console") as mock_console:
            with patch("src.commands.update.display_success"):
                mock_console.input.side_effect = ["1", max_title, ""]
                result = command.execute()

        assert result is not None
        assert result.title == max_title
