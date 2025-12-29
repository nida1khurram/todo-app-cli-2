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

- [ ] T001 Create frontend/ directory with Next.js 15 + TypeScript + Tailwind CSS
- [ ] T002 Create backend/ directory with FastAPI + UV package manager
- [ ] T003 [P] Copy .env.example template to repository root
- [ ] T004 [P] Create frontend/.gitignore for Next.js artifacts
- [ ] T005 [P] Create backend/.gitignore for Python artifacts
- [ ] T006 Update root README.md with Phase II monorepo structure and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before ANY user story implementation

**⚠️ CRITICAL**: Complete this phase before starting user story work

### Backend Foundation

- [ ] T007 Create backend/src/config.py with environment variable loading (DATABASE_URL, JWT_SECRET, CORS_ORIGINS)
- [ ] T008 Create backend/src/database.py with async engine, session factory, and get_session dependency
- [ ] T009 Create backend/src/main.py with FastAPI app initialization and CORS middleware
- [ ] T010 [P] Initialize Alembic in backend/alembic/ for database migrations
- [ ] T011 [P] Create backend/pyproject.toml with dependencies (fastapi, sqlmodel, uvicorn, asyncpg, python-jose, passlib, alembic, pydantic)
- [ ] T012 Create backend/src/models/__init__.py to export all models
- [ ] T013 Create backend/src/schemas/__init__.py to export all schemas
- [ ] T014 Create backend/src/routes/__init__.py to organize routers

### Frontend Foundation

- [ ] T015 [P] Initialize Next.js 15 project in frontend/ with App Router and TypeScript
- [ ] T016 [P] Install and configure Tailwind CSS in frontend/
- [ ] T017 [P] Create frontend/package.json with dependencies (next, react, better-auth, zod, axios)
- [ ] T018 [P] Create frontend/tsconfig.json with strict TypeScript configuration
- [ ] T019 Create frontend/src/lib/api-client.ts with axios instance and JWT token injection
- [ ] T020 Create frontend/src/types/api.ts with common API response types

**Checkpoint**: Foundation complete - user stories can now be implemented independently

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and sign in with email/password

**Independent Test**: Create account → sign out → sign in → verify session persists across refreshes

### Backend Implementation (US1)

- [ ] T021 [P] [US1] Create User model in backend/src/models/user.py with id, email, password_hash, created_at fields
- [ ] T022 [P] [US1] Create UserCreate schema in backend/src/schemas/user.py with email and password validation
- [ ] T023 [P] [US1] Create UserResponse schema in backend/src/schemas/user.py (exclude password_hash)
- [ ] T024 [P] [US1] Create backend/src/auth/password.py with hash_password and verify_password using passlib bcrypt
- [ ] T025 [P] [US1] Create backend/src/auth/jwt.py with create_access_token and decode_token functions using python-jose
- [ ] T026 [US1] Create backend/src/auth/dependencies.py with get_current_user dependency for JWT verification
- [ ] T027 [US1] Create Alembic migration for users table in backend/alembic/versions/001_create_users_table.py
- [ ] T028 [US1] Implement POST /api/auth/register endpoint in backend/src/routes/auth.py
- [ ] T029 [US1] Implement POST /api/auth/login endpoint in backend/src/routes/auth.py
- [ ] T030 [US1] Implement GET /api/auth/me endpoint in backend/src/routes/auth.py
- [ ] T031 [US1] Register auth router in backend/src/main.py

### Frontend Implementation (US1)

- [ ] T032 [P] [US1] Create frontend/src/lib/auth.ts with Better Auth configuration
- [ ] T033 [P] [US1] Create frontend/src/app/api/auth/[...auth]/route.ts for Better Auth API routes
- [ ] T034 [P] [US1] Create frontend/src/types/user.ts with User and AuthResponse types
- [ ] T035 [US1] Create frontend/src/app/(auth)/register/page.tsx with registration form
- [ ] T036 [US1] Create frontend/src/app/(auth)/login/page.tsx with login form
- [ ] T037 [US1] Create frontend/src/components/ui/button.tsx reusable button component with Tailwind styles
- [ ] T038 [US1] Create frontend/src/components/ui/input.tsx reusable input component with validation states
- [ ] T039 [US1] Add sign-out button in frontend/src/app/(dashboard)/layout.tsx
- [ ] T040 [US1] Implement auth state management and protected route logic

