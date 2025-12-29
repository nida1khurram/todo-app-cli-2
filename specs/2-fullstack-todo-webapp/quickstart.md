# Quick Start Guide

**Feature**: Full-Stack Todo Web Application (Phase II)
**Target Audience**: Developers implementing this feature
**Estimated Setup Time**: 15 minutes

---

## Prerequisites

Before starting, ensure you have:

- [ ] **Node.js 18+** installed (`node --version`)
- [ ] **Python 3.13+** installed (`python --version`)
- [ ] **UV package manager** installed (`uv --version`)
- [ ] **npm or pnpm** installed
- [ ] **Git** installed
- [ ] **Neon PostgreSQL** account created (free tier)
- [ ] **Code editor** (VS Code recommended)

---

## Project Structure Overview

```
todo-fullstack-webapp/
├── frontend/               # Next.js 15 application
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # API client, auth config
│   │   └── types/         # TypeScript definitions
│   ├── package.json
│   └── next.config.js
│
├── backend/               # FastAPI application
│   ├── src/
│   │   ├── models/        # SQLModel database models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── routes/        # API endpoint routers
│   │   ├── auth/          # JWT verification
│   │   ├── database.py    # DB connection
│   │   └── main.py        # FastAPI entry point
│   ├── tests/
│   ├── pyproject.toml
│   └── alembic/           # Database migrations
│
├── specs/                 # Feature specifications
├── .env.example           # Environment template
└── README.md
```

---

## Setup Steps

### 1. Environment Setup

