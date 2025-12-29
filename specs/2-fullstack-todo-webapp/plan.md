# Implementation Plan: Full-Stack Todo Web Application (Phase II)

**Branch**: `2-fullstack-todo-webapp` | **Date**: 2025-12-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/2-fullstack-todo-webapp/spec.md`

---

## Summary

Transform Phase I console todo app into a full-stack web application with multi-user authentication, priority system, tagging, search, filters, and sorting capabilities.

**Technical Approach**:
- **Frontend**: Next.js 15 with App Router, React 19 Server/Client Components, Tailwind CSS, Better Auth
- **Backend**: FastAPI with async endpoints, SQLModel ORM, JWT verification via python-jose
- **Database**: Neon Serverless PostgreSQL with asyncpg driver
- **Architecture**: Separate frontend/ and backend/ directories with independent deployment
- **Security**: Multi-layer defense with user isolation at database query level

---

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5 with Next.js 15, React 19
- Backend: Python 3.13+ with FastAPI 0.115

**Primary Dependencies**:
- Frontend: Next.js, React, Tailwind CSS, Better Auth, Zod
- Backend: FastAPI, SQLModel, Pydantic, python-jose, Passlib, Uvicorn, asyncpg

**Storage**: PostgreSQL 16 (Neon Serverless) with SQLModel ORM

**Testing**:
- Frontend: Jest, React Testing Library
- Backend: pytest, pytest-asyncio, pytest-cov

**Target Platform**: Web (browsers: Chrome, Firefox, Safari, Edge latest 2 versions)

**Project Type**: Web application (frontend + backend monorepo)

**Performance Goals**:
- Task list loads in <2 seconds for 500 tasks
- Search results in <1 second
- Filter/sort changes in <500ms
- Support 10 concurrent users without degradation

**Constraints**:
- Free-tier services only (Neon, Vercel, Railway/Render)
- No offline mode (internet required)
- Maximum 500 tasks per user (MVP limit)
- Session duration: 7 days

**Scale/Scope**:
- MVP: 10-50 concurrent users
- Database: 10,000 tasks across all users
- 4 database tables (User, Task, Tag, TaskTag)
- 15 API endpoints
- 10 frontend pages/components

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Development
- [x] Specification created before planning (`spec.md`)
- [x] All requirements traced to user stories
- [x] Research completed before implementation decisions (`research.md`)
- [x] Data model documented (`data-model.md`)
- [x] API contracts defined (`contracts/openapi.yaml`)

### ✅ AI-Native Architecture
- [x] Claude Code used for all specification and planning
- [x] Context7 MCP configured for documentation access
- [x] Better Auth for modern authentication patterns
- [x] Conversational API design (RESTful with clear semantics)

### ✅ Cloud-Native Design
- [x] Stateless API design (JWT tokens, no server sessions)
- [x] Containerization ready (separate frontend/backend)
- [x] Horizontal scalability (connection pooling, stateless endpoints)
- [x] Cloud deployment targets (Vercel, Railway/Render, Neon)

### ✅ Zero-Cost Development
- [x] All services have free tiers:
  - Neon PostgreSQL: Free tier (3 GB storage, always-on)
  - Vercel: Free tier (100 GB bandwidth)
  - Railway: Free tier (500 hours/month) or Render free tier
  - Better Auth: Open source, free
- [x] No paid API keys required
- [x] Open-source tools (FastAPI, Next.js, PostgreSQL)

### ✅ Test-First Quality
- [x] TDD approach planned in quickstart guide
- [x] pytest for backend, Jest for frontend
- [x] Integration tests for API endpoints planned
- [x] E2E tests for critical flows planned
- [x] Target: 80%+ code coverage

### Constitution Status: **PASSED**

No violations. All core principles adhered to.

---

## Project Structure

### Documentation (this feature)

```text
specs/2-fullstack-todo-webapp/
├── spec.md              # Feature specification (/sp.specify output)
├── plan.md              # This file (/sp.plan output)
├── research.md          # Technology decisions (Phase 0)
├── data-model.md        # Database schema (Phase 1)
├── quickstart.md        # Setup guide (Phase 1)
├── contracts/           # API contracts (Phase 1)
│   └── openapi.yaml     # OpenAPI 3.1 specification
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Implementation tasks (/sp.tasks - NOT created yet)
```

### Source Code (repository root)

```text
todo-fullstack-webapp/
│
├── frontend/                      # Next.js 15 Application
│   ├── src/
│   │   ├── app/                   # App Router (Next.js 15)
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx
│   │   │   │   └── tasks/
│   │   │   │       ├── page.tsx         # Server Component
│   │   │   │       ├── task-list.tsx    # Client Component
│   │   │   │       ├── task-form.tsx    # Client Component
│   │   │   │       └── filters.tsx      # Client Component
│   │   │   ├── api/
│   │   │   │   └── auth/[...auth]/route.ts  # Better Auth routes
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/                      # Reusable UI components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── input.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   └── badge.tsx
│   │   │   └── task/                    # Task-specific components
│   │   │       ├── priority-badge.tsx
│   │   │       ├── tag-list.tsx
│   │   │       └── task-card.tsx
│   │   ├── lib/
│   │   │   ├── api-client.ts            # Axios/fetch wrapper with JWT
│   │   │   ├── auth.ts                  # Better Auth config
│   │   │   └── utils.ts                 # Helper functions
│   │   └── types/
│   │       ├── task.ts                  # Task type definitions
│   │       ├── user.ts                  # User type definitions
│   │       └── api.ts                   # API response types
│   ├── public/
│   ├── tests/
│   │   ├── components/                  # Component tests
│   │   ├── integration/                 # Integration tests
│   │   └── e2e/                         # End-to-end tests
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   └── .env.local                       # Frontend environment variables
│
├── backend/                       # FastAPI Application
│   ├── src/
│   │   ├── models/                      # SQLModel database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User model
│   │   │   ├── task.py              # Task model
│   │   │   ├── tag.py               # Tag model
│   │   │   └── task_tag.py          # TaskTag junction model
│   │   ├── schemas/                     # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # UserCreate, UserResponse
│   │   │   ├── task.py              # TaskCreate, TaskUpdate, TaskResponse
│   │   │   └── tag.py               # TagCreate, TagResponse
│   │   ├── routes/                      # API endpoint routers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py              # /api/auth/* endpoints
│   │   │   ├── tasks.py             # /api/tasks/* endpoints
│   │   │   └── tags.py              # /api/tags/* endpoints
│   │   ├── auth/                        # Authentication utilities
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py               # JWT creation/verification
│   │   │   ├── password.py          # Password hashing (passlib)
│   │   │   └── dependencies.py      # FastAPI dependencies (get_current_user)
│   │   ├── database.py                  # Database connection & session management
│   │   ├── config.py                    # Configuration (environment variables)
│   │   └── main.py                      # FastAPI app entry point & CORS
│   ├── tests/
│   │   ├── conftest.py                  # pytest fixtures
│   │   ├── test_models.py               # Model tests
│   │   ├── test_auth.py                 # Authentication tests
│   │   ├── test_tasks_api.py            # Task endpoint tests
│   │   ├── test_tags_api.py             # Tag endpoint tests
│   │   └── test_user_isolation.py       # Security tests
│   ├── alembic/                         # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── pyproject.toml                   # UV dependencies
│   ├── alembic.ini                      # Alembic configuration
│   └── .env                             # Backend environment variables
│
├── specs/                          # Feature specifications (SDD)
│   ├── 1-cli-todo-app/             # Phase I specs
│   └── 2-fullstack-todo-webapp/    # Phase II specs (this feature)
│
├── .specify/                       # Spec-Kit Plus templates
├── history/                        # Prompt History Records
├── .context7.json                  # Context7 library configuration
├── .env.example                    # Environment template
├── .gitignore
├── CLAUDE.md                       # Claude Code instructions
├── CONTEXT7_SETUP.md               # Context7 setup guide
├── CONTEXT7_QUICK_REFERENCE.md     # Context7 usage guide
├── CONTEXT7_LIBRARIES_LOADED.md    # Loaded libraries documentation
└── README.md                       # Project overview
```

**Structure Decision**:

Selected **Option 2: Web application** structure with separate `frontend/` and `backend/` directories.

**Rationale**:
1. Clear separation between Next.js (Node.js) and FastAPI (Python) ecosystems
2. Independent deployment: Vercel for frontend, Railway/Render for backend
3. Different package managers: npm/pnpm for frontend, UV for backend
4. Easier to manage dependencies and configurations
5. Better CI/CD: separate build pipelines for each service

---

## Complexity Tracking

> **No violations to justify. Constitution check passed.**

---

## Phase 0: Research (Completed)

**Output**: `research.md`

**Decisions Made**:
1. ✅ Monorepo structure (separate frontend/backend directories)
2. ✅ Authentication architecture (Better Auth → JWT → python-jose)
3. ✅ Database schema (4 tables with many-to-many relationships)
4. ✅ API endpoint organization (RESTful by resource)
5. ✅ Frontend component strategy (mixed Server/Client components)
6. ✅ Database connection & async operations (asyncpg with connection pooling)
7. ✅ Security & user isolation (multi-layer defense)
8. ✅ Development environment setup
9. ✅ Deployment strategy (Vercel + Railway/Render + Neon)

**No unresolved NEEDS CLARIFICATION markers.**

---

## Phase 1: Design & Contracts (Completed)

**Outputs**:
- `data-model.md` - Complete database schema with SQLModel models
- `contracts/openapi.yaml` - OpenAPI 3.1 specification with all endpoints
- `quickstart.md` - Developer setup guide

**Design Artifacts**:
1. ✅ **4 Entity Models**: User, Task, Tag, TaskTag (junction table)
2. ✅ **11 Indexes**: Optimized for common queries
3. ✅ **15 API Endpoints**: Authentication (3), Tasks (8), Tags (4)
4. ✅ **Query Parameters**: Filtering, sorting, search, pagination
5. ✅ **Security Patterns**: JWT verification, user isolation, input validation
6. ✅ **Migration Strategy**: Alembic for schema evolution
7. ✅ **Development Workflow**: Setup steps, common commands, troubleshooting

**Agent Context Updated**:
- CLAUDE.md updated with Phase II technology stack
- Context7 libraries loaded (14 libraries)

---

## Phase 2: Tasks Generation (Next Step)

**Command**: `/sp.tasks`

**Expected Output**: `tasks.md` with implementation tasks organized by:
1. Project setup (directories, dependencies, configuration)
2. Backend implementation (models, routes, auth, database)
3. Frontend implementation (pages, components, API client, auth)
4. Testing (unit, integration, E2E)
5. Deployment (Vercel, Railway/Render, Neon)

**Estimated Tasks**: 30-40 tasks across 5 categories

---

## Re-evaluation: Constitution Check (Post-Design)

### ✅ Spec-Driven Development
- [x] All Phase 1 artifacts created (`data-model.md`, `contracts/`, `quickstart.md`)
- [x] No implementation details in specification
- [x] Technology decisions documented with rationale

### ✅ AI-Native Architecture
- [x] Context7 configured with all 14 libraries
- [x] Better Auth chosen for modern auth patterns
- [x] API designed for clarity and discoverability

### ✅ Cloud-Native Design
- [x] Stateless API (no server-side sessions)
- [x] Connection pooling configured
- [x] Horizontal scalability possible

### ✅ Zero-Cost Development
- [x] All services remain free-tier compatible
- [x] No new paid dependencies introduced

### ✅ Test-First Quality
- [x] Test structure planned in quickstart
- [x] pytest and Jest configurations ready
- [x] TDD approach documented

### Post-Design Status: **PASSED**

All gates remain green. Ready for `/sp.tasks` command.

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Free tier limits exceeded | High | Low | Monitor usage, implement pagination, add caching |
| JWT secret compromise | Critical | Very Low | Use strong secrets, rotate periodically, env vars only |
| N+1 query performance | Medium | Medium | Eager load relationships, add indexes, use select_related |
| Better Auth complexity | Medium | Low | Follow official docs, use Context7 for up-to-date examples |
| CORS issues | Low | Medium | Configure CORS properly, test cross-origin requests early |
| Neon serverless cold starts | Low | Medium | Use pool_pre_ping, accept slight delay on first request |

---

## Success Criteria Mapping

| Success Criterion | Implementation Approach |
|-------------------|------------------------|
| SC-001: Account creation <60s | Better Auth streamlined flow, optimized API |
| SC-002: Task creation <15s | Simple form, optimistic UI updates |
| SC-003: List loads <2s for 500 tasks | Indexes on all filter fields, pagination |
| SC-004: Search <1s | PostgreSQL ILIKE with indexed columns |
| SC-005: Filter/sort <500ms | Client-side filtering when possible, indexed queries |
| SC-006: 10 concurrent users | Connection pooling (15 connections), async operations |
| SC-007: Feedback <3s | Loading states, toast notifications, error messages |
| SC-008: 100% validation errors | Pydantic validation, Zod on frontend |
| SC-009: 100% success feedback | Success toasts, visual confirmations |
| SC-010: Learn CRUD in 10 min | Intuitive UI, clear labels, simple workflow |
| SC-011: Zero unauthorized access | User isolation at query level, JWT verification |
| SC-012: Latest browsers supported | Modern web standards, no legacy polyfills |
| SC-013: Mobile responsive (375px+) | Tailwind responsive classes, mobile-first design |
| SC-014: Keyboard accessible | Semantic HTML, focus management, ARIA labels |

---

## Next Steps

1. **Run `/sp.tasks`** to generate detailed implementation tasks
2. **Review tasks.md** for completeness and ordering
3. **Begin implementation** following TDD approach
4. **Use Context7** during implementation: `use context7 for <library>`
5. **Commit frequently** with descriptive messages
6. **Deploy incrementally** (frontend first, then backend, then integration)

---

## Planning Complete

**Status**: ✅ Phase 0 and Phase 1 complete
**Ready**: ✅ For `/sp.tasks` command
**Documentation**: ✅ All artifacts generated
**Constitution**: ✅ All gates passed

**Branch**: `2-fullstack-todo-webapp`
**Next Command**: `/sp.tasks`