**Checkpoint US1**: Users can register, login, and logout. Session persists across refreshes.

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can create new tasks and view their task list

**Independent Test**: Sign in → create task with title/description → verify appears in list → refresh → verify persists

### Backend Implementation (US2)

- [ ] T041 [P] [US2] Create Task model in backend/src/models/task.py with id, user_id, title, description, is_completed, priority, created_at, updated_at
- [ ] T042 [P] [US2] Create TaskCreate schema in backend/src/schemas/task.py with title, description, priority validation
- [ ] T043 [P] [US2] Create TaskResponse schema in backend/src/schemas/task.py with all task fields
- [ ] T044 [US2] Create Alembic migration for tasks table in backend/alembic/versions/002_create_tasks_table.py
- [ ] T045 [US2] Implement GET /api/tasks endpoint in backend/src/routes/tasks.py with user_id filtering
- [ ] T046 [US2] Implement POST /api/tasks endpoint in backend/src/routes/tasks.py with authentication
- [ ] T047 [US2] Register tasks router in backend/src/main.py

### Frontend Implementation (US2)

- [ ] T048 [P] [US2] Create frontend/src/types/task.ts with Task, TaskCreate, TaskResponse types
- [ ] T049 [P] [US2] Create frontend/src/app/(dashboard)/tasks/page.tsx Server Component with data fetching
- [ ] T050 [P] [US2] Create frontend/src/components/task/task-card.tsx for displaying individual tasks
- [ ] T051 [US2] Create frontend/src/app/(dashboard)/tasks/task-form.tsx Client Component for task creation form
- [ ] T052 [US2] Create frontend/src/app/(dashboard)/tasks/task-list.tsx Client Component for task list display
- [ ] T053 [US2] Create frontend/src/components/ui/card.tsx reusable card component with Tailwind styles
- [ ] T054 [US2] Add API client methods for createTask and getTasks in frontend/src/lib/api-client.ts

**Checkpoint US2**: Users can create tasks and view their own task list. Other users' tasks are not visible.

---

## Phase 5: User Story 10 - User Isolation and Data Security (Priority: P1) 🎯 MVP

**Goal**: Ensure complete data privacy - users can only access their own tasks

**Independent Test**: Create tasks as User A → sign in as User B → verify User A's tasks not visible → attempt direct API access with User A's task ID → verify 403 error

### Backend Implementation (US10)

- [ ] T055 [P] [US10] Add user_id filter to GET /api/tasks query in backend/src/routes/tasks.py
- [ ] T056 [P] [US10] Add get_task_or_404 dependency to verify task ownership in backend/src/routes/tasks.py
- [ ] T057 [US10] Add 403 Forbidden error handling for unauthorized access attempts
- [ ] T058 [US10] Implement user isolation validation in all task endpoints (GET, PUT, PATCH, DELETE)

### Testing (US10)

- [ ] T059 [P] [US10] Create backend/tests/test_user_isolation.py to verify cross-user access prevention
- [ ] T060 [US10] Test unauthorized access returns 401 when no token provided
- [ ] T061 [US10] Test forbidden access returns 403 when accessing other user's tasks

**Checkpoint US10**: Complete data isolation verified. Users cannot access each other's data.

---

## Phase 6: User Story 3 - Update and Delete Tasks (Priority: P2)

**Goal**: Users can edit task details and remove tasks

**Independent Test**: Create task → edit title/description → verify changes saved → delete task → verify removed from list

### Backend Implementation (US3)

- [ ] T062 [P] [US3] Create TaskUpdate schema in backend/src/schemas/task.py with optional fields
- [ ] T063 [P] [US3] Implement PUT /api/tasks/{task_id} endpoint in backend/src/routes/tasks.py
- [ ] T064 [P] [US3] Implement DELETE /api/tasks/{task_id} endpoint in backend/src/routes/tasks.py
- [ ] T065 [US3] Add updated_at timestamp update logic on PUT endpoint

### Frontend Implementation (US3)

- [ ] T066 [P] [US3] Create frontend/src/app/(dashboard)/tasks/edit-task-form.tsx Client Component for editing
- [ ] T067 [P] [US3] Add delete confirmation modal in frontend/src/components/task/delete-modal.tsx
- [ ] T068 [US3] Add updateTask and deleteTask methods to frontend/src/lib/api-client.ts
- [ ] T069 [US3] Add edit and delete buttons to task-card.tsx component
- [ ] T070 [US3] Implement optimistic UI updates for edit and delete operations