**Create Neon Database**:
1. Go to [neon.tech](https://neon.tech)
2. Create free account
3. Create new project: `todo-app-phase2`
4. Copy connection string (looks like: `postgresql://user:pass@host/db`)

**Create Environment Files**:

**Backend** (`.env` in project root):
```env
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/todo_db?sslmode=require
JWT_SECRET=your-super-secret-jwt-key-min-32-characters
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-better-auth-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

**Generate Secrets**:
```bash
# Generate JWT_SECRET (Python)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate BETTER_AUTH_SECRET (Node.js)
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

---

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies with UV
uv sync

# Run database migrations
uv run alembic upgrade head

# Start development server
uv run uvicorn src.main:app --reload --port 8000
```

**Verify Backend**:
- Open http://localhost:8000/docs
- You should see Swagger UI with API documentation
- Test `/api/auth/register` endpoint

---

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in new terminal)
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Start development server
npm run dev
# or
pnpm dev
```

**Verify Frontend**:
- Open http://localhost:3000
- You should see the login/register page
- Try creating an account

---

### 4. Verify Full Stack

**Test Authentication Flow**:
1. Register new user at http://localhost:3000/register
2. Check browser DevTools → Network tab
3. Verify JWT token in response
4. Verify redirect to dashboard

**Test Task Creation**:
1. Create a task from dashboard
2. Check Network tab for POST request to backend
3. Verify task appears in list
4. Check database in Neon dashboard

---

## Development Workflow

### Running Both Services

**Terminal 1 (Backend)**:
```bash
cd backend
uv run uvicorn src.main:app --reload
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

### Making Changes

**Frontend Changes**:
- Edit files in `frontend/src/`
- Hot reload automatically updates browser
- Check console for errors

**Backend Changes**:
- Edit files in `backend/src/`
- FastAPI auto-reloads on file save
- Check terminal for errors

**Database Changes**:
```bash
# Create new migration
cd backend
uv run alembic revision --autogenerate -m "description"

# Apply migration
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

---

## Common Commands

### Backend

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing

# Format code
uv run ruff format .

# Lint code
uv run ruff check . --fix

# Type check
uv run mypy src/

# Start server
uv run uvicorn src.main:app --reload
```

### Frontend

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run production build locally
npm run start

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Lint code
npm run lint

# Type check
npm run type-check
```

---

## API Testing

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter JWT token: `Bearer <your-token>`
4. Test endpoints directly from browser

### Using curl

**Register User**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'
```

**Get Tasks**:
```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Task","priority":"high","tags":["work"]}'
```

---

## Troubleshooting

### Backend Issues

**Problem**: `sqlalchemy.exc.OperationalError: connection refused`
**Solution**: Check DATABASE_URL in .env file, verify Neon database is running

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Run `uv sync` to install dependencies

**Problem**: `401 Unauthorized` on all endpoints
**Solution**: Check JWT_SECRET matches between frontend and backend

### Frontend Issues

**Problem**: `CORS policy: No 'Access-Control-Allow-Origin' header`
**Solution**: Check CORS_ORIGINS in backend .env includes http://localhost:3000

**Problem**: `Failed to fetch` when calling API
**Solution**: Verify backend is running on port 8000, check NEXT_PUBLIC_API_URL

**Problem**: Better Auth errors
**Solution**: Verify BETTER_AUTH_SECRET is set, check database connection

### Database Issues

**Problem**: Migration fails with "relation already exists"
**Solution**: Drop all tables and re-run migrations from scratch

**Problem**: Cannot connect to Neon
**Solution**: Check connection string includes `sslmode=require`, verify credentials

---

## Database Management

### View Data in Neon Dashboard

1. Go to neon.tech dashboard
2. Select your project
3. Click "SQL Editor"
4. Run queries:
   ```sql
   SELECT * FROM users;
   SELECT * FROM tasks WHERE user_id = 1;
   SELECT * FROM tags;
   ```

### Reset Database

```bash
# Drop all tables
cd backend
uv run alembic downgrade base

# Recreate tables
uv run alembic upgrade head
```

---

## Development Tips

### Hot Reload

- **Frontend**: Saves automatically trigger browser refresh
- **Backend**: FastAPI reloads on Python file changes
- **Database**: Migrations require manual application

### Debugging

**Frontend**:
- Use React DevTools extension
- Check browser console for errors
- Use `console.log()` for quick debugging
- Use VS Code debugger with `debugger;` statements

**Backend**:
- Check terminal output for FastAPI logs
- Use `print()` statements (remove before committing)
- Use VS Code debugger with breakpoints
- Check `/docs` endpoint for API schema

### Code Organization

- Keep components small (<200 lines)
- One model per file in `backend/src/models/`
- Group related endpoints in router files
- Use TypeScript types for API responses

---

## Testing Strategy

### Backend Tests

```bash
# Unit tests for models
uv run pytest tests/test_models.py

# Integration tests for API
uv run pytest tests/test_api.py

# Test with coverage
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Frontend Tests

```bash
# Component tests
npm run test

# E2E tests (if configured)
npm run test:e2e

# Watch mode for TDD
npm run test:watch
```

---

## Next Steps

After setup is complete:

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 3000
3. ✅ Can register and login
4. ✅ Can create tasks

**Ready to implement**:
- Run `/sp.tasks` to generate implementation tasks
- Follow TDD approach (write tests first)
- Implement features incrementally
- Deploy when MVP complete

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Frontend Dev | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| ReDoc API Docs | http://localhost:8000/redoc |
| Neon Dashboard | https://console.neon.tech |

| Command | Purpose |
|---------|---------|
| `uv run uvicorn src.main:app --reload` | Start backend |
| `npm run dev` | Start frontend |
| `uv run pytest` | Run backend tests |
| `npm test` | Run frontend tests |
| `uv run alembic upgrade head` | Apply migrations |

---

## Support & Resources

- **Specification**: `specs/2-fullstack-todo-webapp/spec.md`
- **Research**: `specs/2-fullstack-todo-webapp/research.md`
- **Data Model**: `specs/2-fullstack-todo-webapp/data-model.md`
- **API Contracts**: `specs/2-fullstack-todo-webapp/contracts/openapi.yaml`
- **Context7 Guide**: `CONTEXT7_QUICK_REFERENCE.md`

**Getting Help**:
- Check specification documents first
- Review research.md for architectural decisions
- Use Context7 for library documentation: `use context7 for <library>`
- Check OpenAPI schema in `/docs` endpoint

---

**Estimated Time**: 15 minutes setup + ongoing development

Ready to start implementing! Run `/sp.tasks` to generate detailed implementation tasks.
