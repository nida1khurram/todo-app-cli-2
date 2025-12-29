# Tasks: CLI Todo Application (Phase I)

**Input**: Design documents from `/specs/1-cli-todo-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md
**Branch**: `1-cli-todo-app`
**Date**: 2025-12-28

**Tests**: Tests ARE included as per NFR-006 (test coverage for all CRUD operations) and SC-010 (80% coverage target).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure:
- **Source**: `src/` at repository root
- **Tests**: `tests/` at repository root
- **Commands**: `src/commands/` subdirectory

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Project initialization with UV and dependencies

- [x] T001 Create pyproject.toml with UV configuration in pyproject.toml
- [x] T002 [P] Create src/__init__.py package marker
- [x] T003 [P] Create src/commands/__init__.py package marker
- [x] T004 [P] Create tests/__init__.py package marker
- [x] T005 [P] Create tests/test_commands/__init__.py package marker
- [x] T006 Run `uv sync` to install dependencies and verify environment

**Checkpoint**: Project structure ready, dependencies installed

---

## Phase 2: Foundational (Core Models & Storage)

**Purpose**: Core infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Core Models

- [x] T007 Implement Task Pydantic model in src/models.py
- [x] T008 Implement TaskCreate input model in src/models.py
- [x] T009 Implement TaskUpdate input model in src/models.py

### Storage Layer

- [x] T010 Implement TaskStorage class with __init__ in src/storage.py
- [x] T011 Implement TaskStorage.add() method in src/storage.py
- [x] T012 Implement TaskStorage.get() method in src/storage.py
- [x] T013 Implement TaskStorage.get_all() method in src/storage.py
- [x] T014 Implement TaskStorage.update() method in src/storage.py
- [x] T015 Implement TaskStorage.delete() method in src/storage.py
- [x] T016 Implement TaskStorage.mark_complete() method in src/storage.py

### Command Pattern Base

- [x] T017 Implement abstract Command base class in src/commands/base.py

### UI Utilities

- [x] T018 [P] Create Console singleton in src/ui.py
- [x] T019 [P] Implement display_success() function in src/ui.py
- [x] T020 [P] Implement display_error() function in src/ui.py
- [x] T021 [P] Implement display_info() function in src/ui.py
- [x] T022 Implement display_menu() function in src/ui.py
- [x] T023 Implement display_task_table() function in src/ui.py

### Foundational Tests

- [x] T024 [P] Create pytest fixtures in tests/conftest.py
- [x] T025 [P] Write Task model validation tests in tests/test_models.py
- [x] T026 Write TaskStorage CRUD tests in tests/test_storage.py

**Checkpoint**: Foundation ready - models, storage, UI utilities, and base command in place

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks with title and optional description

**Independent Test**: Launch app → Select "Add Task" → Enter title → Verify confirmation message

### Implementation for User Story 1

- [x] T027 [US1] Implement AddTaskCommand class in src/commands/add.py
- [x] T028 [US1] Add input prompts for title and description in AddTaskCommand
- [x] T029 [US1] Add validation error handling for empty/long title in AddTaskCommand
- [x] T030 [US1] Add validation error handling for long description in AddTaskCommand
- [x] T031 [US1] Export AddTaskCommand in src/commands/__init__.py

### Tests for User Story 1

- [x] T032 [P] [US1] Write AddTaskCommand success tests in tests/test_commands/test_add.py
- [x] T033 [P] [US1] Write AddTaskCommand validation error tests in tests/test_commands/test_add.py

**Checkpoint**: User Story 1 complete - can add tasks with validation

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Display all tasks in a formatted Rich table

**Independent Test**: Add tasks → Select "List Tasks" → Verify formatted table with ID, Status, Title, Created

### Implementation for User Story 2

- [x] T034 [US2] Implement ListTasksCommand class in src/commands/list.py
- [x] T035 [US2] Add empty state handling ("No tasks found") in ListTasksCommand
- [x] T036 [US2] Add task count summary (pending/completed) in ListTasksCommand
- [x] T037 [US2] Export ListTasksCommand in src/commands/__init__.py

### Tests for User Story 2

- [x] T038 [P] [US2] Write ListTasksCommand with tasks tests in tests/test_commands/test_list.py
- [x] T039 [P] [US2] Write ListTasksCommand empty state tests in tests/test_commands/test_list.py

**Checkpoint**: User Story 2 complete - can view tasks in formatted table

---

## Phase 5: User Story 6 - Navigate Menu and Exit (Priority: P1) 🎯 MVP

**Goal**: Provide main menu navigation and graceful exit

**Independent Test**: Launch app → See numbered menu → Select Exit → App closes cleanly

### Implementation for User Story 6

- [x] T040 [US6] Implement main menu loop in src/main.py
- [x] T041 [US6] Add menu option selection and validation in src/main.py
- [x] T042 [US6] Add invalid option error handling in src/main.py
- [x] T043 [US6] Add graceful exit with goodbye message in src/main.py
- [x] T044 [US6] Add Ctrl+C (KeyboardInterrupt) handling in src/main.py

### Tests for User Story 6

- [x] T045 [P] [US6] Write main menu display tests in tests/test_main.py
- [x] T046 [P] [US6] Write invalid option handling tests in tests/test_main.py

**Checkpoint**: MVP Complete - Can add tasks, view list, navigate menu, and exit

---

## Phase 6: User Story 3 - Mark Task as Complete (Priority: P2)

**Goal**: Allow users to mark tasks as completed by ID

**Independent Test**: Add task → Mark complete by ID → View list → See checkmark (✓)

### Implementation for User Story 3

- [x] T047 [US3] Implement CompleteTaskCommand class in src/commands/complete.py
- [x] T048 [US3] Add task ID input prompt in CompleteTaskCommand
- [x] T049 [US3] Add "already completed" informational message in CompleteTaskCommand
- [x] T050 [US3] Add "task not found" error handling in CompleteTaskCommand
- [x] T051 [US3] Export CompleteTaskCommand in src/commands/__init__.py

### Tests for User Story 3

- [x] T052 [P] [US3] Write CompleteTaskCommand success tests in tests/test_commands/test_complete.py
- [x] T053 [P] [US3] Write CompleteTaskCommand already-complete tests in tests/test_commands/test_complete.py
- [x] T054 [P] [US3] Write CompleteTaskCommand not-found tests in tests/test_commands/test_complete.py

**Checkpoint**: User Story 3 complete - can mark tasks as complete

---

## Phase 7: User Story 4 - Update Task (Priority: P2)

**Goal**: Allow users to update task title and/or description

**Independent Test**: Add task → Update title → View list → See updated title

### Implementation for User Story 4

- [x] T055 [US4] Implement UpdateTaskCommand class in src/commands/update.py
- [x] T056 [US4] Add task ID input prompt in UpdateTaskCommand
- [x] T057 [US4] Add optional title/description prompts in UpdateTaskCommand
- [x] T058 [US4] Add "no changes made" handling in UpdateTaskCommand
- [x] T059 [US4] Add "task not found" error handling in UpdateTaskCommand
- [x] T060 [US4] Export UpdateTaskCommand in src/commands/__init__.py

### Tests for User Story 4

- [x] T061 [P] [US4] Write UpdateTaskCommand success tests in tests/test_commands/test_update.py
- [x] T062 [P] [US4] Write UpdateTaskCommand partial-update tests in tests/test_commands/test_update.py
- [x] T063 [P] [US4] Write UpdateTaskCommand no-changes tests in tests/test_commands/test_update.py
- [x] T064 [P] [US4] Write UpdateTaskCommand not-found tests in tests/test_commands/test_update.py

**Checkpoint**: User Story 4 complete - can update tasks

---

## Phase 8: User Story 5 - Delete Task (Priority: P3)

**Goal**: Allow users to delete tasks by ID

**Independent Test**: Add task → Delete by ID → View list → Task not shown

### Implementation for User Story 5

- [x] T065 [US5] Implement DeleteTaskCommand class in src/commands/delete.py
- [x] T066 [US5] Add task ID input prompt in DeleteTaskCommand
- [x] T067 [US5] Add "task not found" error handling in DeleteTaskCommand
- [x] T068 [US5] Export DeleteTaskCommand in src/commands/__init__.py

### Tests for User Story 5

- [x] T069 [P] [US5] Write DeleteTaskCommand success tests in tests/test_commands/test_delete.py
- [x] T070 [P] [US5] Write DeleteTaskCommand not-found tests in tests/test_commands/test_delete.py

**Checkpoint**: User Story 5 complete - can delete tasks

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Quality assurance and documentation

- [x] T071 [P] Add comprehensive docstrings to all modules
- [x] T072 [P] Run ruff format for PEP 8 compliance
- [x] T073 [P] Run ruff check and fix any linting issues
- [x] T074 Verify 80% test coverage with pytest --cov=src
- [x] T075 [P] Update README.md with setup and usage instructions
- [x] T076 Run full test suite and verify all acceptance scenarios pass
- [x] T077 Manual testing: Run quickstart.md validation steps

**Checkpoint**: All quality standards met, ready for submission

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all user stories)
    ↓
┌───────────────────────────────────────────────────┐
│ After Foundational, user stories can proceed:     │
│                                                   │
│   Phase 3: US1 (Add Task) ─────────┐              │
│   Phase 4: US2 (View Tasks) ───────┼── P1 MVP    │
│   Phase 5: US6 (Menu/Exit) ────────┘              │
│                                                   │
│   Phase 6: US3 (Complete) ─────────┐              │
│   Phase 7: US4 (Update) ───────────┴── P2        │
│                                                   │
│   Phase 8: US5 (Delete) ───────────── P3         │
└───────────────────────────────────────────────────┘
    ↓
Phase 9: Polish
```

