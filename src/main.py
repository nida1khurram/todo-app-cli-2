"""Main entry point for Todo CLI Application."""

from src.commands import AddTaskCommand, ListTasksCommand
from src.storage import TaskStorage
from src.ui import console, display_error, display_info, display_menu


def main() -> None:
    """Main entry point - runs the todo application."""
    storage = TaskStorage()

    console.print("\n[bold cyan]Welcome to Todo Manager![/bold cyan]\n")

    while True:
        try:
            display_menu()
            choice = console.input("\n[bold]Enter your choice (1-6):[/bold] ").strip()

            if choice == "1":
                # Add Task
                command = AddTaskCommand(storage)
                command.execute()
            elif choice == "2":
                # List Tasks
                command = ListTasksCommand(storage)
                command.execute()
            elif choice == "3":
                # Update Task
                from src.commands import UpdateTaskCommand

                command = UpdateTaskCommand(storage)
                command.execute()
            elif choice == "4":
                # Delete Task
                from src.commands import DeleteTaskCommand

                command = DeleteTaskCommand(storage)
                command.execute()
            elif choice == "5":
                # Mark Complete
                from src.commands import CompleteTaskCommand

                command = CompleteTaskCommand(storage)
                command.execute()
            elif choice == "6":
                # Exit
                goodbye_msg = "\n[cyan]Goodbye! "
                goodbye_msg += "Your tasks were not saved (in-memory storage).[/cyan]\n"
                console.print(goodbye_msg)
                break
            else:
                display_error("Invalid option. Please choose 1-6.")

            console.print()  # Add spacing between operations

        except KeyboardInterrupt:
            console.print("\n")
            display_info("Operation cancelled.")
            console.print()


if __name__ == "__main__":
    main()
