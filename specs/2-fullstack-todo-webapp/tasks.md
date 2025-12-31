# Tasks: Full-Stack Todo Web Application (Phase II)

**Input**: Design documents from `/specs/2-fullstack-todo-webapp/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Organization**: Tasks grouped by user story for independent implementation and testing

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, etc.)
- File paths included for all tasks

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [x] T001 Create frontend/ directory with Next.js 15 + TypeScript + Tailwind CSS
- [x] T002 Create backend/ directory with FastAPI + UV package manager
- [x] T003 [P] Copy .env.example template to repository root
- [x] T004 [P] Create frontend/.gitignore for Next.js artifacts
- [x] T005 [P] Create backend/.gitignore for Python artifacts
- [x] T006 Update root README.md with Phase II monorepo structure and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before ANY user story implementation

**⚠️ CRITICAL**: Complete this phase before starting user story work

### Backend Foundation

- [x] T007 Create backend/src/config.py with environment variable loading (DATABASE_URL, JWT_SECRET, CORS_ORIGINS)
- [x] T008 Create backend/src/database.py with async engine, session factory, and get_session dependency
- [x] T009 Create backend/src/main.py with FastAPI app initialization and CORS middleware
- [x] T010 [P] Initialize Alembic in backend/alembic/ for database migrations
- [x] T011 [P] Create backend/pyproject.toml with dependencies (fastapi, sqlmodel, uvicorn, asyncpg, python-jose, passlib, alembic, pydantic)
- [x] T012 Create backend/src/models/__init__.py to export all models
- [x] T013 Create backend/src/schemas/__init__.py to export all schemas
- [x] T014 Create backend/src/routes/__init__.py to organize routers

### Frontend Foundation

- [x] T015 [P] Initialize Next.js 15 project in frontend/ with App Router and TypeScript
- [x] T016 [P] Install and configure Tailwind CSS in frontend/
- [x] T017 [P] Create frontend/package.json with dependencies (next, react, better-auth, zod, axios)
- [x] T018 [P] Create frontend/tsconfig.json with strict TypeScript configuration
- [x] T019 Create frontend/src/lib/api-client.ts with axios instance and JWT token injection
- [x] T020 Create frontend/src/types/api.ts with common API response types

### Test Infrastructure Setup

- [x] T021 [P] Create backend/tests/conftest.py with pytest fixtures for async database session and test client
- [x] T022 [P] Create backend/tests/__init__.py to organize test modules
- [x] T023 [P] Install pytest, pytest-asyncio, httpx in backend/pyproject.toml dev dependencies
- [x] T024 [P] Create frontend/jest.config.js with Next.js and TypeScript support
- [x] T025 [P] Create frontend/__tests__/setup.ts with React Testing Library configuration
- [x] T026 [P] Install Jest, React Testing Library, @testing-library/user-event in frontend/package.json dev dependencies

**Checkpoint**: Foundation complete - user stories can now be implemented independently

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and sign in with email/password

**Independent Test**: Create account → sign out → sign in → verify session persists across refreshes

### Testing Setup (US1) - TDD: Write Tests FIRST

- [x] T027 [P] [US1] Create backend/tests/test_models_user.py with User model validation tests
- [x] T028 [P] [US1] Create backend/tests/test_auth_password.py with password hashing and verification tests
- [x] T029 [P] [US1] Create backend/tests/test_auth_jwt.py with JWT token creation and validation tests
- [x] T030 [P] [US1] Create backend/tests/test_routes_auth.py with POST /api/auth/register endpoint tests (success, duplicate email, invalid email)
- [x] T031 [US1] Add tests for POST /api/auth/login endpoint (success, wrong password, user not found) to backend/tests/test_routes_auth.py
- [x] T032 [US1] Add tests for GET /api/auth/me endpoint (authenticated, unauthorized) to backend/tests/test_routes_auth.py
- [x] T033 [P] [US1] Create frontend/__tests__/components/ui/button.test.tsx with button component tests
- [x] T034 [P] [US1] Create frontend/__tests__/components/ui/input.test.tsx with input validation state tests
- [x] T035 [US1] Create frontend/__tests__/app/auth/register.test.tsx with registration form submission and validation tests
- [x] T036 [US1] Create frontend/__tests__/app/auth/login.test.tsx with login form submission and error handling tests
- [x] T037 [US1] Run all US1 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US1)

- [x] T038 [P] [US1] Create User model in backend/src/models/user.py with id, email, password_hash, created_at fields
- [x] T039 [P] [US1] Create UserCreate schema in backend/src/schemas/user.py with email and password validation
- [x] T040 [P] [US1] Create UserResponse schema in backend/src/schemas/user.py (exclude password_hash)
- [x] T041 [P] [US1] Create backend/src/auth/password.py with hash_password and verify_password using passlib bcrypt
- [x] T042 [P] [US1] Create backend/src/auth/jwt.py with create_access_token and decode_token functions using python-jose
- [x] T043 [US1] Create backend/src/auth/dependencies.py with get_current_user dependency for JWT verification
- [x] T044 [US1] Create Alembic migration for users table in backend/alembic/versions/001_create_users_table.py
- [x] T045 [US1] Implement POST /api/auth/register endpoint in backend/src/routes/auth.py
- [x] T046 [US1] Implement POST /api/auth/login endpoint in backend/src/routes/auth.py
- [x] T047 [US1] Implement GET /api/auth/me endpoint in backend/src/routes/auth.py
- [x] T048 [US1] Register auth router in backend/src/main.py

### Frontend Implementation (US1)

- [x] T049 [P] [US1] Create frontend/src/lib/auth.ts with Better Auth configuration
- [x] T050 [P] [US1] Create frontend/src/app/api/auth/[...auth]/route.ts for Better Auth API routes
- [x] T051 [P] [US1] Create frontend/src/types/user.ts with User and AuthResponse types
- [x] T052 [US1] Create frontend/src/app/(auth)/register/page.tsx with registration form
- [x] T053 [US1] Create frontend/src/app/(auth)/login/page.tsx with login form
- [x] T054 [US1] Create frontend/src/components/ui/button.tsx reusable button component with Tailwind styles
- [x] T055 [US1] Create frontend/src/components/ui/input.tsx reusable input component with validation states
- [x] T056 [US1] Add sign-out button in frontend/src/app/(dashboard)/layout.tsx
- [x] T057 [US1] Implement auth state management and protected route logic

### Verify Tests Pass (US1) - Green Phase

- [ ] T058 [US1] Run all backend tests for US1 and verify they PASS (pytest backend/tests/test_*auth*.py)
- [ ] T059 [US1] Run all frontend tests for US1 and verify they PASS (npm test -- auth)
- [ ] T060 [US1] Verify 80%+ code coverage for US1 backend code (pytest --cov)
- [ ] T061 [US1] Verify 80%+ code coverage for US1 frontend components (npm test -- --coverage)

**Checkpoint US1**: Users can register, login, and logout. Session persists across refreshes.

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks and view their task list

**Independent Test**: Sign in → create task with title/description → verify appears in list → refresh → verify persists

### Testing Setup (US2) - TDD: Write Tests FIRST

- [x] T062 [P] [US2] Create backend/tests/test_models_task.py with Task model validation tests (title length, required fields)
- [x] T063 [P] [US2] Create backend/tests/test_routes_tasks_get.py with GET /api/tasks endpoint tests (user isolation, empty list, multiple tasks)
- [x] T064 [P] [US2] Create backend/tests/test_routes_tasks_post.py with POST /api/tasks endpoint tests (success, missing title, unauthorized)
- [x] T065 [P] [US2] Create frontend/__tests__/components/task/task-card.test.tsx with task display tests
- [x] T066 [P] [US2] Create frontend/__tests__/components/task/task-form.test.tsx with form validation and submission tests
- [x] T067 [US2] Create frontend/__tests__/components/task/task-list.test.tsx with task list rendering tests
- [x] T068 [US2] Run all US2 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US2)

- [x] T069 [P] [US2] Create Task model in backend/src/models/task.py with id, user_id, title, description, is_completed, priority, created_at, updated_at
- [x] T070 [P] [US2] Create TaskCreate schema in backend/src/schemas/task.py with title, description, priority validation
- [x] T071 [P] [US2] Create TaskResponse schema in backend/src/schemas/task.py with all task fields
- [x] T072 [US2] Create Alembic migration for tasks table in backend/alembic/versions/002_create_tasks_table.py
- [x] T073 [US2] Implement GET /api/tasks endpoint in backend/src/routes/tasks.py with user_id filtering
- [x] T074 [US2] Implement POST /api/tasks endpoint in backend/src/routes/tasks.py with authentication
- [x] T075 [US2] Register tasks router in backend/src/main.py

### Frontend Implementation (US2)

- [x] T076 [P] [US2] Create frontend/src/types/task.ts with Task, TaskCreate, TaskResponse types
- [x] T077 [P] [US2] Create frontend/src/app/(dashboard)/tasks/page.tsx Server Component with data fetching
- [x] T078 [P] [US2] Create frontend/src/components/task/task-card.tsx for displaying individual tasks
- [x] T079 [US2] Create frontend/src/app/(dashboard)/tasks/task-form.tsx Client Component for task creation form
- [x] T080 [US2] Create frontend/src/app/(dashboard)/tasks/task-list.tsx Client Component for task list display
- [x] T081 [US2] Create frontend/src/components/ui/card.tsx reusable card component with Tailwind styles
- [x] T082 [US2] Add API client methods for createTask and getTasks in frontend/src/lib/api-client.ts

### Verify Tests Pass (US2) - Green Phase

- [ ] T083 [US2] Run all backend tests for US2 and verify they PASS (pytest backend/tests/test_*task*.py)
- [ ] T084 [US2] Run all frontend tests for US2 and verify they PASS (npm test -- task)
- [ ] T085 [US2] Verify 80%+ code coverage for US2 backend code
- [ ] T086 [US2] Verify 80%+ code coverage for US2 frontend components

**Checkpoint US2**: Users can create tasks and view their own task list. Other users' tasks are not visible.

---

## Phase 5: User Story 10 - User Isolation and Data Security (Priority: P1) 🎯 MVP

**Goal**: Ensure complete data privacy - users can only access their own tasks

**Independent Test**: Create tasks as User A → sign in as User B → verify User A's tasks not visible → attempt direct API access with User A's task ID → verify 403 error

### Testing (US10) - TDD: Write Tests FIRST

- [x] T087 [P] [US10] Create backend/tests/test_user_isolation.py to verify cross-user access prevention
- [x] T088 [US10] Test unauthorized access returns 401 when no token provided in backend/tests/test_user_isolation.py
- [x] T089 [US10] Test forbidden access returns 403 when accessing other user's tasks in backend/tests/test_user_isolation.py
- [x] T090 [US10] Run all US10 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US10)

- [x] T091 [P] [US10] Add user_id filter to GET /api/tasks query in backend/src/routes/tasks.py
- [x] T092 [P] [US10] Add get_task_or_404 dependency to verify task ownership in backend/src/routes/tasks.py
- [x] T093 [US10] Add 403 Forbidden error handling for unauthorized access attempts
- [x] T094 [US10] Implement user isolation validation in all task endpoints (GET, PUT, PATCH, DELETE)

### Verify Tests Pass (US10) - Green Phase

- [ ] T095 [US10] Run all backend tests for US10 and verify they PASS (pytest backend/tests/test_user_isolation.py)
- [ ] T096 [US10] Verify 80%+ code coverage for security code

**Checkpoint US10**: Complete data isolation verified. Users cannot access each other's data.

---

## Phase 6: User Story 3 - Update and Delete Tasks (Priority: P2)

**Goal**: Users can edit task details and remove tasks

**Independent Test**: Create task → edit title/description → verify changes saved → delete task → verify removed from list

### Testing Setup (US3) - TDD: Write Tests FIRST

- [x] T097 [P] [US3] Create backend/tests/test_routes_tasks_put.py with PUT /api/tasks/{task_id} tests (success, not found, unauthorized)
- [x] T098 [P] [US3] Create backend/tests/test_routes_tasks_delete.py with DELETE /api/tasks/{task_id} tests (success, not found, unauthorized)
- [x] T099 [P] [US3] Create frontend/__tests__/components/task/edit-task-form.test.tsx with edit form tests
- [x] T100 [P] [US3] Create frontend/__tests__/components/task/delete-modal.test.tsx with deletion confirmation tests
- [x] T101 [US3] Run all US3 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US3)

- [x] T102 [P] [US3] Create TaskUpdate schema in backend/src/schemas/task.py with optional fields
- [x] T103 [P] [US3] Implement PUT /api/tasks/{task_id} endpoint in backend/src/routes/tasks.py
- [x] T104 [P] [US3] Implement DELETE /api/tasks/{task_id} endpoint in backend/src/routes/tasks.py
- [x] T105 [US3] Add updated_at timestamp update logic on PUT endpoint

### Frontend Implementation (US3)

- [x] T106 [P] [US3] Create frontend/src/app/(dashboard)/tasks/edit-task-form.tsx Client Component for editing
- [x] T107 [P] [US3] Add delete confirmation modal in frontend/src/components/task/delete-modal.tsx
- [x] T108 [US3] Add updateTask and deleteTask methods to frontend/src/lib/api-client.ts
- [x] T109 [US3] Add edit and delete buttons to task-card.tsx component
- [x] T110 [US3] Implement optimistic UI updates for edit and delete operations

### Verify Tests Pass (US3) - Green Phase

- [ ] T111 [US3] Run all backend tests for US3 and verify they PASS
- [ ] T112 [US3] Run all frontend tests for US3 and verify they PASS
- [ ] T113 [US3] Verify 80%+ code coverage for US3 code

**Checkpoint US3**: Users can fully update and delete their tasks with confirmation dialogs.

---

## Phase 7: User Story 4 - Mark Tasks as Complete (Priority: P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Create task → mark complete → verify visual change → unmark → verify returns to pending

### Testing Setup (US4) - TDD: Write Tests FIRST

- [x] T114 [P] [US4] Create backend/tests/test_routes_tasks_patch.py with PATCH /api/tasks/{task_id} tests (toggle completion, unauthorized)
- [x] T115 [P] [US4] Create frontend/__tests__/components/task/completion-checkbox.test.tsx with checkbox toggle tests
- [x] T116 [US4] Run all US4 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US4)

- [x] T117 [P] [US4] Implement PATCH /api/tasks/{task_id} endpoint for partial updates in backend/src/routes/tasks.py
- [x] T118 [US4] Add toggle completion logic (update is_completed and updated_at fields)

### Frontend Implementation (US4)

- [x] T119 [P] [US4] Add completion checkbox to task-card.tsx component
- [x] T120 [US4] Add toggleComplete method to frontend/src/lib/api-client.ts
- [x] T121 [US4] Add visual distinction for completed tasks (strikethrough, opacity, etc.) in task-card.tsx
- [x] T122 [US4] Implement optimistic UI update for instant feedback

### Verify Tests Pass (US4) - Green Phase

- [ ] T123 [US4] Run all backend tests for US4 and verify they PASS
- [ ] T124 [US4] Run all frontend tests for US4 and verify they PASS
- [ ] T125 [US4] Verify 80%+ code coverage for US4 code

**Checkpoint US4**: Users can mark tasks complete/incomplete with immediate visual feedback.

---

## Phase 8: User Story 5 - Prioritize Tasks with Colored Badges (Priority: P3)

**Goal**: Users can assign and view priority levels with colored indicators

**Independent Test**: Create tasks with different priorities → verify red/yellow/green badges appear correctly

### Testing Setup (US5) - TDD: Write Tests FIRST

- [x] T126 [P] [US5] Create backend/tests/test_priority_validation.py with priority enum validation tests
- [x] T127 [P] [US5] Create frontend/__tests__/components/task/priority-badge.test.tsx with badge color rendering tests
- [x] T128 [US5] Run all US5 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US5)

- [x] T129 [US5] Add priority field validation to TaskCreate and TaskUpdate schemas (enum: high, medium, low)
- [x] T130 [US5] Add priority default value (medium) in Task model if not already present

### Frontend Implementation (US5)

- [x] T131 [P] [US5] Create frontend/src/components/task/priority-badge.tsx with colored badges (red/yellow/green)
- [x] T132 [P] [US5] Create frontend/src/components/ui/badge.tsx reusable badge component
- [x] T133 [US5] Add priority dropdown to task-form.tsx and edit-task-form.tsx
- [x] T134 [US5] Add priority-badge component to task-card.tsx display

### Verify Tests Pass (US5) - Green Phase

- [ ] T135 [US5] Run all backend tests for US5 and verify they PASS
- [ ] T136 [US5] Run all frontend tests for US5 and verify they PASS
- [ ] T137 [US5] Verify 80%+ code coverage for US5 code

**Checkpoint US5**: Priority system fully functional with visual color coding.

---

## Phase 9: User Story 6 - Organize Tasks with Tags (Priority: P3)

**Goal**: Users can create tags and assign multiple tags to tasks

**Independent Test**: Create tags → assign to tasks → verify display → test autocomplete

### Testing Setup (US6) - TDD: Write Tests FIRST

- [x] T138 [P] [US6] Create backend/tests/test_models_tag.py with Tag model validation tests
- [x] T139 [P] [US6] Create backend/tests/test_models_task_tag.py with TaskTag junction model tests
- [x] T140 [P] [US6] Create backend/tests/test_routes_tags.py with tag CRUD endpoint tests
- [x] T141 [P] [US6] Create backend/tests/test_task_tag_relationships.py with many-to-many relationship tests
- [x] T142 [P] [US6] Create frontend/__tests__/components/task/tag-input.test.tsx with autocomplete tests
- [x] T143 [P] [US6] Create frontend/__tests__/components/task/tag-list.test.tsx with tag display tests
- [x] T144 [US6] Add tests for tag assignment on task creation/update to backend/tests/test_routes_tasks.py
- [x] T145 [US6] Run all US6 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US6)

- [x] T146 [P] [US6] Create Tag model in backend/src/models/tag.py with id, user_id, name, created_at
- [x] T147 [P] [US6] Create TaskTag junction model in backend/src/models/task_tag.py with task_id, tag_id, created_at
- [x] T148 [P] [US6] Create TagCreate schema in backend/src/schemas/tag.py
- [x] T149 [P] [US6] Create TagResponse schema in backend/src/schemas/tag.py
- [x] T150 [US6] Create Alembic migration for tags and task_tags tables in backend/alembic/versions/003_create_tags_tables.py
- [x] T151 [US6] Implement GET /api/tags endpoint with optional search parameter in backend/src/routes/tags.py
- [x] T152 [US6] Implement POST /api/tags endpoint in backend/src/routes/tags.py
- [x] T153 [US6] Implement DELETE /api/tags/{tag_id} endpoint in backend/src/routes/tags.py
- [x] T154 [US6] Add tags field to TaskResponse schema (list of tag names)
- [x] T155 [US6] Modify POST /api/tasks to accept tags array and create task_tag associations
- [x] T156 [US6] Modify PUT /api/tasks to update tag associations
- [x] T157 [US6] Register tags router in backend/src/main.py

### Frontend Implementation (US6)

- [x] T158 [P] [US6] Create frontend/src/types/tag.ts with Tag type definitions
- [x] T159 [P] [US6] Create frontend/src/components/task/tag-list.tsx for displaying tags on tasks
- [x] T160 [P] [US6] Create frontend/src/components/task/tag-input.tsx Client Component with autocomplete
- [x] T161 [US6] Add tag input to task-form.tsx and edit-task-form.tsx
- [x] T162 [US6] Add getTags, createTag, and deleteTag methods to frontend/src/lib/api-client.ts
- [x] T163 [US6] Implement tag autocomplete API call with debouncing in tag-input.tsx
- [x] T164 [US6] Add tag-list component to task-card.tsx display

### Verify Tests Pass (US6) - Green Phase

- [ ] T165 [US6] Run all backend tests for US6 and verify they PASS
- [ ] T166 [US6] Run all frontend tests for US6 and verify they PASS
- [ ] T167 [US6] Verify 80%+ code coverage for US6 code

**Checkpoint US6**: Full tagging system with autocomplete working end-to-end.

---

## Phase 10: User Story 7 - Search Tasks by Keyword (Priority: P3)

**Goal**: Users can search tasks by keyword in title or description

**Independent Test**: Create tasks with distinctive keywords → search → verify only matching tasks shown → clear search → verify all tasks shown

### Testing Setup (US7) - TDD: Write Tests FIRST

- [x] T168 [P] [US7] Create backend/tests/test_routes_tasks_search.py with search query tests (ILIKE, empty results, case insensitive)
- [x] T169 [P] [US7] Create frontend/__tests__/components/task/search-bar.test.tsx with search input and debounce tests
- [x] T170 [US7] Run all US7 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US7)

- [x] T171 [US7] Add search query parameter to GET /api/tasks endpoint in backend/src/routes/tasks.py
- [x] T172 [US7] Implement ILIKE query for title and description search in GET /api/tasks logic

### Frontend Implementation (US7)

- [x] T173 [P] [US7] Create frontend/src/components/task/search-bar.tsx Client Component with input field
- [x] T174 [US7] Add search state management to task-list.tsx with debounced API calls
- [x] T175 [US7] Add search-bar component to tasks page layout
- [x] T176 [US7] Add empty state message when search returns no results

### Verify Tests Pass (US7) - Green Phase

- [ ] T177 [US7] Run all backend tests for US7 and verify they PASS
- [ ] T178 [US7] Run all frontend tests for US7 and verify they PASS
- [ ] T179 [US7] Verify 80%+ code coverage for US7 code

**Checkpoint US7**: Search functionality works with instant feedback and empty states.

---

## Phase 11: User Story 8 - Filter Tasks by Status, Priority, and Tags (Priority: P3)

**Goal**: Users can filter tasks by status, priority, and tags with multi-select

**Independent Test**: Create diverse tasks → apply status filter → apply priority filter → apply tag filter → combine filters → verify all work together

### Testing Setup (US8) - TDD: Write Tests FIRST

- [x] T180 [P] [US8] Create backend/tests/test_routes_tasks_filter.py with filter combination tests (status, priority, tags, AND logic)
- [x] T181 [P] [US8] Create frontend/__tests__/components/task/filters.test.tsx with filter UI tests
- [x] T182 [US8] Add tests for combined filters with edge cases to backend/tests/test_routes_tasks_filter.py
- [x] T183 [US8] Run all US8 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US8)

- [x] T184 [US8] Add status query parameter to GET /api/tasks (all/completed/pending) in backend/src/routes/tasks.py
- [x] T185 [US8] Add priority query parameter to GET /api/tasks in backend/src/routes/tasks.py
- [x] T186 [US8] Add tags query parameter (comma-separated) to GET /api/tasks in backend/src/routes/tasks.py
- [x] T187 [US8] Implement combined filter logic with AND conditions in GET /api/tasks query builder

### Frontend Implementation (US8)

- [x] T188 [P] [US8] Create frontend/src/app/(dashboard)/tasks/filters.tsx Client Component with filter controls
- [x] T189 [US8] Add status filter dropdown (all/completed/pending) to filters.tsx
- [x] T190 [US8] Add priority filter dropdown (any/high/medium/low) to filters.tsx
- [x] T191 [US8] Add tag multi-select filter to filters.tsx
- [x] T192 [US8] Add "Clear All Filters" button to filters.tsx
- [x] T193 [US8] Implement filter state management in task-list.tsx
- [x] T194 [US8] Update API calls to include filter parameters from state

### Verify Tests Pass (US8) - Green Phase

- [ ] T195 [US8] Run all backend tests for US8 and verify they PASS
- [ ] T196 [US8] Run all frontend tests for US8 and verify they PASS
- [ ] T197 [US8] Verify 80%+ code coverage for US8 code

**Checkpoint US8**: All filters working independently and in combination with AND logic.

---

## Phase 12: User Story 9 - Sort Tasks by Different Criteria (Priority: P4)

**Goal**: Users can sort tasks by created date, priority, or title with asc/desc toggle

**Independent Test**: Create multiple tasks → sort by date → toggle direction → sort by priority → sort by title → verify all work correctly

### Testing Setup (US9) - TDD: Write Tests FIRST

- [x] T198 [P] [US9] Create backend/tests/test_routes_tasks_sort.py with sort query tests (created_at, priority, title, asc/desc)
- [x] T199 [P] [US9] Create frontend/__tests__/components/task/sort-dropdown.test.tsx with sort control tests
- [x] T200 [US9] Run all US9 tests to verify they FAIL before implementation (Red phase of TDD)

### Backend Implementation (US9)

- [x] T201 [US9] Add sort_by query parameter to GET /api/tasks (created_at/priority/title) in backend/src/routes/tasks.py
- [x] T202 [US9] Add sort_order query parameter to GET /api/tasks (asc/desc) in backend/src/routes/tasks.py
- [x] T203 [US9] Implement dynamic ORDER BY clause based on sort parameters

### Frontend Implementation (US9)

- [x] T204 [P] [US9] Add sort dropdown to filters.tsx with sort_by options
- [x] T205 [US9] Add asc/desc toggle button to filters.tsx
- [x] T206 [US9] Update API calls to include sort parameters from state
- [x] T207 [US9] Add visual indicator for current sort field and direction

### Verify Tests Pass (US9) - Green Phase

- [ ] T208 [US9] Run all backend tests for US9 and verify they PASS
- [ ] T209 [US9] Run all frontend tests for US9 and verify they PASS
- [ ] T210 [US9] Verify 80%+ code coverage for US9 code

**Checkpoint US9**: Sorting works for all criteria with proper direction toggling.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, loading states, error handling, accessibility

### E2E Testing (Critical User Journeys)

- [x] T211 [P] Create frontend/__tests__/e2e/complete-user-journey.test.tsx with full workflow (register → login → create → edit → delete → logout)
- [x] T212 [P] Create frontend/__tests__/e2e/search-and-filter.test.tsx with search and filtering end-to-end tests
- [x] T213 [P] Create frontend/__tests__/e2e/tag-workflow.test.tsx with tag creation and assignment flow tests
- [ ] T214 Run all E2E tests and verify they PASS
- [ ] T215 Verify overall project code coverage is 80%+ (backend and frontend combined)

### UI/UX Polish

- [x] T216 [P] Add loading spinners for async operations in task-list.tsx
- [x] T217 [P] Add success toast notifications using frontend/src/lib/toast.ts
- [x] T218 [P] Add error toast notifications for failed API calls
- [x] T219 [P] Add empty state message when user has no tasks in task-list.tsx
- [x] T220 [P] Implement keyboard navigation for all interactive elements
- [x] T221 [P] Add ARIA labels for screen reader accessibility

### Responsive Design

- [ ] T222 [P] Test mobile layout on 375px width viewport
- [x] T223 [P] Add responsive Tailwind classes to all components
- [ ] T224 [P] Test tablet layout on 768px width viewport

### Error Handling

- [x] T225 [P] Add global error boundary in frontend/src/app/error.tsx
- [x] T226 [P] Add validation error display in all forms
- [x] T227 [P] Add network error retry logic in api-client.ts

### Environment & Deployment

- [x] T228 [P] Create .env.example with all required variables and descriptions
- [x] T229 [P] Create deployment guide in specs/2-fullstack-todo-webapp/deployment.md
- [x] T230 Configure Vercel deployment for frontend/ directory
- [x] T231 Configure Railway or Render deployment for backend/ directory

---

## Dependencies & Execution Order

### User Story Completion Order

```
MVP (Required for basic functionality):
  Phase 3: US1 (Authentication) ← Must complete first
  Phase 4: US2 (Create/View Tasks) ← Requires US1
  Phase 5: US10 (User Isolation) ← Requires US1 & US2

