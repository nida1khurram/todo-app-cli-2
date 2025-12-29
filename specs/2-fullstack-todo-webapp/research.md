# Research & Technology Decisions

**Feature**: Full-Stack Todo Web Application (Phase II)
**Date**: 2025-12-29
**Status**: Complete

---

## 1. Monorepo Structure Decision

### Decision
Use **separate frontend/ and backend/ directories** at repository root with independent package management.

### Rationale
- Clear separation of concerns between Next.js and FastAPI ecosystems
- Independent deployment pipelines (Vercel for frontend, Railway/Render for backend)
- Different package managers (npm/pnpm for frontend, UV for backend)
- Easier CI/CD configuration with separate build scripts
- Better compatibility with free-tier deployment services

### Alternatives Considered
1. **Nx/Turborepo monorepo**: Rejected - adds complexity, tooling overhead for simple 2-service architecture
2. **Single directory with mixed tech**: Rejected - conflicts between Node.js and Python tooling
3. **Separate repositories**: Rejected - harder to maintain consistency, duplicate configuration

### Implementation
```
todo-fullstack-webapp/
├── frontend/               # Next.js 15 application
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # API client, utilities
│   │   └── types/         # TypeScript types
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── next.config.js
├── backend/               # FastAPI application
│   ├── src/
│   │   ├── models/        # SQLModel database models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── routes/        # API endpoint routers
│   │   ├── auth/          # JWT verification middleware
│   │   ├── database.py    # DB connection, session management
│   │   └── main.py        # FastAPI app entry point
│   ├── tests/
│   ├── pyproject.toml
│   └── alembic/           # Database migrations
└── .env.example           # Environment variables template
```

---

## 2. Authentication Architecture

### Decision
**Better Auth (frontend) → JWT tokens → python-jose verification (backend)**

### Rationale
- Better Auth handles frontend session management with minimal setup
- JWT tokens enable stateless API authentication
- python-jose provides standard JWT verification for FastAPI
- Clean separation: frontend manages sessions, backend validates tokens
- No shared session store required (Redis-free for MVP)

### Authentication Flow
```
1. User Registration/Login (Frontend)
   → Better Auth creates session
   → Better Auth generates JWT token
   → Token stored in HTTP-only cookie

2. API Request (Frontend → Backend)
   → Next.js API client includes JWT in Authorization header
   → Bearer token format: "Bearer <jwt_token>"

3. Token Verification (Backend)
   → FastAPI dependency extracts token from header
   → python-jose verifies signature using shared JWT_SECRET
   → Decode payload to get user_id
   → Attach user_id to request context

4. User Isolation (Backend)
   → All database queries filter by authenticated user_id
   → Prevent cross-user data access at ORM level
```

### Implementation Components

**Frontend (Better Auth setup):**
- `src/lib/auth.ts` - Better Auth configuration
- `src/app/api/auth/[...auth]/route.ts` - Auth API routes
- `src/lib/api-client.ts` - Axios/fetch client with JWT injection

**Backend (JWT verification):**
- `src/auth/jwt.py` - Token verification utilities
- `src/auth/dependencies.py` - FastAPI dependency for `get_current_user`
- `src/auth/middleware.py` - Optional middleware for global auth

### Security Considerations
- JWT_SECRET must be strong (32+ characters)
- Token expiration: 7 days (configurable)
- HTTP-only cookies prevent XSS attacks
- CORS configured to allow frontend origin only

### Alternatives Considered
1. **Session-based auth with Redis**: Rejected - adds Redis dependency, not needed for MVP scale
2. **OAuth2 Password Flow**: Rejected - unnecessary complexity for email/password auth
3. **NextAuth.js**: Rejected - Better Auth more modern, lighter weight

---

## 3. Database Schema Design (SQLModel)

### Decision
**Four-table schema with many-to-many relationship** for tasks and tags.

### Rationale
- Normalized design prevents data duplication
- Many-to-many via junction table enables multiple tags per task
- User foreign keys enforce data isolation at database level
- Timestamps enable audit trails
- Indexes on frequently queried fields improve performance

