# Todo CLI Application

A command-line todo manager built with Python, featuring a clean Rich-based UI.

## Features

- Add tasks with title and optional description
- View all tasks in a formatted table
- Update task title and description
- Delete tasks by ID
- Mark tasks as complete
- Input validation with helpful error messages

## Requirements

- Python 3.13+
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hac2-todoapp
```

2. Install dependencies using UV:
```bash
uv sync
```

## Usage

Run the application:
```bash
uv run python -m src.main
```

### Menu Options

1. **Add Task** - Create a new task with title and optional description
2. **View Tasks** - Display all tasks in a formatted table
3. **Update Task** - Modify an existing task's title or description
4. **Delete Task** - Remove a task by ID
5. **Mark Complete** - Mark a task as done
6. **Exit** - Close the application

## Development

### Running Tests

```bash
uv run pytest -v
```

### Running Tests with Coverage

```bash
uv run pytest --cov=src --cov-report=term-missing
```

### Code Formatting

```bash
uv run ruff format .
```

### Linting

```bash
uv run ruff check . --fix
```

## Project Structure

```
hac2-todoapp/
├── src/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── models.py         # Pydantic data models
│   ├── storage.py        # In-memory task storage
│   ├── ui.py             # Rich console UI utilities
│   └── commands/
│       ├── __init__.py
│       ├── base.py       # Abstract Command base class
│       ├── add.py        # Add task command
│       ├── list.py       # List tasks command
│       ├── update.py     # Update task command
│       ├── delete.py     # Delete task command
│       └── complete.py   # Mark complete command
├── tests/
│   ├── conftest.py       # Pytest fixtures
│   ├── test_models.py
│   ├── test_storage.py
│   ├── test_main.py
│   └── test_commands/
│       ├── test_add.py
│       ├── test_list.py
│       ├── test_update.py
│       ├── test_delete.py
│       └── test_complete.py
├── pyproject.toml
└── README.md
```

## Tech Stack

- **Python 3.13+** - Core language
- **Pydantic** - Data validation
- **Rich** - Terminal UI formatting
- **pytest** - Testing framework
- **UV** - Package management

## Note

This application uses in-memory storage. Tasks are not persisted between sessions.
