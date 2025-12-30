---
id: 005
title: Fix Task Creation and Server Issues
stage: misc
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fullstack-todo-webapp
branch: 2-fullstack-todo-webapp
user: nida1khurram
command: manual
labels: ["task-creation", "bug-fix", "debugging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/schemas/task.py
  - backend/src/routes/tasks.py
  - backend/src/routes/auth.py
  - backend/.env
tests:
  - manual curl testing
---

## Prompt

User asked: "ok app is run but when task is created failed to create tasks"

## Response snapshot

**Issues Fixed:**

1. **Task Creation Error (AttributeError: 'Task' object has no attribute 'tags')**
   - Root cause: TaskResponse schema had `from_attributes: True` which tried to access ORM attributes
   - Fix: Set `model_config = {"from_attributes": False}` in TaskResponse class
   - File: `backend/src/schemas/task.py:66`

2. **JWT Token Creation Error**
   - Error: `AttributeError: 'int' object has no attribute 'copy'`
   - Root cause: `create_access_token(user.id)` was passing int instead of dict
   - Fix: Changed to `create_access_token({"sub": str(user.id)})` in auth routes
   - Files: `backend/src/routes/auth.py:56,94`

3. **Password Hashing Compatibility**
   - Changed from passlib to direct bcrypt library

4. **CORS Configuration**
   - Added port 3001 to CORS_ORIGINS in `.env`

**Servers Running:**
- Backend: http://localhost:8000 (with auto-reload)
- Frontend: http://localhost:3003

**Manual Testing:**
- Registration works (201 Created with JWT)
- Task creation API tested via curl
