# Todo Application

A multi-phase todo application project demonstrating progression from CLI to full-stack web application.

## Project Phases

### Phase I: CLI Application (Completed)
A command-line todo manager built with Python, featuring a clean Rich-based UI.

### Phase II: Full-Stack Web Application (In Progress)
A multi-user web application with authentication, priority system, tagging, and advanced filtering.

---

## Phase II: Full-Stack Web Application

### Tech Stack

**Frontend:**
- Next.js 15 with App Router
- React 19 (Server & Client Components)
- TypeScript 5 (strict mode)
- Tailwind CSS
- Better Auth (authentication)

**Backend:**
- FastAPI 0.115+
- Python 3.13+
- SQLModel ORM
- Neon PostgreSQL (serverless)
- JWT authentication (python-jose)

### Features
- User authentication (register, login, logout)
- Task CRUD operations
- Priority system (high/medium/low with color badges)
- Tagging system with autocomplete
- Search by keyword
- Filter by status, priority, tags
- Sort by date, priority, title
- User data isolation

### Quick Start

#### Prerequisites
- Node.js 18+
- Python 3.13+
- UV package manager
- Neon PostgreSQL account (free tier)

#### Backend Setup
```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Environment Variables
Copy `.env.example` to `.env` and configure:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Strong secret key (32+ chars)
- `BETTER_AUTH_SECRET` - Better Auth secret key
- `CORS_ORIGINS` - Allowed frontend origins

### Project Structure

```
todo-fullstack-webapp/
├── frontend/                 # Next.js 15 Application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # API client, utilities
│   │   └── types/           # TypeScript definitions
│   └── package.json
│
├── backend/                  # FastAPI Application
│   ├── src/
│   │   ├── models/          # SQLModel database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── routes/          # API endpoints
│   │   ├── auth/            # JWT verification
│   │   └── main.py          # FastAPI entry point
│   ├── tests/
│   ├── alembic/             # Database migrations
│   └── pyproject.toml
│
├── src/                      # Phase I CLI app (legacy)
├── specs/                    # Feature specifications
├── .env.example              # Environment template
└── README.md
```

---

## Phase I: CLI Application (Legacy)

### Features
- Add tasks with title and optional description
- View all tasks in a formatted table
- Update task title and description
- Delete tasks by ID
- Mark tasks as complete

### Usage
```bash
uv run python -m src.main
```

### Running Tests
```bash
uv run pytest -v
uv run pytest --cov=src --cov-report=term-missing
```

---

## Development

### Specifications
See `specs/2-fullstack-todo-webapp/` for detailed documentation:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `tasks.md` - Implementation tasks
- `data-model.md` - Database schema
- `contracts/openapi.yaml` - API specification

### Context7 Libraries
Use Context7 MCP for up-to-date documentation:
```
use context7 for nextjs
use context7 for fastapi
use context7 for sqlmodel
use context7 for better-auth
```

---

## License

MIT
