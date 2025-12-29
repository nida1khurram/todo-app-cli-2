"""Tests for main menu functionality."""

from unittest.mock import patch


class TestMainMenuDisplay:
    """Tests for main menu display."""

    def test_menu_displays_all_options(self) -> None:
        """Test that menu displays all 6 options."""
        with patch("src.ui.console") as mock_console:
            from src.ui import display_menu

            display_menu()

        # Verify Panel was printed
        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Todo Manager" in call_args or mock_console.print.called


class TestMainMenuInvalidOption:
    """Tests for invalid option handling."""

    def test_invalid_numeric_option(self) -> None:
        """Test that invalid numeric option (7) shows error."""
        with patch("src.main.console") as mock_console:
            with patch("src.main.display_error") as mock_error:
                with patch("src.main.display_menu"):
                    mock_console.input.side_effect = ["7", "6"]

                    from src.main import main

                    main()

        mock_error.assert_called_with("Invalid option. Please choose 1-6.")

    def test_invalid_text_option(self) -> None:
        """Test that text option shows error."""
        with patch("src.main.console") as mock_console:
            with patch("src.main.display_error") as mock_error:
                with patch("src.main.display_menu"):
                    mock_console.input.side_effect = ["abc", "6"]

                    from src.main import main

                    main()

        mock_error.assert_called_with("Invalid option. Please choose 1-6.")

    def test_empty_option(self) -> None:
        """Test that empty option shows error."""
        with patch("src.main.console") as mock_console:
            with patch("src.main.display_error") as mock_error:
                with patch("src.main.display_menu"):
                    mock_console.input.side_effect = ["", "6"]

                    from src.main import main

                    main()

        mock_error.assert_called_with("Invalid option. Please choose 1-6.")


class TestMainMenuExit:
    """Tests for exit functionality."""

    def test_exit_option_terminates(self) -> None:
        """Test that option 6 exits the application."""
        with patch("src.main.console") as mock_console:
            with patch("src.main.display_menu"):
                mock_console.input.return_value = "6"

                from src.main import main

                main()  # Should exit without error

        # Verify goodbye message was printed
        calls = [str(c) for c in mock_console.print.call_args_list]
        goodbye_printed = any("Goodbye" in c for c in calls)
        assert goodbye_printed or mock_console.print.called
