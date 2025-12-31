# Implementation Plan: Fix Authentication & API Issues

**Branch**: `3-fix-auth-issues` | **Date**: 2025-12-30 | **Spec**: [specs/3-fix-auth-issues/spec.md](../spec.md)
**Input**: Feature specification from `/specs/3-fix-auth-issues/spec.md`

## Summary

Fix critical authentication and API issues in the full-stack todo webapp. The primary problems are: Better Auth is installed but not configured (app uses incomplete custom JWT auth), all protected endpoints return 401 Unauthorized due to JWT token validation failures, inconsistent token storage keys cause unpredictable auth behavior, and missing middleware for route protection. The solution involves fully configuring Better Auth with proper database adapter, ensuring JWT token consistency between frontend and backend, adding Next.js middleware for route protection, and verifying CORS configuration.

## Technical Context

**Language/Version**: Python 3.13+ (FastAPI), TypeScript 5.x (Next.js 16+)
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, JWT, Neon PostgreSQL, Next.js App Router
**Storage**: Neon Serverless PostgreSQL (async SQLModel)
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web browser (Chrome, Firefox, Safari)
**Project Type**: Web application (FastAPI backend + Next.js frontend)
**Performance Goals**: API response <500ms p95, frontend LCP <2.5s
**Constraints**: Must use Better Auth for authentication, JWT token expiry 7 days, user data isolation required
**Scale/Scope**: Single-user to multi-user (start with basic auth, expand to multi-user)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Spec-Driven Development
- [x] Feature specification exists at `specs/3-fix-auth-issues/spec.md`
- [x] User stories defined with priorities (P1-P3)
- [x] Functional requirements listed (FR-001 to FR-010)
- [x] Success criteria measurable and technology-agnostic

### Gate 2: Technology Stack Compliance (Phase II)
- [x] Frontend: Next.js 16+ (App Router) - CONFIRMED
- [x] Backend: Python FastAPI - CONFIRMED
- [x] ORM: SQLModel - CONFIRMED
- [x] Database: Neon Serverless PostgreSQL - CONFIRMED
- [x] Authentication: Better Auth - CONFIRMED (needs proper config)
- [x] JWT: PyJWT / Better Auth JWT Plugin - CONFIRMED

### Gate 3: Security Requirements
- [x] User Isolation - REQUIRED (backend must filter by user_id)
- [x] Stateless Auth - REQUIRED (JWT verification independent)
- [x] Token Expiry - REQUIRED (7 days max)
- [x] No Shared DB Session - REQUIRED (frontend/backend verify independently)
- [x] CORS Configuration - NEEDS VERIFICATION

### Gate 4: Free Services Strategy
- [x] Neon DB free tier - IN USE
- [x] Vercel free tier - IN USE
- [x] Better Auth open source - IN USE
- [x] No paid API keys required - CONFIRMED

## Phase 0: Research

### Research Needed

1. **Better Auth JWT Plugin Configuration**
   - Current state: Better Auth installed but not properly configured with JWT
   - Need to verify: How Better Auth JWT plugin integrates with existing FastAPI JWT validation
   - Key question: Can Better Auth and FastAPI share the same JWT secret?

2. **JWT Token Format Compatibility**
   - Current issue: All protected endpoints return 401
   - Need to verify: Token format expected by FastAPI vs what Better Auth generates
   - Key question: Is the JWT "sub" claim a string (Better Auth) or integer (FastAPI expects)?

3. **CORS Configuration**
   - Current config: `CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-frontend.vercel.app`
   - Need to verify: Credentials: true setting, preflight handling
   - Key question: Is CORS blocking the Authorization header?

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth Strategy | Better Auth + FastAPI JWT | Better Auth handles UI auth, FastAPI validates JWT independently |
| JWT Secret | Share BETTER_AUTH_SECRET with backend | Single source of truth for token validation |
| Token Format | Use Better Auth default (string user ID) | Avoid schema conflicts with existing users |
| Token Storage Key | Use `better-auth.session-token` | Consistent with Better Auth's cookie-based approach |

## Phase 1: Design & Contracts

### Entities (from data-model.md)

**User** - Registered user with email, password hash, and timestamps (managed by Better Auth)

**Session** - Authenticated session with token and expiration (managed by Better Auth)

**Task** - Todo item owned by a user with title, description, priority, and tags (FastAPI SQLModel)

### API Contracts

**Authentication Endpoints (Better Auth)**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Create new account |
| POST | `/api/auth/signin` | Authenticate user |
| POST | `/api/auth/signout` | End session |
| GET | `/api/auth/session` | Get current session |

**Task Endpoints (FastAPI - Protected)**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List all tasks for user |
| POST | `/api/tasks` | Create new task |
| GET | `/api/tasks/{id}` | Get task details |
| PUT | `/api/tasks/{id}` | Update task |
| PATCH | `/api/tasks/{id}` | Toggle completion |
| DELETE | `/api/tasks/{id}` | Delete task |

**Tag Endpoints (FastAPI - Protected)**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tags` | List all tags for user |
| POST | `/api/tags` | Create new tag |
| DELETE | `/api/tags/{id}` | Delete tag |

### Authentication Flow

```
1. User signs up/in on Frontend → Better Auth creates session + JWT token
2. Frontend stores session token in cookie (Better Auth default)
3. Frontend makes API call → Better Auth attaches Authorization header
4. Backend receives request → Extracts token, verifies with shared secret
5. Backend identifies user → Decodes token to get user_id (string)
6. Backend filters data → Returns only tasks/tags belonging to that user
```

## Project Structure

### Documentation (this feature)

```text
specs/3-fix-auth-issues/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (this command)
├── data-model.md        # Phase 1 output (this command)
├── quickstart.md        # Phase 1 output (this command)
├── contracts/           # Phase 1 output (this command)
│   └── api-endpoints.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── auth/
│   │   ├── dependencies.py    # JWT verification
│   │   └── jwt.py             # Token creation/validation
│   ├── routes/
│   │   ├── auth.py            # Register/login endpoints
│   │   ├── tasks.py           # Task CRUD
│   │   └── tags.py            # Tag management
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── task.py            # Task model
│   │   └── tag.py             # Tag model
│   ├── main.py                # FastAPI app
│   └── database.py            # SQLModel async engine
└── tests/
    └── test_routes_*.py

frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/            # Login/Register pages
│   │   ├── (dashboard)/       # Protected pages
│   │   └── api/auth/[...all]/ # Better Auth API route
│   ├── lib/
│   │   ├── auth.ts            # Better Auth config
│   │   └── api-client.ts      # Axios client for backend
│   └── components/
│       ├── ui/
│       └── task/
├── middleware.ts              # Route protection (TO CREATE)
└── tests/
    └── e2e/

scripts/
└── run_tests.py
```

**Structure Decision**: Web application structure with separate `backend/` and `frontend/` directories as specified in the constitution. Middleware will be created at `frontend/middleware.ts` for route protection.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Next Steps

After this plan is complete:
1. Run `/sp.tasks` to generate implementation tasks
2. Execute tasks using appropriate agents (authentication-agent, fastapi-backend-agent, nextjs-frontend-agent)
3. Test authentication flow end-to-end
4. Verify all protected endpoints work correctly

## Generated Artifacts

- [x] `plan.md` - This file
- [ ] `research.md` - To be created
- [ ] `data-model.md` - To be created
- [ ] `quickstart.md` - To be created
- [ ] `contracts/api-endpoints.md` - To be created
- [ ] `tasks.md` - Created by `/sp.tasks` command
