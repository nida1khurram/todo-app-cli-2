# Implementation Plan: CLI Todo Application (Phase I)

**Branch**: `1-cli-todo-app` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-cli-todo-app/spec.md`

## Summary

Build a command-line todo application in Python 3.13+ with in-memory storage that implements 5 basic CRUD operations (Add, View, Update, Delete, Mark Complete). The application uses Rich library for beautiful terminal UI, Pydantic for data validation, and follows the Command pattern for clean architecture.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Rich v13.0+, Pydantic v2.0+
**Storage**: In-Memory Dictionary (no database)
**Testing**: pytest v7.0+, pytest-cov
**Target Platform**: Windows/Linux/macOS Terminal
**Project Type**: Single CLI project
**Performance Goals**: Handle 100+ tasks without noticeable degradation
**Constraints**: In-memory only, single user session, no persistence
**Scale/Scope**: Single user, one session at a time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Specification complete, plan follows spec |
| II. AI-Native Architecture | PASS | Using Claude Code for implementation |
| III. Cloud-Native Design | N/A | Phase I is local CLI only |
| IV. Zero-Cost Development | PASS | All tools/libraries are free |
| V. Test-First Quality | PASS | pytest with 80% coverage target |
| VI. Security by Default | PASS | No secrets needed for Phase I |

**Gate Status**: PASS - All applicable principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/1-cli-todo-app/
├── plan.md              # This file
├── research.md          # Phase 0 output (complete)
├── data-model.md        # Phase 1 output (complete)
├── quickstart.md        # Phase 1 output (complete)
├── contracts/
│   └── cli-interface.md # CLI interface contract (complete)
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Entry point with main menu loop
├── models.py            # Pydantic Task, TaskCreate, TaskUpdate
├── storage.py           # TaskStorage class (in-memory dict)
├── ui.py                # Rich Console utilities
└── commands/
    ├── __init__.py      # Command exports
    ├── base.py          # Abstract Command class
    ├── add.py           # AddTaskCommand
    ├── delete.py        # DeleteTaskCommand
    ├── update.py        # UpdateTaskCommand
    ├── list.py          # ListTasksCommand
    └── complete.py      # CompleteTaskCommand

tests/
├── __init__.py
├── conftest.py          # pytest fixtures (storage, sample tasks)
├── test_models.py       # Task model validation tests
├── test_storage.py      # Storage CRUD tests
└── test_commands/
    ├── __init__.py
    ├── test_add.py      # AddTaskCommand tests
    ├── test_delete.py   # DeleteTaskCommand tests
    ├── test_update.py   # UpdateTaskCommand tests
    ├── test_list.py     # ListTasksCommand tests
    └── test_complete.py # CompleteTaskCommand tests
```

**Structure Decision**: Single project layout selected per constitution Section 4.5. The `src/` directory contains all application code with `commands/` subdirectory implementing the Command pattern. Tests mirror source structure under `tests/`.

## Complexity Tracking

> No constitution violations - complexity tracking not required.

| Item | Status |
|------|--------|
| Max 3 projects | PASS (1 project) |
| No Repository pattern | PASS (direct storage) |
| No premature abstractions | PASS |
| Minimal dependencies | PASS (only Rich, Pydantic, pytest) |

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Main Loop                             │   │
│  │  1. Display menu (ui.py)                                 │   │
│  │  2. Get user choice                                      │   │
│  │  3. Execute command                                      │   │
│  │  4. Display result                                       │   │
│  │  5. Loop until exit                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────────┐
│    ui.py        │   │   storage.py    │   │    commands/        │
│                 │   │                 │   │                     │
│ - Console       │   │ - TaskStorage   │   │ - AddTaskCommand    │
│ - display_menu  │   │   - add()       │   │ - ListTasksCommand  │
│ - display_table │   │   - get()       │   │ - UpdateTaskCommand │
│ - success_msg   │   │   - get_all()   │   │ - DeleteTaskCommand │
│ - error_msg     │   │   - update()    │   │ - CompleteCommand   │
│                 │   │   - delete()    │   │                     │
└─────────────────┘   │   - complete()  │   └──────────┬──────────┘
                      └────────┬────────┘              │
                               │                       │
                               └───────────────────────┘
                                         │
                                         ▼
                               ┌─────────────────┐
                               │   models.py     │
                               │                 │
                               │ - Task          │
                               │ - TaskCreate    │
                               │ - TaskUpdate    │
                               └─────────────────┘