Extended Features (Independent after MVP):
  Phase 6: US3 (Update/Delete) ← Requires US2
  Phase 7: US4 (Mark Complete) ← Requires US2
  Phase 8: US5 (Priority System) ← Requires US2
  Phase 9: US6 (Tagging) ← Requires US2
  Phase 10: US7 (Search) ← Requires US2
  Phase 11: US8 (Filtering) ← Requires US2, US5, US6
  Phase 12: US9 (Sorting) ← Requires US2

Polish:
  Phase 13: Cross-cutting ← Requires all user stories complete
```

### Parallel Execution Opportunities

**Within MVP (Phase 3-5)**:
- Tasks marked [P] within same user story can run in parallel
- US10 security tasks can run in parallel with US2 frontend work

**Extended Features (Phase 6-12)**:
- After MVP complete, ALL user stories US3-US9 can be implemented in parallel
- Each story is independent and has no cross-dependencies

**Example Parallel Workflow**:
```
Sprint 1 (MVP):
  Developer A: US1 Backend (T027-T048)
  Developer B: US1 Frontend (T049-T057)
  ↓
  Developer A: US2 Backend (T062-T075)
  Developer B: US2 Frontend (T076-T082)
  ↓
  Both: US10 Security (T087-T094)

Sprint 2 (Features):
  Developer A: US3 (Update/Delete) + US4 (Mark Complete)
  Developer B: US5 (Priority) + US6 (Tags)
  ↓
  Developer A: US7 (Search)
  Developer B: US8 (Filters) + US9 (Sort)

