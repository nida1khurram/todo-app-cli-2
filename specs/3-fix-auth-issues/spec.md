# Feature Specification: Fix Authentication & API Issues

**Feature Branch**: `3-fix-auth-issues`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Fix authentication issues in the todo webapp"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration Works (Priority: P1)

As a new user, I want to register an account with email and password so that I can access the todo application.

**Why this priority**: Registration is the entry point for all users. Without working registration, no users can use the application.

**Independent Test**: Can be tested by navigating to registration page, entering valid credentials, and verifying account is created without errors.

**Acceptance Scenarios**:

1. **Given** the user is on the registration page, **When** they enter a valid email and password meeting requirements, **Then** the account is created and user is redirected to the tasks dashboard.
2. **Given** the user is on the registration page, **When** they enter an email that is already registered, **Then** they see an error message indicating the email is taken.
3. **Given** the user is on the registration page, **When** they enter a password that does not meet requirements, **Then** they see validation errors for the password.

---

### User Story 2 - User Login Works (Priority: P1)

As a registered user, I want to log in with my email and password so that I can access my tasks.

**Why this priority**: Login is required for returning users to access their data. Without working login, existing users cannot use the application.

**Independent Test**: Can be tested by entering valid credentials on the login page and verifying successful authentication.

**Acceptance Scenarios**:

1. **Given** the user has a registered account, **When** they enter correct email and password, **Then** they are logged in and redirected to the tasks page.
2. **Given** the user enters incorrect password, **When** they attempt to login, **Then** they see an error message and remain on the login page.
3. **Given** the user enters an unregistered email, **When** they attempt to login, **Then** they see an error message.

---

### User Story 3 - Task Creation Works (Priority: P1)

As an authenticated user, I want to create new tasks so that I can track my todo items.

**Why this priority**: Task creation is the core functionality of the application. All protected API endpoints (tasks, tags) are returning 401 errors, preventing any task management.

**Independent Test**: Can be tested by logging in, clicking "Add Task", filling the form, and verifying the task appears in the task list without 401 errors.

**Acceptance Scenarios**:

1. **Given** the user is logged in and on the tasks page, **When** they create a new task with a title, **Then** the task is saved and appears in the task list.
2. **Given** the user is logged in, **When** they create a task with optional description and priority, **Then** those details are saved with the task.
3. **Given** the user is logged in, **When** they create a task with tags, **Then** the tags are associated with the task.
4. **Given** the user is not logged in, **When** they attempt to create a task, **Then** they are redirected to the login page.

---

### User Story 4 - Protected Routes Are Secured (Priority: P2)

As a user, I want protected pages to redirect me to login when I'm not authenticated so that my data remains secure.

**Why this priority**: Without route protection, unauthorized users could potentially access authenticated pages. Middleware provides security at the edge level.

**Independent Test**: Can be tested by accessing `/tasks` without being logged in and verifying redirection to login.

**Acceptance Scenarios**:

1. **Given** the user is not logged in, **When** they navigate directly to `/tasks`, **Then** they are redirected to `/login`.
2. **Given** the user is logged in, **When** they navigate to `/login`, **Then** they are redirected to `/tasks`.
3. **Given** the user is not logged in, **When** they navigate to `/profile`, **Then** they are redirected to `/login`.

---

### User Story 5 - Consistent Token Storage (Priority: P3)

As a developer, I want authentication tokens to use consistent storage keys so that the authentication system works reliably.

**Why this priority**: Different parts of the code use different localStorage keys for tokens, causing authentication to fail unpredictably.

**Independent Test**: Can be tested by checking that all authentication-related code uses the same token key, and login/logout work consistently.

**Acceptance Scenarios**:

1. **Given** the application code, **When** any component reads the auth token, **Then** they all use the same localStorage key.
2. **Given** the user logs in, **When** the token is stored, **Then** it is stored with a consistent key that all components recognize.

---

### Edge Cases

- What happens when the JWT token expires while the user is active?
- How does the system handle network errors during authentication?
- What happens when the database is unavailable during registration?
- How does the system handle concurrent login attempts from different devices?
- What happens when CORS blocks requests from the frontend?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email and password.
- **FR-002**: System MUST validate password strength (minimum 8 characters, uppercase, lowercase, digit).
- **FR-003**: System MUST allow users to log in with registered credentials.
- **FR-004**: System MUST create a user session upon successful login.
- **FR-005**: System MUST return 401 for unauthenticated requests to protected endpoints.
- **FR-006**: System MUST allow authenticated users to create tasks via the API.
- **FR-007**: System MUST redirect unauthenticated users to login when accessing protected pages.
- **FR-008**: System MUST use consistent localStorage keys for authentication tokens.
- **FR-009**: System MUST handle CORS to allow frontend requests to backend.
- **FR-010**: System MUST use Better Auth for authentication (replacing custom JWT auth).

### Key Entities

- **User**: Represents a registered user with email, password hash, and timestamps.
- **Session**: Represents an authenticated session with token and expiration.
- **Task**: Represents a todo item owned by a user with title, description, priority, and tags.

### Assumptions

- Better Auth will use its own database schema (separate from FastAPI models) in the same Neon PostgreSQL database.
- JWT tokens will expire after 7 days (industry standard).
- Social auth (OAuth) is not required for this phase.
- FastAPI backend will continue to handle task CRUD operations.
- Frontend and backend will remain on different ports (localhost:3000 and localhost:8000).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully register and login on the first attempt with valid credentials.
- **SC-002**: Task creation API returns 201 Created instead of 401 Unauthorized for authenticated users.
- **SC-003**: All protected API endpoints (tasks, tags) return appropriate responses instead of 401 errors.
- **SC-004**: Authenticated users can perform task CRUD operations without authentication errors.
- **SC-005**: Unauthenticated users are redirected to login within 500ms of accessing protected routes.
- **SC-006**: No token key inconsistencies exist in the codebase (single localStorage key used).

## Technical Notes

This specification addresses critical authentication and API issues that prevent the todo webapp from functioning. The primary issues are:

1. Better Auth is installed but not configured - app uses incomplete custom auth.
2. All protected endpoints return 401 due to JWT token validation failures.
3. Inconsistent token storage keys cause unpredictable auth behavior.
4. Missing middleware for route protection at the edge.

## Out of Scope

- Social authentication (Google, GitHub OAuth)
- Email verification flow
- Password reset functionality
- Two-factor authentication
- Moving task APIs from FastAPI to Next.js

## Dependencies

- Better Auth package (already installed in frontend)
- Neon PostgreSQL database (already configured)
- FastAPI backend (already implemented)
- Next.js frontend (already implemented)