### User Story Dependencies

| User Story | Depends On | Can Run In Parallel With |
|------------|------------|--------------------------|
| US1 (Add) | Foundational | US2, US6 |
| US2 (View) | Foundational | US1, US6 |
| US6 (Menu) | Foundational, US1, US2 | - |
| US3 (Complete) | US1 (need tasks to complete) | US4, US5 |
| US4 (Update) | US1 (need tasks to update) | US3, US5 |
| US5 (Delete) | US1 (need tasks to delete) | US3, US4 |

### Within Each User Story

1. Command implementation before tests (tests verify behavior)
2. Export to `__init__.py` after command complete
3. All tests for a story can run in parallel

---

## Parallel Execution Examples

### Foundational Phase Parallelization

```bash
# Launch all UI utilities in parallel:
Task T018: "Create Console singleton in src/ui.py"
Task T019: "Implement display_success() function in src/ui.py"
Task T020: "Implement display_error() function in src/ui.py"
Task T021: "Implement display_info() function in src/ui.py"

# Launch all test files in parallel:
Task T024: "Create pytest fixtures in tests/conftest.py"
Task T025: "Write Task model validation tests in tests/test_models.py"
```

### MVP Phase Parallelization (P1 Stories)

```bash
# After Foundational, launch MVP stories in parallel:
Task T027-T033: User Story 1 (Add Task)
Task T034-T039: User Story 2 (View Tasks)
# US6 depends on US1, US2 being available for integration
```