**Checkpoint US3**: Users can fully update and delete their tasks with confirmation dialogs.

---

## Phase 7: User Story 4 - Mark Tasks as Complete (Priority: P2)

**Goal**: Users can toggle task completion status

**Independent Test**: Create task → mark complete → verify visual change → unmark → verify returns to pending

### Backend Implementation (US4)

- [ ] T071 [P] [US4] Implement PATCH /api/tasks/{task_id} endpoint for partial updates in backend/src/routes/tasks.py
- [ ] T072 [US4] Add toggle completion logic (update is_completed and updated_at fields)

### Frontend Implementation (US4)

- [ ] T073 [P] [US4] Add completion checkbox to task-card.tsx component
- [ ] T074 [US4] Add toggleComplete method to frontend/src/lib/api-client.ts
- [ ] T075 [US4] Add visual distinction for completed tasks (strikethrough, opacity, etc.) in task-card.tsx
- [ ] T076 [US4] Implement optimistic UI update for instant feedback

**Checkpoint US4**: Users can mark tasks complete/incomplete with immediate visual feedback.

---

## Phase 8: User Story 5 - Prioritize Tasks with Colored Badges (Priority: P3)

**Goal**: Users can assign and view priority levels with colored indicators

**Independent Test**: Create tasks with different priorities → verify red/yellow/green badges appear correctly

### Backend Implementation (US5)

- [ ] T077 [US5] Add priority field validation to TaskCreate and TaskUpdate schemas (enum: high, medium, low)
- [ ] T078 [US5] Add priority default value (medium) in Task model if not already present

### Frontend Implementation (US5)

- [ ] T079 [P] [US5] Create frontend/src/components/task/priority-badge.tsx with colored badges (red/yellow/green)
- [ ] T080 [P] [US5] Create frontend/src/components/ui/badge.tsx reusable badge component
- [ ] T081 [US5] Add priority dropdown to task-form.tsx and edit-task-form.tsx
- [ ] T082 [US5] Add priority-badge component to task-card.tsx display

**Checkpoint US5**: Priority system fully functional with visual color coding.

---

## Phase 9: User Story 6 - Organize Tasks with Tags (Priority: P3)

**Goal**: Users can create tags and assign multiple tags to tasks

**Independent Test**: Create tags → assign to tasks → verify display → test autocomplete

### Backend Implementation (US6)

- [ ] T083 [P] [US6] Create Tag model in backend/src/models/tag.py with id, user_id, name, created_at
- [ ] T084 [P] [US6] Create TaskTag junction model in backend/src/models/task_tag.py with task_id, tag_id, created_at
- [ ] T085 [P] [US6] Create TagCreate schema in backend/src/schemas/tag.py
- [ ] T086 [P] [US6] Create TagResponse schema in backend/src/schemas/tag.py
- [ ] T087 [US6] Create Alembic migration for tags and task_tags tables in backend/alembic/versions/003_create_tags_tables.py
- [ ] T088 [US6] Implement GET /api/tags endpoint with optional search parameter in backend/src/routes/tags.py
- [ ] T089 [US6] Implement POST /api/tags endpoint in backend/src/routes/tags.py
- [ ] T090 [US6] Implement DELETE /api/tags/{tag_id} endpoint in backend/src/routes/tags.py
- [ ] T091 [US6] Add tags field to TaskResponse schema (list of tag names)
- [ ] T092 [US6] Modify POST /api/tasks to accept tags array and create task_tag associations
- [ ] T093 [US6] Modify PUT /api/tasks to update tag associations
- [ ] T094 [US6] Register tags router in backend/src/main.py

### Frontend Implementation (US6)

- [ ] T095 [P] [US6] Create frontend/src/types/tag.ts with Tag type definitions
- [ ] T096 [P] [US6] Create frontend/src/components/task/tag-list.tsx for displaying tags on tasks
- [ ] T097 [P] [US6] Create frontend/src/components/task/tag-input.tsx Client Component with autocomplete
- [ ] T098 [US6] Add tag input to task-form.tsx and edit-task-form.tsx
- [ ] T099 [US6] Add getTags, createTag, and deleteTag methods to frontend/src/lib/api-client.ts
- [ ] T100 [US6] Implement tag autocomplete API call with debouncing in tag-input.tsx
- [ ] T101 [US6] Add tag-list component to task-card.tsx display