### Schema Design

**User Table:**
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    tags: list["Tag"] = Relationship(back_populates="user")
```

**Task Table:**
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False, index=True)
    priority: str = Field(default="medium", index=True)  # high/medium/low
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
```

**Tag Table:**
```python
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=50, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTag)

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_user_tag"),
    )
```

**TaskTag Junction Table:**
```python
class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Indexes Strategy
- Primary keys: automatic unique index
- Foreign keys: explicit index for join performance
- Frequently filtered fields: `user_id`, `is_completed`, `priority`, `created_at`
- Search fields: `email`, `tag.name`
- Composite unique constraint: `(user_id, tag_name)` prevents duplicate tags per user

### Migration Strategy
- Use Alembic for schema migrations
- Initial migration creates all tables
- Future migrations handle schema evolution
- Never destructive migrations without backup

---

## 4. API Endpoint Organization

### Decision
**RESTful endpoints organized by resource** with FastAPI APIRouter.

### Rationale
- RESTful conventions provide predictable API structure
- APIRouter enables modular endpoint organization
- Dependency injection for auth and database sessions
- OpenAPI documentation auto-generated
- Easy to add new resources without changing main.py

### Endpoint Structure

**Authentication Endpoints** (`routes/auth.py`):
```
POST   /api/auth/register    - Create new user account
POST   /api/auth/login        - Authenticate user
POST   /api/auth/logout       - Invalidate session
GET    /api/auth/me           - Get current user info
```

**Task Endpoints** (`routes/tasks.py`):
```
GET    /api/tasks                      - List user's tasks (with filters/sort)
POST   /api/tasks                      - Create new task
GET    /api/tasks/{task_id}            - Get single task
PUT    /api/tasks/{task_id}            - Update entire task
PATCH  /api/tasks/{task_id}            - Partial update (e.g., mark complete)
DELETE /api/tasks/{task_id}            - Delete task
GET    /api/tasks/search?q={keyword}   - Search tasks by keyword
```

**Tag Endpoints** (`routes/tags.py`):
```
GET    /api/tags                 - List user's tags (autocomplete support)
POST   /api/tags                 - Create new tag
GET    /api/tags/{tag_id}        - Get single tag
DELETE /api/tags/{tag_id}        - Delete tag
GET    /api/tags/{tag_id}/tasks  - Get tasks with this tag
```

### Query Parameters for Filtering/Sorting

**GET /api/tasks** supports:
- `?status=completed` - Filter by completion status (all/completed/pending)
- `?priority=high` - Filter by priority (high/medium/low)
- `?tags=work,urgent` - Filter by tag names (comma-separated)
- `?search=keyword` - Full-text search in title/description
- `?sort_by=created_at` - Sort field (created_at/priority/title)
- `?sort_order=desc` - Sort direction (asc/desc)
- `?limit=50&offset=0` - Pagination

### Response Format
All endpoints return consistent JSON structure:

**Success (2xx):**
```json
{
  "data": { ... },
  "message": "Success message"
}
```

**Error (4xx/5xx):**
```json
{
  "detail": "Error message",
  "error_code": "VALIDATION_ERROR"
}
```

### Alternatives Considered
1. **GraphQL**: Rejected - REST sufficient for MVP, GraphQL adds complexity
2. **RPC-style endpoints**: Rejected - less standard, harder to document
3. **Nested routes** (`/users/{id}/tasks`): Rejected - user always authenticated, redundant nesting

---

## 5. Frontend Component Architecture

### Decision
**Mixed Server and Client Components** using Next.js 15 App Router patterns.

### Rationale
- Server Components reduce client bundle size
- Client Components enable interactivity (forms, filters)
- React Server Components fetch data closer to database (API backend)
- Clear boundaries based on interactivity needs

### Component Strategy

**Server Components** (default, no 'use client'):
- Page layouts
- Task list display (initial render)
- Static navigation
- Data fetching from API

**Client Components** ('use client' directive):
- Forms (task create/edit)
- Filter controls (checkboxes, dropdowns)
- Search input with debouncing
- Delete confirmation modals
- Tag autocomplete input

### File Organization

```
frontend/src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx          # Server Component
│   │   └── register/page.tsx       # Server Component
│   ├── (dashboard)/
│   │   ├── layout.tsx              # Server Component
│   │   └── tasks/
│   │       ├── page.tsx            # Server Component (data fetching)
│   │       ├── task-list.tsx       # Client Component (interactive)
│   │       ├── task-form.tsx       # Client Component (form)
│   │       └── filters.tsx         # Client Component (filters)
│   └── api/
│       └── auth/[...auth]/route.ts # Better Auth API routes
├── components/
│   ├── ui/
│   │   ├── button.tsx              # Client Component
│   │   ├── input.tsx               # Client Component
│   │   └── card.tsx                # Server Component (presentational)
│   └── task/
│       ├── priority-badge.tsx      # Server Component (display only)
│       ├── tag-list.tsx            # Server Component (display only)
│       └── task-card.tsx           # Server Component (wraps client actions)
└── lib/
    ├── api-client.ts               # API wrapper with JWT injection
    └── auth.ts                     # Better Auth configuration
