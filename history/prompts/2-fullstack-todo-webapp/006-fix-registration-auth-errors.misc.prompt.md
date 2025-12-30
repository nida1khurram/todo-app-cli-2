---
id: 006
title: Fix Registration and CORS Errors
stage: misc
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fullstack-todo-webapp
branch: 2-fullstack-todo-webapp
user: nida1khurram
command: manual
labels: ["registration", "cors", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/.env
  - backend/src/routes/auth.py
  - backend/src/auth/jwt.py
tests:
  - manual curl testing
---

## Prompt

User reported: "when sign up app error is """Registration failed. Please try again.""" solve"

## Response snapshot

**Issues Fixed:**

1. **CORS Error (400 on OPTIONS preflight)**
   - Port 3001 was not in CORS_ORIGINS
   - Fix: Updated `.env` to include port 3001
   - Before: `CORS_ORIGINS=http://localhost:3000`
   - After: `CORS_ORIGINS=http://localhost:3000,http://localhost:3001`

2. **JWT Token Creation Error**
   - Error: `AttributeError: 'int' object has no attribute 'copy'`
   - Root cause: `create_access_token(data=user.id)` - passing int instead of dict
   - Fix: Changed to `create_access_token({"sub": str(user.id)})`
   - File: `backend/src/routes/auth.py:56,94`

3. **JWT Function Signature**
   - Fixed to accept `data: dict[str, Any]` parameter
   - File: `backend/src/auth/jwt.py`

**Testing:**
- Registration now works (201 Created)
- Returns JWT access_token and user object
- Login also works with same fix