### P2 Stories Parallelization

```bash
# US3 and US4 can run in parallel:
Task T047-T054: User Story 3 (Mark Complete)
Task T055-T064: User Story 4 (Update Task)
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational ✓
3. Complete Phase 3: US1 (Add Task) ✓
4. Complete Phase 4: US2 (View Tasks) ✓
5. Complete Phase 5: US6 (Menu/Exit) ✓
6. **STOP and VALIDATE**: Test MVP independently
7. Can demo: Add tasks, view list, exit

### Incremental Delivery

1. Setup + Foundational → Core infrastructure
2. Add US1 + US2 + US6 → MVP (can add and view tasks)
3. Add US3 → Can mark complete
4. Add US4 → Can update tasks
5. Add US5 → Can delete tasks
6. Polish → Documentation, coverage, quality

### Suggested MVP Scope

**MVP = US1 + US2 + US6 (Phases 1-5)**

This delivers:
- Add Task functionality
- View Task List functionality
- Menu navigation and exit
- ~35 tasks total for MVP

---

## Task Summary

| Phase | Description | Task Count | Parallelizable |
|-------|-------------|------------|----------------|
| Phase 1 | Setup | 6 | 4 |
| Phase 2 | Foundational | 20 | 8 |
| Phase 3 | US1 - Add Task | 7 | 2 |
| Phase 4 | US2 - View Tasks | 6 | 2 |
| Phase 5 | US6 - Menu/Exit | 7 | 2 |
| Phase 6 | US3 - Complete | 8 | 3 |
| Phase 7 | US4 - Update | 10 | 4 |
| Phase 8 | US5 - Delete | 6 | 2 |
| Phase 9 | Polish | 7 | 4 |
| **TOTAL** | | **77** | **31** |

### Tasks Per User Story

| User Story | Priority | Task Count |
|------------|----------|------------|
| US1 - Add Task | P1 | 7 |
| US2 - View Tasks | P1 | 6 |
| US6 - Menu/Exit | P1 | 7 |
| US3 - Complete | P2 | 8 |
| US4 - Update | P2 | 10 |
| US5 - Delete | P3 | 6 |

---

## Notes

- All tasks follow the strict checklist format with IDs and file paths
- [P] marks tasks that can run in parallel (different files)
- [US#] maps task to specific user story for traceability
- Tests are included per NFR-006 and SC-010 requirements
- Each checkpoint validates story independence
- Commit after each task or logical group
- 80% coverage target applies to final Phase 9

---

**Tasks Status**: COMPLETE
**Total Tasks**: 77
**Ready for**: `/sp.implement` command