```

### Data Flow Patterns

**Server Component Data Fetching:**
```typescript
// app/tasks/page.tsx (Server Component)
async function TasksPage() {
  const tasks = await fetchTasks(); // Direct API call, no client fetch
  return <TaskList initialTasks={tasks} />;
}
```

**Client Component Mutations:**
```typescript
// components/task-form.tsx (Client Component)
'use client';

function TaskForm() {
  const handleSubmit = async (data) => {
    await apiClient.post('/api/tasks', data); // JWT injected automatically
    router.refresh(); // Revalidate server components
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### State Management
- **Server state**: React Server Components + `fetch` with caching
- **Client state**: React useState/useReducer (no Redux needed for MVP)
- **Form state**: React Hook Form or native form handling
- **URL state**: Next.js useSearchParams for filters/sorting

### Alternatives Considered
1. **All Client Components**: Rejected - larger bundle, slower initial load
2. **SPA with client-side routing**: Rejected - misses Next.js SSR benefits
3. **getServerSideProps (Pages Router)**: Rejected - App Router more modern

---

## 6. Database Connection & Async Operations

### Decision
**asyncpg driver with SQLModel async engine** and dependency injection for sessions.

### Rationale
- asyncpg is fastest PostgreSQL driver for Python
- SQLModel provides type-safe ORM with async support
- Dependency injection ensures proper session cleanup
- Connection pooling improves performance under load

### Connection Setup

**Database Configuration** (`backend/src/database.py`):
```python
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # Neon PostgreSQL URL

# Async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    pool_size=5,  # Max connections in pool
    max_overflow=10,  # Max extra connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before using
)

# Async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    """Dependency for FastAPI routes."""
    async with async_session() as session:
        yield session
```

### Query Patterns

**Get All Tasks (with filters):**
```python
from sqlmodel import select

async def get_user_tasks(
    user_id: int,
    session: AsyncSession,
    status: str | None = None,
    priority: str | None = None,
):
    query = select(Task).where(Task.user_id == user_id)

    if status == "completed":
        query = query.where(Task.is_completed == True)
    elif status == "pending":
        query = query.where(Task.is_completed == False)

    if priority:
        query = query.where(Task.priority == priority)

    query = query.order_by(Task.created_at.desc())

    result = await session.execute(query)
    return result.scalars().all()
```

**Create Task with Tags:**
```python
async def create_task_with_tags(
    user_id: int,
    task_data: TaskCreate,
    tag_names: list[str],
    session: AsyncSession,
):
    # Create task
    task = Task(**task_data.dict(), user_id=user_id)
    session.add(task)
    await session.flush()  # Get task.id without committing

    # Get or create tags
    for tag_name in tag_names:
        result = await session.execute(
            select(Tag).where(
                Tag.user_id == user_id,
                Tag.name == tag_name
            )
        )
        tag = result.scalar_one_or_none()

        if not tag:
            tag = Tag(user_id=user_id, name=tag_name)
            session.add(tag)
            await session.flush()

        # Create task-tag association
        task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
        session.add(task_tag)

    await session.commit()
    await session.refresh(task)
    return task
```

### Connection Pool Configuration

**For Neon Serverless Postgres:**
- `pool_size=5` - Sufficient for free tier (10 max connections)
- `max_overflow=10` - Allow bursts up to 15 connections
- `pool_pre_ping=True` - Handle serverless cold starts
- `pool_recycle=3600` - Recycle connections after 1 hour

### Error Handling
```python
from sqlalchemy.exc import IntegrityError

try:
    await session.commit()
except IntegrityError:
    await session.rollback()
    raise HTTPException(
        status_code=409,
        detail="Resource already exists"
    )
```

---

## 7. Security & User Isolation Patterns

### Decision
**Defense-in-depth approach** with isolation at multiple layers.

### Rationale
- Never trust client data
- Enforce user isolation at database query level
- Validate all inputs with Pydantic
- Prevent common web vulnerabilities

### Layer 1: Input Validation (Pydantic Schemas)

```python
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    priority: str = Field("medium", regex="^(high|medium|low)$")

    @validator('title')
    def title_not_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()
```

### Layer 2: Authentication Verification

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """Extract and verify JWT token, return user_id."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

### Layer 3: Authorization (User Isolation)

```python
async def get_task_or_404(
    task_id: int,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Task:
    """Get task and verify ownership."""
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # User isolation
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task
```

### Layer 4: CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-app.vercel.app"  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Layer 5: SQL Injection Prevention
- SQLModel/SQLAlchemy uses parameterized queries
- Never string concatenation for SQL
- All user input sanitized through ORM

### Layer 6: XSS Prevention (Frontend)
- React automatically escapes JSX values
- Tailwind CSS (no inline styles)
- HTTP-only cookies prevent JS access to tokens

### Security Checklist
- ✅ All endpoints require authentication (except /auth/login, /auth/register)
- ✅ User isolation enforced at database query level
- ✅ JWT secrets stored in environment variables
- ✅ Passwords hashed with bcrypt (via passlib)
- ✅ HTTPS enforced in production (Vercel/Railway handle SSL)
- ✅ CORS restricted to frontend origin
- ✅ Input validation on all endpoints
- ✅ SQL injection prevented via ORM
- ✅ XSS prevented via React escaping

---

## 8. Development Environment

### Frontend Environment Variables
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<generate-secret-key>
BETTER_AUTH_URL=http://localhost:3000
```

### Backend Environment Variables
```env
# .env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
JWT_SECRET=<generate-strong-secret-32-chars>
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### Local Development Setup
1. **Backend**: `cd backend && uv sync && uv run uvicorn src.main:app --reload`
2. **Frontend**: `cd frontend && npm install && npm run dev`
3. **Database**: Use Neon free tier (no local Postgres needed)

---

## 9. Deployment Strategy

### Frontend Deployment (Vercel)
- Auto-deploy from GitHub on push to main
- Environment variables configured in Vercel dashboard
- Automatic HTTPS, CDN, edge functions

### Backend Deployment (Railway or Render)
- Auto-deploy from GitHub on push to main
- Environment variables configured in platform dashboard
- Automatic HTTPS, health checks
- Free tier: 500 hours/month (Railway) or always-on (Render free tier)

### Database (Neon Serverless PostgreSQL)
- Always-on free tier
- Automatic backups
- No manual scaling needed for MVP traffic

---

## Summary

All technology decisions are finalized and ready for implementation:

1. ✅ **Monorepo**: Separate frontend/ and backend/ directories
2. ✅ **Auth**: Better Auth → JWT → python-jose verification
3. ✅ **Database**: 4-table schema with SQLModel + asyncpg
4. ✅ **API**: RESTful endpoints organized by resource
5. ✅ **Frontend**: Mixed Server/Client Components (Next.js App Router)
6. ✅ **Database Ops**: Async queries with connection pooling
7. ✅ **Security**: Multi-layer defense with user isolation at query level

No unresolved clarifications. Ready to proceed to Phase 1: Design.
