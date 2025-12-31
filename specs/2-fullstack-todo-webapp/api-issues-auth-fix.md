# API Issues & Better Auth Integration Specification

**Feature:** Full-Stack Todo Webapp - Authentication & API Fixes
**Created:** 2025-12-30
**Status:** Pending Implementation

---

## Executive Summary

Current issues identified in the todo webapp:

1. **Authentication**: Better Auth is installed but NOT being used - app uses custom JWT auth instead
2. **Task Creation API**: Endpoint `/api/tasks` returns 401 Unauthorized errors
3. **API Integration**: Frontend calls are not properly connected to working endpoints

---

## Issue 1: Better Auth Not Integrated

### Current State

Better Auth package is installed in `frontend/package.json`:
```json
"better-auth": "^1.2.0"
```

However, the frontend uses **custom JWT auth** via `authApi` in `api-client.ts`:
- Custom register/login endpoints: `/api/auth/register`, `/api/auth/login`
- Tokens stored in `localStorage` as `access_token`
- Custom axios interceptor for JWT injection

### Problem

- Better Auth configuration exists in `frontend/src/lib/auth.ts` but is incomplete
- No API route handler for Better Auth (`/api/auth/[...all]`)
- Login/register pages use `authApi` instead of Better Auth client
- Inconsistent auth patterns (custom + Better Auth both partially implemented)

### Required Changes

#### 1.1 Configure Better Auth Properly

**File:** `frontend/src/lib/auth.ts`

Current (broken):
```typescript
import { createAuth } from 'better-auth';

export const auth = createAuth({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  secret: process.env.BETTER_AUTH_SECRET || 'default-secret-change-in-production',
  plugins: [],
});
```

Should be:
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "@better-auth/jwt";

export const auth = betterAuth({
  database: /* PostgreSQL connection */,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,
  },
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  secret: process.env.BETTER_AUTH_SECRET!,
  plugins: [
    jwt({
      jwt: {
        secret: process.env.JWT_SECRET!,
        expiresIn: "7d",
      },
    }),
  ],
});
```

#### 1.2 Create Better Auth API Route

**File:** `frontend/src/app/api/auth/[...all]/route.ts`

Current (empty):
```typescript
export const { GET, POST } = /* not configured */;
```

Should be:
```typescript
import { auth } from "@/lib/auth/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

#### 1.3 Update Login/Register Pages

**Files:**
- `frontend/src/app/(auth)/login/page.tsx`
- `frontend/src/app/(auth)/register/page.tsx`

Replace `authApi.register()` / `authApi.login()` with Better Auth client:
```typescript
import { signIn, signUp } from "@/lib/auth/client";

await signUp.email({ email, password });
await signIn.email({ email, password });
```

---

## Issue 2: Task Creation API Returns 401

### Current State

**Endpoint:** `POST /api/tasks`
**Status:** Returns 401 Unauthorized
**Error:** `Could not validate credentials`

### Root Cause Analysis

1. Frontend sends request with JWT token in `Authorization: Bearer <token>` header
2. Backend expects Bearer token via `HTTPBearer` security scheme
3. Token validation fails because:
   - Custom JWT is created on registration
   - Token may be expired or malformed
   - `get_current_user_id` dependency expects valid JWT

### Debug Steps Needed

1. Check if `Authorization` header is being sent by frontend
2. Verify JWT token format: `Bearer eyJ...`
3. Check token expiration in JWT payload
4. Verify `decode_token()` function works correctly
5. Check database connection for user lookup

### Current Backend Token Validation Flow

```
POST /api/tasks
  → Depends(get_current_user_id)
    → HTTPBearer() extracts credentials
    → decode_token(token)
    → Extract payload.sub (user_id)
    → Return user_id (no DB lookup)
```

### Expected Fix

1. Ensure token is being sent from frontend
2. Verify JWT secret matches between creation and validation
3. Check token expiration timestamp

---

## Issue 3: API Client Configuration

### Current State

**File:** `frontend/src/lib/api-client.ts`

