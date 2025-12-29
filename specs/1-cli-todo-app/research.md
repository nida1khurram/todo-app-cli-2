# Research Document: CLI Todo Application (Phase I)

**Feature**: CLI Todo Application (Phase I)
**Branch**: `1-cli-todo-app`
**Date**: 2025-12-28
**Status**: Complete

## Overview

This document captures research findings and technical decisions for Phase I of the Evolution of Todo project - an in-memory Python console application.

## Technical Decisions

### 1. Runtime Environment

**Decision**: Python 3.13+

**Rationale**:
- Required by hackathon specification
- Latest stable Python with improved performance
- Full type hint support including generics
- Better error messages for debugging

**Alternatives Considered**:
- Python 3.12: Slightly older, less features
- Python 3.11: Would work but older than required

---

### 2. Package Manager

**Decision**: UV Package Manager

**Rationale**:
- Required by hackathon specification
- 10-100x faster than pip
- Built-in virtual environment management
- Modern `pyproject.toml` support
- Written in Rust for performance

**Alternatives Considered**:
- pip + venv: Traditional but slower
- Poetry: Good but UV is faster and hackathon requirement
- PDM: Good alternative but UV specified

---

### 3. CLI Framework

**Decision**: Rich Library v13.0+

**Rationale**:
- Required by hackathon specification
- Beautiful terminal output with colors
- Built-in Table, Panel, and Progress components
- Console class for structured output
- Prompt class for user input

**Alternatives Considered**:
- Click: Good for CLI parsing but Rich better for UI
- Typer: Built on Click, could combine with Rich
- argparse: Standard library but minimal UI

---

### 4. Data Validation

**Decision**: Pydantic v2.0+

**Rationale**:
- Required by hackathon specification
- Type-safe data models
- Built-in validation with Field constraints
- Automatic JSON serialization
- Excellent error messages

**Alternatives Considered**:
- dataclasses: Built-in but less validation
- attrs: Good but Pydantic is specified
- Manual validation: Error-prone

---

### 5. Storage Pattern

**Decision**: In-Memory Dictionary Storage

**Rationale**:
- Required for Phase I (database in Phase II)
- Simple dict[int, Task] structure
- Auto-incrementing ID counter
- Fast O(1) lookups by ID

**Alternatives Considered**:
- List storage: O(n) lookups by ID
- SQLite: Overkill for Phase I, planned for Phase II
- File-based: Not required for in-memory phase

---

### 6. Architecture Pattern

**Decision**: Command Pattern with Dependency Injection

**Rationale**:
- Clean separation of concerns
- Each command is independent and testable
- Storage injected into commands
- Easy to extend with new commands
- Follows constitution's architecture guidelines

**Alternatives Considered**:
- Simple functions: Less organized
- MVC: Overkill for CLI
- Repository pattern: Better for Phase II with DB

---

### 7. Testing Framework

**Decision**: pytest v7.0+

**Rationale**:
- Industry standard for Python
- Simple test discovery
- Fixtures for dependency injection
- Rich plugin ecosystem
- Constitution requires 80% coverage

**Alternatives Considered**:
- unittest: Built-in but verbose
- nose2: Less maintained
- hypothesis: Good for property testing, can add later

---

### 8. Project Structure

**Decision**: src/ layout with commands/ subdirectory

**Rationale**:
- Constitution specifies this structure (Section 4.5)
- Clear separation: models, storage, commands, ui
- Importable package structure
- Test directory at project root

**Structure**:
```
src/
├── __init__.py
├── main.py           # Entry point with main menu
├── models.py         # Pydantic Task model
├── storage.py        # In-memory TaskStorage class
├── ui.py             # Rich console utilities
└── commands/
    ├── __init__.py
    ├── base.py       # Abstract Command class
    ├── add.py        # AddTaskCommand
    ├── delete.py     # DeleteTaskCommand
    ├── update.py     # UpdateTaskCommand
    ├── list.py       # ListTasksCommand
    └── complete.py   # CompleteTaskCommand

tests/
├── __init__.py
├── conftest.py       # pytest fixtures
├── test_models.py
├── test_storage.py
└── test_commands/
    ├── test_add.py
    ├── test_delete.py
    ├── test_update.py
    ├── test_list.py
    └── test_complete.py
```

---

## Best Practices Applied

### Rich Library Best Practices

1. **Use Console singleton**: Create one Console instance for the app
2. **Use Panel for headers**: Wrap titles in Panel for emphasis
3. **Use Table for lists**: Display tasks in formatted tables
4. **Color coding**: Green for success, red for errors, yellow for warnings
5. **Prompt class**: Use for user input with validation

### Pydantic Best Practices

1. **Field constraints**: Use min_length, max_length on strings
2. **Default factories**: Use Field(default_factory=datetime.now) for timestamps
3. **Optional fields**: Use Optional[str] = None pattern
4. **Model validation**: Let Pydantic handle all validation

### Command Pattern Best Practices

1. **Abstract base class**: Define execute() method signature
2. **Dependency injection**: Pass storage to commands
3. **Single responsibility**: Each command does one thing
4. **Return types**: Commands return results, UI handles display

---

## Integration Patterns

### Main Loop Pattern

```
1. Display menu (Rich Table)
2. Get user input (Rich Prompt)
3. Validate selection
4. Execute command
5. Display result
6. Loop until exit
```

### Error Handling Pattern

```
1. Validate input in command
2. Raise descriptive exceptions
3. Catch in main loop
4. Display error with Rich console (red)
5. Continue loop
```

---

## Dependencies Summary

| Package | Version | Purpose |
|---------|---------|---------|
| python | 3.13+ | Runtime |
| pydantic | 2.0+ | Data validation |
| rich | 13.0+ | Terminal UI |
| pytest | 7.0+ | Testing |
| pytest-cov | * | Coverage reporting |
| ruff | * | Linting/formatting |

---

## Resolved Clarifications

All technical context items from the plan template have been resolved:

| Item | Status | Decision |
|------|--------|----------|
| Language/Version | Resolved | Python 3.13+ |
| Primary Dependencies | Resolved | Rich, Pydantic |
| Storage | Resolved | In-Memory Dict |
| Testing | Resolved | pytest |
| Target Platform | Resolved | Windows/Linux/macOS Terminal |
| Project Type | Resolved | Single CLI project |
| Performance Goals | Resolved | Handle 100+ tasks without degradation |
| Constraints | Resolved | In-memory only, single session |
| Scale/Scope | Resolved | Single user, single session |

---

## Next Steps

1. Create `data-model.md` with detailed entity definitions
2. Generate `quickstart.md` with setup instructions
3. Fill in `plan.md` template
4. Proceed to `/sp.tasks` for task generation

---

**Research Status**: COMPLETE
**Ready for**: Phase 1 Design
