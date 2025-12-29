"""Rich console utilities for Todo CLI Application."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models import Task

# Console singleton
console = Console()


def display_success(message: str) -> None:
    """Display a success message in green.

    Args:
        message: The success message to display
    """
    console.print(f"[green]✓ {message}[/green]")


def display_error(message: str) -> None:
    """Display an error message in red.

    Args:
        message: The error message to display
    """
    console.print(f"[red]✗ Error: {message}[/red]")


def display_info(message: str) -> None:
    """Display an informational message in yellow.

    Args:
        message: The info message to display
    """
    console.print(f"[yellow]ℹ {message}[/yellow]")


def display_menu() -> None:
    """Display the main menu with numbered options."""
    menu_content = """[bold]1.[/bold] Add Task
[bold]2.[/bold] List Tasks
[bold]3.[/bold] Update Task
[bold]4.[/bold] Delete Task
[bold]5.[/bold] Mark Complete
[bold]6.[/bold] Exit"""

    panel = Panel(
        menu_content,
        title="[bold cyan]Todo Manager[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


def display_task_table(tasks: list[Task]) -> None:
    """Display tasks in a formatted Rich table.

    Args:
        tasks: List of tasks to display
    """
    if not tasks:
        display_info("No tasks found. Add your first task!")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Status", width=8)
    table.add_column("Title", width=30)
    table.add_column("Description", width=35)
    table.add_column("Created", width=20)

    pending_count = 0
    completed_count = 0

    for task in tasks:
        status = "[green]✓[/green]" if task.completed else "[yellow]○[/yellow]"
        if task.completed:
            completed_count += 1
        else:
            pending_count += 1

        created_str = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
        description = task.description if task.description else "-"
        table.add_row(str(task.id), status, task.title, description, created_str)

    console.print(table)
    summary = f"\nTotal: {len(tasks)} task(s) "
    summary += f"({pending_count} pending, {completed_count} completed)"
    console.print(summary)