- Base URL: `http://localhost:8000` (or `NEXT_PUBLIC_API_URL`)
- JWT token retrieved from `localStorage.getItem('access_token')`
- Interceptor adds `Authorization: Bearer <token>` to requests

### Potential Issues

1. **Token key mismatch**: `auth.ts` checks `localStorage.getItem('token')` but `api-client.ts` uses `access_token`
2. **CORS**: May not allow requests from `localhost:3000` to `localhost:8000`
3. **Environment variables**: `NEXT_PUBLIC_API_URL` may not be set

---

## API Endpoints Summary

### Authentication Endpoints (Current - Custom)

| Method | Endpoint | Status | Notes |
|--------|----------|--------|-------|
| POST | `/api/auth/register` | Working | Creates user, returns JWT |
| POST | `/api/auth/login` | Working | Validates credentials, returns JWT |
| GET | `/api/auth/me` | Working | Returns current user |

### Task Endpoints

| Method | Endpoint | Status | Notes |
|--------|----------|--------|-------|
| GET | `/api/tasks` | Returns 401 | Needs auth |
| POST | `/api/tasks` | Returns 401 | Needs auth - ISSUE |
| GET | `/api/tasks/{id}` | Returns 401 | Needs auth |
| PUT | `/api/tasks/{id}` | Returns 401 | Needs auth |
| PATCH | `/api/tasks/{id}` | Returns 401 | Needs auth |
| DELETE | `/api/tasks/{id}` | Returns 401 | Needs auth |

### Tag Endpoints

| Method | Endpoint | Status | Notes |
|--------|----------|--------|-------|
| GET | `/api/tags` | Returns 401 | Needs auth |
| POST | `/api/tags` | Returns 401 | Needs auth |
| DELETE | `/api/tags/{id}` | Returns 401 | Needs auth |

---

## Required Changes Checklist

### Authentication

- [ ] Configure Better Auth with database adapter
- [ ] Create Better Auth API route handler
- [ ] Update login page to use Better Auth client
- [ ] Update register page to use Better Auth client
- [ ] Create auth client helper (`lib/auth/client.ts`)
- [ ] Create server-side session helper (`lib/auth/server.ts`)
- [ ] Add middleware for route protection
- [ ] Remove custom JWT auth code (or keep as fallback)

### Task API

- [ ] Debug why `/api/tasks` returns 401
- [ ] Verify JWT token is sent in Authorization header
- [ ] Check token creation and validation match
- [ ] Fix any CORS issues
- [ ] Test all task CRUD operations

### Integration

- [ ] Update frontend API client for Better Auth
- [ ] Ensure token storage is consistent
- [ ] Test full user journey: register → login → create task

---

## User Stories

### User Story 1: Authentication with Better Auth
**As a** user
**I want to** register and login using Better Auth
**So that** I have secure, standardized authentication

**Acceptance Criteria:**
- User can sign up with email/password
- User can sign in with email/password
- Session persists across page refreshes
- Protected routes redirect to login if not authenticated

### User Story 2: Task Creation Works
**As a** authenticated user
**I want to** create tasks through the API
**So that** I can manage my todo items

**Acceptance Criteria:**
- POST `/api/tasks` returns 201 on success
- Task is saved with correct user_id
- Frontend shows success message
- Task appears in task list immediately

---

## Technical Constraints

1. **Database**: Neon PostgreSQL (async connection)
2. **Backend**: FastAPI with SQLModel
3. **Frontend**: Next.js 15+ with App Router
4. **Auth**: Must use Better Auth
5. **JWT**: Compatible with both backend validation and Better Auth

---

## Questions for Clarification

1. Should we keep the FastAPI backend for task APIs, or move everything to Next.js API routes?
2. Should Better Auth use the same PostgreSQL database as FastAPI?
3. What's the expected token expiration time?
4. Should we support social auth (Google, GitHub) in addition to email/password?

---

## References

- [Better Auth Documentation](https://www.better-auth.com/docs)
- [Better Auth JWT Plugin](https://www.better-auth.com/docs/plugins/jwt)
- Current backend auth: `backend/src/auth/dependencies.py`
- Current frontend API client: `frontend/src/lib/api-client.ts`
