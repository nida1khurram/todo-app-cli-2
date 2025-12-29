# Quickstart Guide: CLI Todo Application (Phase I)

**Feature**: CLI Todo Application (Phase I)
**Branch**: `1-cli-todo-app`
**Date**: 2025-12-28

## Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Terminal/Command Prompt

### Install UV (if not installed)

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verify Installation

```bash
python --version   # Should be 3.13+
uv --version       # Should show UV version
```

---

## Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/nida1khurram/todo-app-cli.git
cd todo-app-cli
git checkout 1-cli-todo-app
```

### 2. Create Virtual Environment

```bash
uv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
uv sync
```

### 5. Run Application

```bash
python -m src.main
```

---

## Project Structure

```
todo-app-cli/
├── pyproject.toml          # UV project configuration
├── src/
│   ├── __init__.py
│   ├── main.py             # Entry point
│   ├── models.py           # Pydantic Task model
│   ├── storage.py          # In-memory storage
│   ├── ui.py               # Rich console utilities
│   └── commands/
│       ├── __init__.py
│       ├── base.py         # Abstract Command
│       ├── add.py          # Add task
│       ├── delete.py       # Delete task
│       ├── update.py       # Update task
│       ├── list.py         # List tasks
│       └── complete.py     # Mark complete
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest fixtures
│   └── ...
└── specs/
    └── 1-cli-todo-app/
        ├── spec.md
        ├── plan.md
        └── ...
```

---

## Usage Examples

### Add a Task

```
Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread

✓ Task added successfully: "Buy groceries" (ID: 1)
```

### List Tasks

```
Enter your choice (1-6): 2

┌─────┬────────┬──────────────────────────────────────────┬──────────────────────┐
│ ID  │ Status │ Title                                    │ Created              │
├─────┼────────┼──────────────────────────────────────────┼──────────────────────┤
│ 1   │ ○      │ Buy groceries                            │ 2025-12-28 10:30:00  │
└─────┴────────┴──────────────────────────────────────────┴──────────────────────┘

Total: 1 task (1 pending, 0 completed)
```

### Mark Task Complete

```
Enter your choice (1-6): 5
Enter task ID to mark complete: 1

✓ Task marked as complete: "Buy groceries" (ID: 1)
```

### Update a Task

```
Enter your choice (1-6): 3
Enter task ID to update: 1
Enter new title (press Enter to keep current): Buy organic groceries
Enter new description (press Enter to keep current):

✓ Task updated successfully: "Buy organic groceries" (ID: 1)
```

### Delete a Task

```
Enter your choice (1-6): 4
Enter task ID to delete: 1

✓ Task deleted successfully: "Buy organic groceries" (ID: 1)
```

### Exit Application

```
Enter your choice (1-6): 6

👋 Goodbye! Your tasks were not saved (in-memory storage).
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_models.py
```

---

## Development Commands

### Format Code

```bash
ruff format .
```

### Lint Code

```bash
ruff check .
```

### Type Check

```bash
# If mypy installed
mypy src/
```

---

## Troubleshooting

### "Python not found"

Ensure Python 3.13+ is installed and in PATH:
```bash
python --version
```

### "UV not found"

Install UV using the commands in Prerequisites section.

### "Module not found"

Activate virtual environment and run `uv sync`:
```bash
# Windows
.venv\Scripts\Activate.ps1
uv sync

# Linux/macOS
source .venv/bin/activate
uv sync
```

### "Permission denied" (Windows)

Run PowerShell as Administrator, then:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pydantic | 2.0+ | Data validation |
| rich | 13.0+ | Terminal UI |
| pytest | 7.0+ | Testing |
| pytest-cov | * | Coverage |
| ruff | * | Linting |

---

## Notes

- **In-memory storage**: All tasks are lost when you exit. This is expected behavior for Phase I.
- **Single user**: The app runs for one user session at a time.
- **No persistence**: Database storage comes in Phase II.

---

## Next Steps

After completing Phase I:
1. Run `/sp.tasks` to generate implementation tasks
2. Run `/sp.implement` to start coding
3. Ensure all tests pass with 80%+ coverage
4. Submit via the hackathon form

---

**Quickstart Status**: COMPLETE