**Checkpoint US6**: Full tagging system with autocomplete working end-to-end.

---

## Phase 10: User Story 7 - Search Tasks by Keyword (Priority: P3)

**Goal**: Users can search tasks by keyword in title or description

**Independent Test**: Create tasks with distinctive keywords → search → verify only matching tasks shown → clear search → verify all tasks shown

### Backend Implementation (US7)

- [ ] T102 [US7] Add search query parameter to GET /api/tasks endpoint in backend/src/routes/tasks.py
- [ ] T103 [US7] Implement ILIKE query for title and description search in GET /api/tasks logic

### Frontend Implementation (US7)

- [ ] T104 [P] [US7] Create frontend/src/components/task/search-bar.tsx Client Component with input field
- [ ] T105 [US7] Add search state management to task-list.tsx with debounced API calls
- [ ] T106 [US7] Add search-bar component to tasks page layout
- [ ] T107 [US7] Add empty state message when search returns no results

**Checkpoint US7**: Search functionality works with instant feedback and empty states.

---

## Phase 11: User Story 8 - Filter Tasks by Status, Priority, and Tags (Priority: P3)

**Goal**: Users can filter tasks by status, priority, and tags with multi-select

**Independent Test**: Create diverse tasks → apply status filter → apply priority filter → apply tag filter → combine filters → verify all work together

### Backend Implementation (US8)

- [ ] T108 [US8] Add status query parameter to GET /api/tasks (all/completed/pending) in backend/src/routes/tasks.py
- [ ] T109 [US8] Add priority query parameter to GET /api/tasks in backend/src/routes/tasks.py
- [ ] T110 [US8] Add tags query parameter (comma-separated) to GET /api/tasks in backend/src/routes/tasks.py
- [ ] T111 [US8] Implement combined filter logic with AND conditions in GET /api/tasks query builder

### Frontend Implementation (US8)

- [ ] T112 [P] [US8] Create frontend/src/app/(dashboard)/tasks/filters.tsx Client Component with filter controls
- [ ] T113 [US8] Add status filter dropdown (all/completed/pending) to filters.tsx
- [ ] T114 [US8] Add priority filter dropdown (any/high/medium/low) to filters.tsx
- [ ] T115 [US8] Add tag multi-select filter to filters.tsx
- [ ] T116 [US8] Add "Clear All Filters" button to filters.tsx
- [ ] T117 [US8] Implement filter state management in task-list.tsx
- [ ] T118 [US8] Update API calls to include filter parameters from state

**Checkpoint US8**: All filters working independently and in combination with AND logic.

---

## Phase 12: User Story 9 - Sort Tasks by Different Criteria (Priority: P4)

**Goal**: Users can sort tasks by created date, priority, or title with asc/desc toggle

**Independent Test**: Create multiple tasks → sort by date → toggle direction → sort by priority → sort by title → verify all work correctly

### Backend Implementation (US9)

- [ ] T119 [US9] Add sort_by query parameter to GET /api/tasks (created_at/priority/title) in backend/src/routes/tasks.py
- [ ] T120 [US9] Add sort_order query parameter to GET /api/tasks (asc/desc) in backend/src/routes/tasks.py
- [ ] T121 [US9] Implement dynamic ORDER BY clause based on sort parameters

### Frontend Implementation (US9)

- [ ] T122 [P] [US9] Add sort dropdown to filters.tsx with sort_by options
- [ ] T123 [US9] Add asc/desc toggle button to filters.tsx
- [ ] T124 [US9] Update API calls to include sort parameters from state
- [ ] T125 [US9] Add visual indicator for current sort field and direction

**Checkpoint US9**: Sorting works for all criteria with proper direction toggling.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, loading states, error handling, accessibility

### UI/UX Polish

- [ ] T126 [P] Add loading spinners for async operations in task-list.tsx
- [ ] T127 [P] Add success toast notifications using frontend/src/lib/toast.ts
- [ ] T128 [P] Add error toast notifications for failed API calls
- [ ] T129 [P] Add empty state message when user has no tasks in task-list.tsx
- [ ] T130 [P] Implement keyboard navigation for all interactive elements
- [ ] T131 [P] Add ARIA labels for screen reader accessibility

