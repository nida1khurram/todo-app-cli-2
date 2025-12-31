# Data Model: Fix Authentication & API Issues

**Feature**: Fix Authentication & API Issues
**Date**: 2025-12-30

## Entities

### User (Managed by Better Auth)

Better Auth manages the User entity with its own database schema. The frontend uses Better Auth's built-in user model.

**Better Auth User Schema** (auto-created in database):
```sql
CREATE TABLE "user" (
  id TEXT PRIMARY KEY,           -- String ID (e.g., "user_abc123")
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  email_verified BOOLEAN DEFAULT false,
  password TEXT,                 -- Hashed password
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Frontend Type** (from Better Auth):
```typescript
type User = {
  id: string;
  name: string;
  email: string;
  emailVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
};
```

---

### Session (Managed by Better Auth)

Better Auth manages sessions with JWT tokens stored in cookies.

**Better Auth Session Schema**:
```sql
CREATE TABLE "session" (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  expires_at TIMESTAMP NOT NULL,
  token TEXT NOT NULL,
  ip_address TEXT,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**JWT Token Payload**:
```json
{
  "sub": "user_abc123",    // String user ID from Better Auth
  "exp": 1738123456,       // Expiration timestamp
  "iat": 1737518656        // Issued at timestamp
}
```

---

### Task (FastAPI SQLModel)

The Task entity is managed by FastAPI with SQLModel.

**Task Model** (from `backend/src/models/task.py`):
```python
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="user.id")  # Reference to Better Auth user
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # "high", "medium", "low"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tags: list["Tag"] = Relationship(back_populates="tasks", link_model="task_tag")
```

**Database Schema**:
```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_completed ON task(is_completed);
```

---

### Tag (FastAPI SQLModel)

The Tag entity is managed by FastAPI with SQLModel.

**Tag Model** (from `backend/src/models/tag.py`):
```python
class Tag(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key="user.id")  # Each user has their own tags
    name: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="tags", link_model="task_tag")
```

**Database Schema**:
```sql
CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tag_user_id ON tag(user_id);
CREATE INDEX idx_tag_name ON tag(name);
```

---

### TaskTag (Many-to-Many Relationship)

**TaskTag Model** (from `backend/src/models/task_tag.py`):
```python
class TaskTag(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)
```

**Database Schema**:
```sql
CREATE TABLE task_tag (
    task_id INTEGER NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);
```

---

## Entity Relationships

```
User (Better Auth)
 ├── Session (managed by Better Auth)
 └── Task (1:N relationship, filtered by user_id)
      └── TaskTag (M:N through)
           └── Tag (1:N relationship, filtered by user_id)
```

## User ID Mapping

**Challenge**: Better Auth uses string IDs (`user_abc123`) while FastAPI SQLModel uses integer IDs (`1`).

**Solution**:
1. Store `better_auth_user_id` as string column in Task/Tag tables
2. Or: Maintain a mapping table between Better Auth string IDs and local integer IDs

**Proposed Update to Task Model**:
```python
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    better_auth_user_id: str = Field(max_length=255)  # String ID from Better Auth
    title: str = Field(max_length=200)
    # ... other fields
```

This allows proper user isolation while using Better Auth's string IDs.

## Validation Rules

### Task Validation
- `title`: Required, 1-200 characters, trimmed
- `description`: Optional, max 2000 characters
- `priority`: Optional, default "medium", must be "high", "medium", or "low"
- `tags`: Optional list of tag names (strings, max 50 chars each, lowercase)

### Tag Validation
- `name`: Required, 1-50 characters, lowercase, trimmed

### Password Validation (Better Auth)
- Minimum 8 characters
- Must contain uppercase, lowercase, and digit

## State Transitions

### Task States
```
pending → completed (via PATCH /api/tasks/{id})
pending → deleted (via DELETE /api/tasks/{id})
completed → pending (via PATCH /api/tasks/{id})
```

## Indexes

For optimal query performance:
- `task.user_id` - Filter tasks by user
- `task.is_completed` - Filter by completion status
- `task.priority` - Filter by priority
- `tag.user_id` + `tag.name` - Unique constraint for user tags
- `task_tag.task_id` + `task_tag.tag_id` - Relationship indexes
