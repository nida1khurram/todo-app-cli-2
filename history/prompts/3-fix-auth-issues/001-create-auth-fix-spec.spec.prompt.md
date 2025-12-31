---
id: '001'
title: Create auth fix spec
stage: spec
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 3-fix-auth-issues
branch: 3-fix-auth-issues
user: nida1khurram
command: sp.specify
labels: ["spec","authentication","issues"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/3-fix-auth-issues/spec.md
  - specs/3-fix-auth-issues/checklists/requirements.md
  - ISSUES.md
tests: []
---

## Prompt

# Issues - Todo Webapp

## Authentication Issues

### Issue #1: Better Auth Installed But Not Used

**Status:** 🔴 Open
**Priority:** High

**Description:**
Better Auth package is installed but not being used. App uses custom JWT auth instead.

**Files Involved:**
- `frontend/package.json` - has `"better-auth": "^1.2.0"`
- `frontend/src/lib/auth.ts` - incomplete Better Auth config
- `frontend/src/lib/api-client.ts` - uses custom `authApi`
- `frontend/src/app/(auth)/login/page.tsx` - uses `authApi.login()`
- `frontend/src/app/(auth)/register/page.tsx` - uses `authApi.register()`

### Issue #2: Token Key Mismatch in localStorage

**Status:** 🔴 Open
**Priority:** High

**Description:**
Different parts of code use different keys for storing auth token in localStorage.

### Issue #3: Task Creation Returns 401 Unauthorized

**Status:** 🔴 Open
**Priority:** Critical

**Description:**
POST `/api/tasks` endpoint returns 401 Unauthorized error even after successful login.

### Issue #4: All Protected Endpoints Return 401

**Status:** 🔴 Open
**Priority:** Critical

**Description:**
All authenticated endpoints return 401 Unauthorized.

### Issue #5: Backend CORS May Not Allow Frontend

**Status:** 🟡 Pending
**Priority:** Medium

### Issue #6: Auth Check in Dashboard Layout

**Status:** 🟢 Fixed (but needs Better Auth update)
**Priority:** Medium

### Issue #7: No Middleware for Route Protection

**Status:** 🔴 Open
**Priority:** High

**Description:**
No Next.js middleware to protect routes at the edge.

## Response snapshot

Created feature specification for fixing authentication and API issues:
- Branch: `3-fix-auth-issues`
- Spec file: `specs/3-fix-auth-issues/spec.md`
- 5 user stories with priorities (P1-P3)
- 10 functional requirements
- 6 measurable success criteria
- Checklist: `specs/3-fix-auth-issues/checklists/requirements.md`

All validation passed - no clarification markers needed.

## Outcome

- ✅ Impact: Authentication issues documented and spec created for fixes
- 🧪 Tests: Not applicable
- 📁 Files: 2 files created (spec + checklist)
- 🔁 Next prompts: `/sp.plan` or `/sp.tasks`
- 🧠 Reflection: All issues understood, reasonable defaults applied for assumptions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
