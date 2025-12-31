# Quick Start: Fix Authentication & API Issues

**Feature**: Fix Authentication & API Issues
**Date**: 2025-12-30

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL (Neon or local)
- Git

## Environment Setup

### 1. Clone and Install Dependencies

```bash
# Backend
cd backend
cp .env.example .env  # Fill in DATABASE_URL and JWT secrets
uv sync

# Frontend
cd frontend
cp .env.local.example .env.local  # Fill in Better Auth secrets
npm install
```

### 2. Environment Variables

**Backend (.env)**:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.region.neon.tech/dbname?ssl=require
JWT_SECRET=your-jwt-secret-min-32-chars
JWT_ALGORITHM=HS256
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
DEBUG=true
```

**Frontend (.env.local)**:
```bash
BETTER_AUTH_SECRET=your-better-auth-secret-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Servers

```bash
# Terminal 1: Backend
cd backend
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 4. Verify Services

- Backend API: http://localhost:8000
- Frontend App: http://localhost:3000
- Health Check: http://localhost:8000/health

## Testing Authentication

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'
```

### 2. Login and Get Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'
```

Response:
```json
{
  "access_token": "eyJ...",
  "user": {"id": 1, "email": "test@example.com"}
}
```

### 3. Create a Task (Authenticated)

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "This is a test task",
    "priority": "high",
    "tags": ["urgent", "test"]
  }'
```

### 4. List Tasks (Authenticated)

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>"
```

## Frontend Testing

1. Open http://localhost:3000
2. Click "Create Account" or "Sign in"
3. Register with email and password
4. After login, navigate to /tasks
5. Try creating a task
6. Verify task appears in the list without 401 errors

## Common Issues

### 401 Unauthorized on Task Creation

**Symptoms**: Registration/Login works, but task creation returns 401

**Causes**:
1. Token not sent in Authorization header
2. JWT secret mismatch between frontend and backend
3. Token expired

**Fix**:
```bash
# Verify token is being sent
curl -v -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Test"}'

# Check backend logs for JWT validation errors
```

### CORS Errors

**Symptoms**: Console shows "Access to XMLHttpRequest has been blocked by CORS policy"

**Fix**: Verify CORS_ORIGINS in backend/.env includes frontend URL:
```bash
CORS_ORIGINS=http://localhost:3000
```

### Token Key Mismatch

**Symptoms**: Inconsistent behavior where sometimes auth works, sometimes not

**Fix**: Ensure all code uses the same localStorage key. Better Auth uses `better-auth.session-token` cookie by default.

## Development Workflow

1. **Make changes** to frontend or backend code
2. **Test locally** with both servers running
3. **Run tests**:
   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd frontend
   npm test
   ```
4. **Commit** using `/sp.git.commit_pr`
5. **Deploy** to Vercel (frontend) and Railway/Render (backend)

## Deployment Checklist

- [ ] All tests pass
- [ ] CORS origins updated for production URL
- [ ] Environment variables set in deployment platform
- [ ] Database migrations applied
- [ ] SSL/HTTPS enabled
- [ ] Error monitoring configured

## Useful Commands

```bash
# Backend
cd backend
uvicorn src.main:app --reload          # Dev server
pytest                                 # Run tests
ruff check .                           # Linting

# Frontend
cd frontend
npm run dev                            # Dev server
npm run build                          # Production build
npm test                               # Run tests
```