### Responsive Design

- [ ] T132 [P] Test mobile layout on 375px width viewport
- [ ] T133 [P] Add responsive Tailwind classes to all components
- [ ] T134 [P] Test tablet layout on 768px width viewport

### Error Handling

- [ ] T135 [P] Add global error boundary in frontend/src/app/error.tsx
- [ ] T136 [P] Add validation error display in all forms
- [ ] T137 [P] Add network error retry logic in api-client.ts

### Environment & Deployment

- [ ] T138 Create .env.example with all required variables and descriptions
- [ ] T139 Create deployment guide in specs/2-fullstack-todo-webapp/deployment.md
- [ ] T140 Configure Vercel deployment for frontend/ directory
- [ ] T141 Configure Railway or Render deployment for backend/ directory

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
  Developer A: US1 Backend (T021-T031)
  Developer B: US1 Frontend (T032-T040)
  ↓
  Developer A: US2 Backend (T041-T047)
  Developer B: US2 Frontend (T048-T054)
  ↓
  Both: US10 Security (T055-T061)

Sprint 2 (Features):
  Developer A: US3 (Update/Delete) + US4 (Mark Complete)
  Developer B: US5 (Priority) + US6 (Tags)
  ↓
  Developer A: US7 (Search)
  Developer B: US8 (Filters) + US9 (Sort)

Sprint 3 (Polish):
  Both: Phase 13 (Cross-cutting concerns)
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
- Performance optimization
- Final deployment

---

## Task Summary

| Phase | User Story | Priority | Tasks | Can Parallelize |
|-------|------------|----------|-------|-----------------|
| Phase 1 | Setup | - | 6 tasks | Some (T004, T005) |
| Phase 2 | Foundation | - | 14 tasks | Many (T010-T020) |
| Phase 3 | US1: Auth | P1 | 20 tasks | Many (T021-T025, T032-T034, T037-T038) |
| Phase 4 | US2: Create/View | P1 | 14 tasks | Many (T041-T043, T048-T050, T053) |
| Phase 5 | US10: Security | P1 | 7 tasks | Some (T055-T056, T059) |
| Phase 6 | US3: Update/Delete | P2 | 9 tasks | Many (T062-T064, T066-T067) |
| Phase 7 | US4: Mark Complete | P2 | 6 tasks | Some (T071, T073-T074) |
| Phase 8 | US5: Priority | P3 | 6 tasks | Many (T079-T080) |
| Phase 9 | US6: Tagging | P3 | 19 tasks | Many (T083-T086, T095-T097) |
| Phase 10 | US7: Search | P3 | 6 tasks | Some (T104) |
| Phase 11 | US8: Filtering | P3 | 11 tasks | Some (T112) |
| Phase 12 | US9: Sorting | P4 | 7 tasks | Some (T122) |
| Phase 13 | Polish | - | 16 tasks | All parallel |
| **Total** | **10 Stories** | | **141 tasks** | **~60% parallelizable** |

---

## Validation Checklist

- [x] All tasks follow format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [x] Each user story has independent test criteria
- [x] Task IDs are sequential (T001-T141)
- [x] All [P] tasks are truly parallelizable
- [x] All [Story] labels match user stories from spec.md
- [x] File paths are specific and complete
- [x] Dependencies clearly documented
- [x] MVP scope identified (US1, US2, US10)
- [x] Parallel execution examples provided
- [x] Each user story phase has checkpoint criteria

**Format Validation**: ✅ PASSED - All 141 tasks follow strict checklist format

---

## Next Steps

1. **Review tasks.md** for completeness
2. **Run `/sp.implement`** to execute all tasks with Claude Code
3. **Or implement manually** following TDD approach (tests first, then implementation)
4. **Use Context7**: `use context7 for <library>` during implementation
5. **Commit frequently** after each user story checkpoint
6. **Deploy MVP** after Phase 3-5 complete

---

**Total Tasks**: 141
**MVP Tasks**: 57 (Phases 1-5)
**Extended Features**: 68 (Phases 6-12)
**Polish**: 16 (Phase 13)
**Parallel Opportunities**: ~85 tasks can run in parallel

Ready for implementation! 🚀
