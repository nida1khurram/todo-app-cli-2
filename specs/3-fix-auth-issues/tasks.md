# Tasks: Fix Authentication & API Issues

**Input**: Design documents from `/specs/3-fix-auth-issues/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create environment variables template in backend/.env.example (BETTER_AUTH_SECRET, JWT_SECRET, CORS_ORIGINS)
- [ ] T002 Create environment variables template in frontend/.env.local.example (BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL)
- [ ] T003 [P] Verify backend dependencies in pyproject.toml (better-auth, pyjwt, python-jose)
- [ ] T004 [P] Verify frontend dependencies in package.json (@better-auth/jwt, better-auth)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Configure Better Auth with JWT plugin in frontend/src/lib/auth.ts (database adapter, emailAndPassword, jwt configuration)
- [ ] T006 Create Better Auth API route handler in frontend/src/app/api/auth/[...all]/route.ts (GET, POST handlers from toNextJsHandler)
- [ ] T007 Update backend JWT verification to accept string user_id in backend/src/auth/dependencies.py (remove int() conversion, accept string sub)
- [ ] T008 Verify CORS configuration in backend/src/main.py (allow_credentials=True, allow_origins includes localhost:3000)
- [ ] T009 Update Task model to use string better_auth_user_id in backend/src/models/task.py
- [ ] T010 [P] Update Tag model to use string better_auth_user_id in backend/src/models/tag.py
- [ ] T011 [P] Update TaskTag model in backend/src/models/task_tag.py
- [ ] T012 Update Task schemas with proper validation in backend/src/schemas/task.py (title, priority, tags)
- [ ] T013 Update frontend API client token key in frontend/src/lib/api-client.ts (use consistent key)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration Works (Priority: P1) 🎯 MVP

**Goal**: Users can register with email and password

**Independent Test**: Navigate to registration page, enter valid credentials, verify account created without errors

### Implementation for User Story 1

- [ ] T014 [US1] Update registration page to use Better Auth in frontend/src/app/(auth)/register/page.tsx (signUp.email API)
- [ ] T015 [US1] Create registration form component with email, password, confirm password fields in frontend/src/components/auth/register-form.tsx
- [ ] T016 [US1] Add password validation (8+ chars, uppercase, lowercase, digit) in register form
- [ ] T017 [US1] Handle registration success/error states with user-friendly messages
- [ ] T018 [US1] Redirect to tasks dashboard on successful registration

**Checkpoint**: User registration should work - test with new account creation

---

## Phase 4: User Story 2 - User Login Works (Priority: P1)

**Goal**: Users can log in with email and password

**Independent Test**: Enter valid credentials on login page, verify successful authentication and redirect

### Implementation for User Story 2

- [ ] T019 [US2] Update login page to use Better Auth in frontend/src/app/(auth)/login/page.tsx (signIn.email API)
- [ ] T020 [US2] Create login form component with email and password fields in frontend/src/components/auth/login-form.tsx
- [ ] T021 [US2] Handle login success/error states (invalid credentials message)
- [ ] T022 [US2] Redirect to tasks dashboard on successful login
- [ ] T023 [US2] Update dashboard layout to use Better Auth session in frontend/src/app/(dashboard)/layout.tsx (use auth.session instead of authApi.me)

**Checkpoint**: User login should work - test with registered account

---

## Phase 5: User Story 3 - Task Creation Works (Priority: P1)

**Goal**: Authenticated users can create tasks without 401 errors

**Independent Test**: Log in, click "Add Task", fill form, verify task appears in list

### Implementation for User Story 3

- [ ] T024 [US3] Update tasks API client to get token from Better Auth in frontend/src/lib/api-client.ts
- [ ] T025 [US3] Fix task creation endpoint in backend/src/routes/tasks.py (verify get_current_user_id returns string)
- [ ] T026 [US3] Add task list endpoint GET /api/tasks with user filtering
- [ ] T027 [US3] Add task creation endpoint POST /api/tasks with proper validation
- [ ] T028 [US3] Add task update endpoint PUT /api/tasks/{id}
- [ ] T029 [US3] Add task toggle completion endpoint PATCH /api/tasks/{id}
- [ ] T030 [US3] Add task delete endpoint DELETE /api/tasks/{id}
- [ ] T031 [US3] Update tasks page to use API client in frontend/src/app/(dashboard)/tasks/page.tsx

**Checkpoint**: Task creation and CRUD should work without 401 errors

---

## Phase 6: User Story 4 - Protected Routes Are Secured (Priority: P2)

**Goal**: Unauthenticated users are redirected to login when accessing protected routes

**Independent Test**: Access /tasks without login, verify redirect to /login within 500ms

### Implementation for User Story 4

- [ ] T032 [US4] Create Next.js middleware for route protection in frontend/middleware.ts
- [ ] T033 [US4] Define protected routes pattern in middleware (/tasks, /profile, etc.)
- [ ] T034 [US4] Define auth routes pattern in middleware (/login, /register)
- [ ] T035 [US4] Implement redirect to login for unauthenticated access to protected routes
- [ ] T036 [US4] Implement redirect to dashboard for authenticated access to auth routes

**Checkpoint**: Protected routes should redirect properly

---

## Phase 7: User Story 5 - Consistent Token Storage (Priority: P3)

**Goal**: All authentication code uses consistent token storage keys

**Independent Test**: Verify all auth-related code uses same localStorage/cookie key

### Implementation for User Story 5

- [ ] T037 [US5] Audit all frontend files for token storage usage (grep for localStorage.getItem/setItem)
- [ ] T038 [US5] Update any inconsistent token key usage to use BETTER_AUTH_SESSION_TOKEN
- [ ] T039 [US5] Remove custom JWT token creation/validation code (authApi.register, authApi.login) - use Better Auth only
- [ ] T040 [US5] Clean up unused auth imports and dependencies

**Checkpoint**: All token storage should be consistent

---

## Phase 8: Tag Management (Supporting)

**Goal**: Users can manage tags for tasks

**Independent Test**: Create tag, associate with task, verify tag appears in task

### Implementation for Tag Management

- [ ] T041 Add tag creation endpoint POST /api/tags in backend/src/routes/tags.py
- [ ] T042 Add tag list endpoint GET /api/tags in backend/src/routes/tags.py
- [ ] T043 Add tag delete endpoint DELETE /api/tags/{id} in backend/src/routes/tags.py
- [ ] T044 Update Task model to include tags relationship in backend/src/models/task.py

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Run full authentication flow test (register → login → create task → view tasks)
- [ ] T046 [P] Verify CORS headers allow Authorization header from frontend
- [ ] T047 Add error logging for authentication failures
- [ ] T048 Update frontend logout to use Better Auth signOut in frontend/src/app/(dashboard)/layout.tsx
- [ ] T049 [P] Run quickstart.md validation from specs/3-fix-auth-issues/quickstart.md
- [ ] T050 Create integration test for complete auth flow (register, login, create task, logout)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1, US2, US3 can proceed in parallel once foundation is ready
  - US4, US5 depend on US1, US2 being complete
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Registration)**: Can start after Foundational - No dependencies on other stories
- **US2 (Login)**: Can start after Foundational - No dependencies on other stories
- **US3 (Task Creation)**: Depends on US2 (login must work first)
- **US4 (Protected Routes)**: Depends on US1, US2 (auth must work)
- **US5 (Token Storage)**: Depends on US1, US2 (cleanup requires working auth)

### Within Each User Story

- Foundational tasks must complete before any story
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to dependent stories

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- Foundational tasks T005-T008 can run in parallel (no file conflicts)
- Foundational tasks T009-T013 can run in parallel
- Once Foundational is done, US1 and US2 can proceed in parallel
- US3 depends on US2 but can start once T019-T023 are done
- US4 depends on US1 and US2 but can start once T014-T023 are done

---

## Parallel Example: Foundational Phase

```bash
# These can run in parallel:
Task T005: Configure Better Auth with JWT plugin
Task T006: Create Better Auth API route handler
Task T007: Update JWT verification for string user_id
Task T008: Verify CORS configuration
```

---

## Implementation Strategy

### MVP First (User Story 1 + Foundational)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. **STOP and VALIDATE**: Test registration independently
5. Continue to User Story 2

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently
3. Add User Story 2 → Test independently (login)
4. Add User Story 3 → Test independently (task creation)
5. Add User Story 4 → Test (middleware)
6. Add User Story 5 → Cleanup

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 50 |
| **Setup Phase** | 4 tasks |
| **Foundational Phase** | 9 tasks |
| **User Story 1** | 5 tasks |
| **User Story 2** | 5 tasks |
| **User Story 3** | 8 tasks |
| **User Story 4** | 5 tasks |
| **User Story 5** | 4 tasks |
| **Tag Management** | 4 tasks |
| **Polish Phase** | 6 tasks |

### MVP Scope

**Minimum for MVP**: Phases 1-4 (Setup, Foundational, US1 Registration, US2 Login)

This delivers working registration and login with Better Auth.

### Next Steps After MVP

1. Add US3 (Task Creation) - Core functionality
2. Add US4 (Protected Routes) - Security
3. Add US5 (Token Cleanup) - Code quality
4. Add Tag Management - Feature completeness
5. Polish - Testing and validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