```

### Data Flow

```
User Input → Main Loop → Command → Storage → Model → Storage → Command → UI → User Output
```

## Implementation Phases

### Phase 1: Foundation (models.py, storage.py)

1. Create `pyproject.toml` with UV configuration
2. Implement `Task`, `TaskCreate`, `TaskUpdate` Pydantic models
3. Implement `TaskStorage` class with CRUD operations
4. Write unit tests for models and storage

### Phase 2: Commands (commands/)

1. Implement abstract `Command` base class
2. Implement `AddTaskCommand`
3. Implement `ListTasksCommand`
4. Implement `UpdateTaskCommand`
5. Implement `DeleteTaskCommand`
6. Implement `CompleteTaskCommand`
7. Write unit tests for each command

### Phase 3: UI Layer (ui.py, main.py)

1. Implement Rich console utilities in `ui.py`
2. Implement main menu display
3. Implement task table display
4. Implement success/error message formatting
5. Implement main loop in `main.py`
6. Write integration tests

### Phase 4: Polish & Documentation

1. Add comprehensive docstrings
2. Ensure PEP 8 compliance (ruff)
3. Achieve 80%+ test coverage
4. Update README.md with setup instructions

## Key Design Decisions

### 1. Command Pattern

**Why**: Clean separation between UI and business logic. Each command is independently testable.

### 2. Dependency Injection

**Why**: Storage is passed to commands, making testing easy with mock storage.

### 3. Pydantic for Validation

**Why**: Type-safe validation with clear error messages. Constitution requirement.

### 4. Rich for UI

**Why**: Beautiful terminal output with tables, colors, and formatting. Constitution requirement.

### 5. In-Memory Storage

**Why**: Phase I requirement. No database complexity, data lost on exit is expected.

## Success Criteria Mapping

| Spec Criteria | Implementation |
|---------------|----------------|
| SC-001: Add task < 30s | Command pattern + Rich prompt |
| SC-002: View with single selection | ListTasksCommand |
| SC-003: All 5 operations work | 5 command classes |
| SC-004: Invalid input shows errors | Pydantic validation + Rich error display |
| SC-005: 100+ tasks without degradation | O(1) dict operations |
| SC-006: Color-coded messages | Rich console styles |
| SC-007: Formatted table | Rich Table component |
| SC-008: Clean exit | Graceful exit handling |
| SC-009: All acceptance scenarios pass | pytest test suite |
| SC-010: 80% code coverage | pytest-cov configuration |

## Dependencies

```toml
[project]
name = "todo-cli"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "pydantic>=2.0",
    "rich>=13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff",
]
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Rich compatibility | Test early on Python 3.13 |
| Pydantic validation complexity | Follow Pydantic v2 docs |
| Coverage target | Write tests alongside code |

## Next Steps

1. Run `/sp.tasks` to generate detailed task breakdown
2. Run `/sp.implement` to start implementation
3. Follow TDD: write tests before implementation
4. Use `python-console-agent` for CLI-specific guidance

## Artifacts Created

| Artifact | Path | Status |
|----------|------|--------|
| Research | `specs/1-cli-todo-app/research.md` | Complete |
| Data Model | `specs/1-cli-todo-app/data-model.md` | Complete |
| CLI Contract | `specs/1-cli-todo-app/contracts/cli-interface.md` | Complete |
| Quickstart | `specs/1-cli-todo-app/quickstart.md` | Complete |
| Plan | `specs/1-cli-todo-app/plan.md` | Complete |

---

**Plan Status**: COMPLETE
**Ready for**: `/sp.tasks` command to generate implementation tasks
