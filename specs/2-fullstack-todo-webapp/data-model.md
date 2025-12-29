# Data Model Specification

**Feature**: Full-Stack Todo Web Application (Phase II)
**Date**: 2025-12-29
**Database**: PostgreSQL 16 with SQLModel ORM

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (UQ)      │
│ password_hash   │
│ created_at      │
└─────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐         ┌─────────────────┐
│      Task       │────M:N──│      Tag        │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │         │ id (PK)         │
│ user_id (FK)    │         │ user_id (FK)    │
│ title           │         │ name            │
│ description     │         │ created_at      │
│ is_completed    │         └─────────────────┘
│ priority        │                   │
│ created_at      │                   │ 1:N
│ updated_at      │                   │
└─────────────────┘                   │
         │                            │
         │                            │
         │         M:N                │
         └──────────┬─────────────────┘
                    │
                    ▼
            ┌─────────────────┐
            │    TaskTag      │
            ├─────────────────┤
            │ task_id (PK,FK) │
            │ tag_id (PK,FK)  │
            │ created_at      │
            └─────────────────┘
```

---

## Entity Definitions

### 1. User Entity

**Purpose**: Represents an authenticated user account.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `email` | String(255) | Unique, Not Null, Index | User's email address (login credential) |
| `password_hash` | String(255) | Not Null | Bcrypt hashed password |
| `created_at` | DateTime | Not Null, Default=now() | Account creation timestamp |

**Relationships**:
- One user has many tasks (1:N)
- One user has many tags (1:N)

**Indexes**:
- Primary key index on `id`
- Unique index on `email`

**Validation Rules**:
- Email must be valid format (validated at application layer)
- Password must be 8+ characters before hashing
- Email uniqueness enforced at database level

**SQLModel Implementation**:
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)
    tags: list["Tag"] = Relationship(back_populates="user", cascade_delete=True)
```

---

### 2. Task Entity

**Purpose**: Represents a single todo item belonging to a user.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique task identifier |
| `user_id` | Integer | Foreign Key (users.id), Not Null, Index | Owner of the task |
| `title` | String(200) | Not Null | Task title/summary |
| `description` | String(2000) | Nullable | Detailed task description |
| `is_completed` | Boolean | Not Null, Default=False, Index | Completion status |
| `priority` | String(10) | Not Null, Default='medium', Index | Priority level (high/medium/low) |
| `created_at` | DateTime | Not Null, Default=now(), Index | Task creation timestamp |
| `updated_at` | DateTime | Not Null, Default=now() | Last modification timestamp |

**Relationships**:
- Many tasks belong to one user (N:1)
- Many tasks can have many tags (M:N via TaskTag)

**Indexes**:
- Primary key index on `id`
- Index on `user_id` (frequent joins and filters)
- Index on `is_completed` (status filtering)
- Index on `priority` (priority filtering)
- Index on `created_at` (sorting by date)

**Validation Rules**:
- Title: 1-200 characters, non-empty after trimming whitespace
- Description: 0-2000 characters, nullable
- Priority: Must be one of ['high', 'medium', 'low']
- User isolation: All queries must filter by `user_id`

**State Transitions**:
```
[Pending] ──(mark complete)──> [Completed]
[Completed] ──(unmark)──> [Pending]
```

**SQLModel Implementation**:
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False, index=True)
    priority: str = Field(default="medium", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tasks")
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model="TaskTag")

    @validator('priority')
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError('Priority must be high, medium, or low')
        return v
```

---

### 3. Tag Entity

**Purpose**: Represents a category label for organizing tasks.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique tag identifier |
| `user_id` | Integer | Foreign Key (users.id), Not Null, Index | Owner of the tag |
| `name` | String(50) | Not Null, Index | Tag name/label |
| `created_at` | DateTime | Not Null, Default=now() | Tag creation timestamp |

**Relationships**:
- Many tags belong to one user (N:1)
- Many tags can be applied to many tasks (M:N via TaskTag)

**Indexes**:
- Primary key index on `id`
- Index on `user_id` (frequent joins and filters)
- Index on `name` (autocomplete search)
- Composite unique constraint on `(user_id, name)` (prevent duplicate tags per user)

**Validation Rules**:
- Name: 1-50 characters, non-empty
- Case-insensitive uniqueness per user (enforced at application layer before insert)
- Tag names trimmed and normalized

**SQLModel Implementation**:
```python
from sqlalchemy import UniqueConstraint

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=50, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="tags")
    tasks: list["Task"] = Relationship(back_populates="tags", link_model="TaskTag")

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="unique_user_tag"),
    )
```

---

### 4. TaskTag Entity (Junction Table)

**Purpose**: Represents the many-to-many relationship between tasks and tags.

**Fields**:
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `task_id` | Integer | Primary Key, Foreign Key (tasks.id) | Task identifier |
| `tag_id` | Integer | Primary Key, Foreign Key (tags.id) | Tag identifier |
| `created_at` | DateTime | Not Null, Default=now() | Association creation timestamp |

**Relationships**:
- Composite primary key ensures unique task-tag pairs
- Cascade delete when task or tag is deleted

**Indexes**:
- Composite primary key index on `(task_id, tag_id)`

**SQLModel Implementation**:
```python
class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True, ondelete="CASCADE")
    tag_id: int = Field(foreign_key="tags.id", primary_key=True, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Database Schema SQL (Reference)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_tags_name ON tags(name);
CREATE UNIQUE INDEX idx_tags_user_name ON tags(user_id, name);

-- TaskTag junction table
CREATE TABLE task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (task_id, tag_id)
);
```

---

## Data Access Patterns

### Common Query Patterns

**1. Get all tasks for a user (with optional filters):**
```sql
SELECT t.*, array_agg(tg.name) as tags
FROM tasks t
LEFT JOIN task_tags tt ON t.id = tt.task_id
LEFT JOIN tags tg ON tt.tag_id = tg.id
WHERE t.user_id = :user_id
  AND (:status IS NULL OR t.is_completed = :status)
  AND (:priority IS NULL OR t.priority = :priority)
