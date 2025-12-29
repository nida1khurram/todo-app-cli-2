# CLI Interface Contract: Todo Application (Phase I)

**Feature**: CLI Todo Application (Phase I)
**Branch**: `1-cli-todo-app`
**Date**: 2025-12-28
**Type**: Command-Line Interface Contract

## Overview

This document defines the CLI interface contract for Phase I. Unlike REST APIs, CLI apps use menu-driven interaction with the user.

---

## Main Menu Contract

### Menu Display

```
╔══════════════════════════════════════════════════════════╗
║                     Todo Manager                          ║
╠══════════════════════════════════════════════════════════╣
║  1. Add Task                                              ║
║  2. List Tasks                                            ║
║  3. Update Task                                           ║
║  4. Delete Task                                           ║
║  5. Mark Complete                                         ║
║  6. Exit                                                  ║
╚══════════════════════════════════════════════════════════╝

Enter your choice (1-6): _
```

### Menu Options

| Option | Action | Triggers |
|--------|--------|----------|
| 1 | Add Task | Prompts for title and description |
| 2 | List Tasks | Displays task table |
| 3 | Update Task | Prompts for ID and new values |
| 4 | Delete Task | Prompts for ID |
| 5 | Mark Complete | Prompts for ID |
| 6 | Exit | Terminates application |

---

## Command Contracts

### 1. Add Task

**Input Prompts**:
```
Enter task title: _
Enter description (optional, press Enter to skip): _
```

**Success Output** (Green):
```
✓ Task added successfully: "Buy groceries" (ID: 1)
```

**Error Outputs** (Red):
```
✗ Error: Title is required (1-200 characters)
✗ Error: Title must be 200 characters or less
✗ Error: Description must be 1000 characters or less
```

---

### 2. List Tasks

**Success Output** (with tasks):
```
┌─────┬────────┬──────────────────────────────────────────┬──────────────────────┐
│ ID  │ Status │ Title                                    │ Created              │
├─────┼────────┼──────────────────────────────────────────┼──────────────────────┤
│ 1   │ ○      │ Buy groceries                            │ 2025-12-28 10:30:00  │
│ 2   │ ✓      │ Call mom                                 │ 2025-12-28 09:15:00  │
│ 3   │ ○      │ Finish project report                    │ 2025-12-28 11:45:00  │
└─────┴────────┴──────────────────────────────────────────┴──────────────────────┘

Total: 3 tasks (2 pending, 1 completed)
```

**Empty State Output** (Yellow):
```
ℹ No tasks found. Add your first task!
```

---

### 3. Update Task

**Input Prompts**:
```
Enter task ID to update: _
Enter new title (press Enter to keep current): _
Enter new description (press Enter to keep current): _
```

**Success Output** (Green):
```
✓ Task updated successfully: "Buy organic groceries" (ID: 1)
```

**No Changes Output** (Yellow):
```
ℹ No changes made
```

**Error Outputs** (Red):
```
✗ Error: Task not found with ID: 999
✗ Error: Invalid task ID. Please enter a number.
✗ Error: Title must be 200 characters or less
```

---

### 4. Delete Task

**Input Prompts**:
```
Enter task ID to delete: _
```

**Success Output** (Green):
```
✓ Task deleted successfully: "Buy groceries" (ID: 1)
```

**Error Outputs** (Red):
```
✗ Error: Task not found with ID: 999
✗ Error: Invalid task ID. Please enter a number.
```

---

### 5. Mark Complete

**Input Prompts**:
```
Enter task ID to mark complete: _
```

**Success Output** (Green):
```
✓ Task marked as complete: "Buy groceries" (ID: 1)
```

**Already Complete Output** (Yellow):
```
ℹ Task is already completed: "Buy groceries" (ID: 1)
```

**Error Outputs** (Red):
```
✗ Error: Task not found with ID: 999
✗ Error: Invalid task ID. Please enter a number.
```

---

### 6. Exit

**Output** (Cyan):
```
👋 Goodbye! Your tasks were not saved (in-memory storage).
```

---

## Error Handling Contract

### Invalid Menu Selection

```
✗ Invalid option. Please choose 1-6.
```

### Keyboard Interrupt (Ctrl+C)

```
ℹ Operation cancelled.
```

### General Error

```
✗ An unexpected error occurred: {error_message}
```

---

## Color Scheme Contract

| Color | Usage |
|-------|-------|
| Green | Success messages |
| Red | Error messages |
| Yellow | Warnings, informational |
| Cyan | Exit message |
| White | Normal text |
| Bold | Headers, titles |

---

## Symbol Contract

| Symbol | Meaning |
|--------|---------|
| ✓ | Success / Completed task |
| ✗ | Error |
| ○ | Pending task |
| ℹ | Information |
| 👋 | Goodbye |

---

## Input Validation Contract

### Task ID Input

| Input | Response |
|-------|----------|
| Valid number | Proceed with operation |
| Empty | "Invalid task ID. Please enter a number." |
| Non-numeric | "Invalid task ID. Please enter a number." |
| Negative | "Invalid task ID. Please enter a number." |
| Zero | "Invalid task ID. Please enter a number." |
| Not found | "Task not found with ID: {id}" |

### Title Input

| Input | Response |
|-------|----------|
| 1-200 chars | Valid |
| Empty | "Title is required (1-200 characters)" |
| > 200 chars | "Title must be 200 characters or less" |

### Description Input

| Input | Response |
|-------|----------|
| 0-1000 chars | Valid |
| Empty | Set to None |
| > 1000 chars | "Description must be 1000 characters or less" |

---

## Command Pattern Contract

### Base Command Interface

```python
from abc import ABC, abstractmethod
from typing import Any

class Command(ABC):
    """Abstract base class for all commands."""

    @abstractmethod
    def execute(self) -> Any:
        """Execute the command and return result."""
        pass
```

### Command Implementations

| Command Class | Method | Returns |
|---------------|--------|---------|
| `AddTaskCommand` | `execute()` | `Task` |
| `ListTasksCommand` | `execute()` | `list[Task]` |
| `UpdateTaskCommand` | `execute()` | `Task | None` |
| `DeleteTaskCommand` | `execute()` | `Task | None` |
| `CompleteTaskCommand` | `execute()` | `Task | None` |

---

## Screen Flow Contract

```
┌──────────────┐
│   Start      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Main Menu   │◄──────────────────────────────┐
└──────┬───────┘                               │
       │                                        │
       ├──1──▶ Add Task ──────────────────────┤
       │                                        │
       ├──2──▶ List Tasks ────────────────────┤
       │                                        │
       ├──3──▶ Update Task ───────────────────┤
       │                                        │
       ├──4──▶ Delete Task ───────────────────┤
       │                                        │
       ├──5──▶ Mark Complete ─────────────────┤
       │
       └──6──▶ Exit
              │
              ▼
       ┌──────────────┐
       │     End      │
       └──────────────┘
```

---

**Contract Status**: COMPLETE
**Ready for**: Implementation