Sprint 3 (Polish):
  Both: Phase 13 (Cross-cutting concerns + E2E tests)
```

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Recommended MVP**: User Stories 1, 2, 10 only
- US1: Authentication (P1)
- US2: Create/View Tasks (P1)
- US10: User Isolation (P1)

**MVP Deliverable**: Secure multi-user todo app with basic CRUD

**Rationale**: Demonstrates core value, validates architecture, enables user testing

### Incremental Delivery

**Iteration 1 (MVP)**:
- Foundation (Phase 1-2)
- US1: Authentication
- US2: Create/View
- US10: Security
- Deploy to production

**Iteration 2 (Core Features)**:
- US3: Update/Delete
- US4: Mark Complete
- US5: Priority System
- Deploy update

**Iteration 3 (Advanced Features)**:
- US6: Tagging
- US7: Search
- US8: Filtering
- US9: Sorting
- Deploy update

**Iteration 4 (Polish)**:
- Phase 13: Cross-cutting
- E2E Tests
- Performance optimization
- Final deployment

---

## Task Summary

| Phase | User Story | Priority | Tasks | Test Tasks | Implementation Tasks | Can Parallelize |
|-------|------------|----------|-------|------------|----------------------|-----------------|
| Phase 1 | Setup | - | 6 tasks | 0 | 6 | Some (T004, T005) |
| Phase 2 | Foundation | - | 20 tasks | 6 | 14 | Many (T010-T026) |
| Phase 3 | US1: Auth | P1 | 35 tasks | 11 | 24 | Many (T027-T034, T038-T042, T049-T051, T054-T055) |
| Phase 4 | US2: Create/View | P1 | 25 tasks | 7 | 18 | Many (T062-T067, T069-T071, T076-T078, T081) |
| Phase 5 | US10: Security | P1 | 10 tasks | 4 | 6 | Some (T087-T089, T091-T092) |
| Phase 6 | US3: Update/Delete | P2 | 17 tasks | 5 | 12 | Many (T097-T100, T102-T104, T106-T107) |
| Phase 7 | US4: Mark Complete | P2 | 12 tasks | 3 | 9 | Some (T114-T115, T117, T119-T120) |
| Phase 8 | US5: Priority | P3 | 12 tasks | 3 | 9 | Many (T126-T127, T131-T132) |
| Phase 9 | US6: Tagging | P3 | 30 tasks | 8 | 22 | Many (T138-T145, T146-T149, T158-T160) |
| Phase 10 | US7: Search | P3 | 12 tasks | 3 | 9 | Some (T168-T169, T173) |
| Phase 11 | US8: Filtering | P3 | 18 tasks | 4 | 14 | Some (T180-T181, T188) |
| Phase 12 | US9: Sorting | P4 | 13 tasks | 3 | 10 | Some (T198-T199, T204) |
| Phase 13 | Polish & E2E | - | 21 tasks | 5 E2E | 16 | All parallel |
| **Total** | **10 Stories** | | **231 tasks** | **62 test tasks** | **169 impl tasks** | **~65% parallelizable** |

---

## Validation Checklist

- [x] All tasks follow format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [x] Each user story has independent test criteria
- [x] Task IDs are sequential (T001-T231)
- [x] All [P] tasks are truly parallelizable
- [x] All [Story] labels match user stories from spec.md
- [x] File paths are specific and complete
- [x] Dependencies clearly documented
- [x] MVP scope identified (US1, US2, US10)
- [x] Parallel execution examples provided
- [x] Each user story phase has checkpoint criteria
- [x] **TDD approach: Test tasks BEFORE implementation tasks**
- [x] **Test coverage requirements documented (80%+)**
- [x] **E2E tests for critical user journeys included**

**Format Validation**: ✅ PASSED - All 231 tasks follow strict checklist format with TDD approach

---

## Next Steps

1. **Review tasks.md** for completeness
2. **Run `/sp.implement`** to execute all tasks with Claude Code
3. **Or implement manually** following TDD approach (tests first, then implementation)
4. **Use Context7**: `use context7 for <library>` during implementation
5. **Commit frequently** after each user story checkpoint
6. **Deploy MVP** after Phase 3-5 complete

---

**Total Tasks**: 231 (increased from 141)
**Test Tasks**: 62 (new)
**MVP Tasks**: 71 (Phases 1-5)
**Extended Features**: 139 (Phases 6-12)
**Polish & E2E**: 21 (Phase 13)
**Parallel Opportunities**: ~150 tasks can run in parallel
**Code Coverage Target**: 80% minimum (per constitution)

Ready for TDD implementation! 🚀
