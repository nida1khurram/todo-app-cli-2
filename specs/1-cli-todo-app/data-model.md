# Data Model: CLI Todo Application (Phase I)

**Feature**: CLI Todo Application (Phase I)
**Branch**: `1-cli-todo-app`
**Date**: 2025-12-28
**Status**: Complete

## Overview

This document defines the data models, validation rules, and state transitions for the Phase I CLI Todo Application.

---

## Entity Definitions

### Task Entity

The primary entity representing a todo item.

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    """
    Represents a single todo task.

    Attributes:
        id: Unique identifier (auto-incremented)
        title: Short description (1-200 characters, required)
        description: Detailed description (max 1000 characters, optional)
        completed: Whether the task is done (default: False)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
    """
    id: int = Field(..., ge=1, description="Unique task identifier")
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional detailed description"
    )
    completed: bool = Field(
        default=False,
        description="Completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Last modification timestamp"
    )
```

---

## Field Specifications

### id: int

| Property | Value |
|----------|-------|
| Type | Integer |
| Required | Yes (system-generated) |
| Constraints | >= 1, auto-incrementing |
| Default | None (assigned by storage) |
| Description | Unique identifier for the task |

### title: str

| Property | Value |
|----------|-------|
| Type | String |
| Required | Yes |
| Constraints | 1-200 characters |
| Default | None |
| Validation Error | "Title is required (1-200 characters)" |
| Description | Short description of the task |

### description: Optional[str]

| Property | Value |
|----------|-------|
| Type | String or None |
| Required | No |
| Constraints | Max 1000 characters |
| Default | None |
| Validation Error | "Description must be 1000 characters or less" |
| Description | Detailed task description |

### completed: bool

| Property | Value |
|----------|-------|
| Type | Boolean |
| Required | No |
| Constraints | True or False |
| Default | False |
| Description | Task completion status |

### created_at: datetime

| Property | Value |
|----------|-------|
| Type | datetime |
| Required | No (auto-generated) |
| Constraints | Must be valid datetime |
| Default | Current timestamp |
| Description | When the task was created |

### updated_at: datetime

| Property | Value |
|----------|-------|
| Type | datetime |
| Required | No (auto-generated) |
| Constraints | Must be valid datetime |
| Default | Current timestamp (updated on modify) |
| Description | When the task was last modified |

---

## Input Models

### TaskCreate

Model for creating a new task (user input).

```python
class TaskCreate(BaseModel):
    """Input model for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

### TaskUpdate

Model for updating an existing task (user input).

```python
class TaskUpdate(BaseModel):
    """Input model for updating a task. All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

---

## State Transitions

### Task Lifecycle

```
                    ┌──────────────┐
                    │   Created    │
                    │ (completed   │
                    │   = False)   │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   Updated    │ │  Completed   │ │   Deleted    │
    │ (title/desc) │ │ (completed   │ │  (removed)   │
    └──────────────┘ │   = True)    │ └──────────────┘
                     └──────────────┘
```

### State Transition Rules

| From State | To State | Action | Trigger |
|------------|----------|--------|---------|
| (new) | Created | Add Task | User creates task |
| Created | Updated | Update Task | User modifies title/description |
| Created | Completed | Mark Complete | User marks task done |
| Created | Deleted | Delete Task | User removes task |
| Completed | Completed | Mark Complete | No change (already complete) |
| Updated | Completed | Mark Complete | User marks task done |
| Updated | Deleted | Delete Task | User removes task |
| Completed | Deleted | Delete Task | User removes task |

---

## Storage Model

### TaskStorage Class

```python
from typing import Optional

class TaskStorage:
    """
    In-memory storage for tasks using dictionary.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for auto-incrementing IDs
    """
    _tasks: dict[int, Task]
    _next_id: int

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._tasks = {}
        self._next_id = 1

    def add(self, task_create: TaskCreate) -> Task:
        """
        Add a new task and return it with assigned ID.

        Args:
            task_create: Task creation data

        Returns:
            Created Task with ID and timestamps
        """
        ...

    def get(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: The task ID to look up

        Returns:
            Task if found, None otherwise
        """
        ...

    def get_all(self) -> list[Task]:
        """
        Get all tasks ordered by ID.

        Returns:
            List of all tasks
        """
        ...

    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: The task ID to update
            task_update: Fields to update

        Returns:
            Updated Task if found, None otherwise
        """
        ...

    def delete(self, task_id: int) -> Optional[Task]:
        """
        Delete a task by ID.

        Args:
            task_id: The task ID to delete

        Returns:
            Deleted Task if found, None otherwise
        """
        ...

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as completed.

        Args:
            task_id: The task ID to mark complete

        Returns:
            Updated Task if found, None otherwise
        """
        ...
```

---

## Validation Rules

### Title Validation

| Rule | Error Message |
|------|---------------|
| Cannot be empty | "Title is required (1-200 characters)" |
| Cannot exceed 200 chars | "Title must be 200 characters or less" |
| Must be string | Pydantic type error |

### Description Validation

| Rule | Error Message |
|------|---------------|
| Cannot exceed 1000 chars | "Description must be 1000 characters or less" |
| Can be None | No error |
| Must be string if provided | Pydantic type error |

### ID Validation

| Rule | Error Message |
|------|---------------|
| Must be positive integer | "Invalid task ID" |
| Must exist in storage | "Task not found with ID: {id}" |

---

## Display Format

### Task List Table

| Column | Width | Content |
|--------|-------|---------|
| ID | 5 | Task ID |
| Status | 8 | ✓ (complete) or ○ (pending) |
| Title | 40 | Task title (truncated if needed) |
| Created | 20 | Formatted datetime |

### Example Output

```
┌─────┬────────┬──────────────────────────────────────────┬──────────────────────┐
│ ID  │ Status │ Title                                    │ Created              │
├─────┼────────┼──────────────────────────────────────────┼──────────────────────┤
│ 1   │ ○      │ Buy groceries                            │ 2025-12-28 10:30:00  │
│ 2   │ ✓      │ Call mom                                 │ 2025-12-28 09:15:00  │
│ 3   │ ○      │ Finish project report                    │ 2025-12-28 11:45:00  │
└─────┴────────┴──────────────────────────────────────────┴──────────────────────┘
```

---

## Relationships

Phase I has no relationships (single entity model).

Future phases will add:
- **Phase II**: Task → User (many-to-one)
- **Phase III**: Task → Conversation (via messages)
- **Phase V**: Task → Category (many-to-one), Task → Tags (many-to-many)

---

## Data Model Status

| Item | Status |
|------|--------|
| Task entity defined | Complete |
| Field constraints specified | Complete |
| Input models defined | Complete |
| State transitions documented | Complete |
| Storage interface defined | Complete |
| Validation rules specified | Complete |
| Display format defined | Complete |

---

**Data Model Status**: COMPLETE
**Ready for**: Implementation Planning
