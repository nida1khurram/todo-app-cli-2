---
id: 007
title: Frontend Setup and Server Startup
stage: misc
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fullstack-todo-webapp
branch: 2-fullstack-todo-webapp
user: nida1khurram
command: manual
labels: ["frontend", "server", "setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/api-client.ts
  - frontend/src/lib/auth.ts
  - frontend/tailwind.config.ts
  - frontend/src/app/globals.css
tests:
  - curl health checks
---

## Prompt

User asked to run both backend and frontend servers

## Response snapshot

**Backend (FastAPI):**
- Port: 8000
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Commands:
  ```bash
  cd backend && .venv/Scripts/python.exe -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
  ```

**Frontend (Next.js 15):**
- Port: 3003 (3000, 3001 were in use)
- Home page: http://localhost:3003
- Routes:
  - `/` - Landing page with Sign In/Create Account buttons
  - `/login` - Login page
  - `/register` - Registration page
  - `/tasks` - Dashboard (auth required)

**Frontend Authentication Setup:**
- Uses axios with JWT tokens in localStorage
- Token key: `access_token`
- Auth API methods in `api-client.ts`: register, login, me, logout
- Interceptor adds `Authorization: Bearer <token>` to requests
- 401 errors auto-redirect to `/login`

**Issues Resolved:**
1. Port conflicts - used 3002, 3003 as alternatives
2. Tailwind CSS variables - added CSS var colors to config
3. CORS - added ports 3000 and 3001 to backend .env