GROUP BY t.id
ORDER BY t.created_at DESC;
```

**2. Get tasks with specific tag:**
```sql
SELECT t.*
FROM tasks t
JOIN task_tags tt ON t.id = tt.task_id
JOIN tags tg ON tt.tag_id = tg.id
WHERE t.user_id = :user_id
  AND tg.name = :tag_name;
```

**3. Full-text search in tasks:**
```sql
SELECT *
FROM tasks
WHERE user_id = :user_id
  AND (
    title ILIKE :search_pattern
    OR description ILIKE :search_pattern
  );
```

**4. Autocomplete tags:**
```sql
SELECT name
FROM tags
WHERE user_id = :user_id
  AND name ILIKE :prefix || '%'
ORDER BY name
LIMIT 10;
```

---

## Data Integrity Rules

### Referential Integrity
- All foreign keys enforced at database level
- Cascade delete: When user deleted, all their tasks and tags are deleted
- Cascade delete: When task deleted, all task_tags associations are deleted
- Cascade delete: When tag deleted, all task_tags associations are deleted

### Uniqueness Constraints
- User email must be unique globally
- Tag name must be unique per user (case-insensitive at application layer)
- Task-tag pairs must be unique (composite primary key)

### Check Constraints (Application Layer)
- Task priority must be 'high', 'medium', or 'low'
- Title and tag names must not be empty after trimming
- Email must match valid format

---

## Migration Strategy

### Initial Migration (Alembic)
```python
# alembic/versions/001_initial_schema.py

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.String(2000)),
        sa.Column('is_completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('priority', sa.String(10), nullable=False, default='medium'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_is_completed', 'tasks', ['is_completed'])
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_created_at', 'tasks', ['created_at'])

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_tags_user_id', 'tags', ['user_id'])
    op.create_index('idx_tags_name', 'tags', ['name'])
    op.create_index('idx_tags_user_name', 'tags', ['user_id', 'name'], unique=True)

    # Create task_tags junction table
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('task_id', 'tag_id'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE')
    )

def downgrade():
    op.drop_table('task_tags')
    op.drop_table('tags')
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## Performance Considerations

### Index Strategy
- **Primary keys**: Automatic B-tree indexes for fast lookups
- **Foreign keys**: Explicit indexes for join performance
- **Filter columns**: Indexes on frequently filtered fields (user_id, is_completed, priority)
- **Sort columns**: Index on created_at for chronological sorting
- **Composite index**: (user_id, name) for tag uniqueness and autocomplete

### Query Optimization
- Use `SELECT` with specific columns instead of `SELECT *`
- Limit result sets with pagination (LIMIT/OFFSET)
- Eager load relationships to avoid N+1 queries
- Use database-level filtering instead of application-level filtering

### Connection Pooling
- Pool size: 5 connections (sufficient for free tier)
- Max overflow: 10 additional connections for bursts
- Pre-ping: Verify connections before use (handles serverless cold starts)
- Recycle: Close connections after 1 hour

---

## Sample Data

### Seed Data for Development

**User:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "password_hash": "$2b$12$...",
  "created_at": "2025-12-29T00:00:00Z"
}
```

**Tasks:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Complete Phase II specification",
    "description": "Write detailed spec for full-stack todo app",
    "is_completed": true,
    "priority": "high",
    "created_at": "2025-12-28T10:00:00Z",
    "updated_at": "2025-12-29T12:00:00Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "title": "Implement authentication system",
    "description": "Set up Better Auth and JWT verification",
    "is_completed": false,
    "priority": "high",
    "created_at": "2025-12-29T09:00:00Z",
    "updated_at": "2025-12-29T09:00:00Z"
  }
]
```

**Tags:**
```json
[
  {"id": 1, "user_id": 1, "name": "work", "created_at": "2025-12-28T10:00:00Z"},
  {"id": 2, "user_id": 1, "name": "urgent", "created_at": "2025-12-28T10:00:00Z"},
  {"id": 3, "user_id": 1, "name": "backend", "created_at": "2025-12-29T09:00:00Z"}
]
```

**TaskTags:**
```json
[
  {"task_id": 1, "tag_id": 1, "created_at": "2025-12-28T10:00:00Z"},
  {"task_id": 1, "tag_id": 2, "created_at": "2025-12-28T10:00:00Z"},
  {"task_id": 2, "tag_id": 3, "created_at": "2025-12-29T09:00:00Z"}
]
```

---

## Summary

**Entities**: 4 tables (User, Task, Tag, TaskTag)
**Relationships**: 1:N (User-Task, User-Tag), M:N (Task-Tag via TaskTag)
**Indexes**: 11 indexes for optimal query performance
**Constraints**: Foreign keys, unique constraints, check constraints
**Security**: User isolation enforced at query level via user_id filtering

Database schema is normalized, scalable, and optimized for the Phase II feature requirements.
