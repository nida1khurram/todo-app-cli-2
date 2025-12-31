# API Contracts: Fix Authentication & API Issues

**Feature**: Fix Authentication & API Issues
**Date**: 2025-12-30

## Authentication Endpoints (Better Auth)

Better Auth handles these endpoints via `/api/auth/[...all]` route.

### POST /api/auth/signup

Create a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2025-12-30T10:00:00Z",
    "updatedAt": "2025-12-30T10:00:00Z"
  },
  "session": {
    "token": "eyJ...",
    "expiresAt": "2026-01-06T10:00:00Z"
  }
}
```

**Errors**:
- 409: Email already registered
- 400: Validation error

---

### POST /api/auth/signin

Authenticate an existing user.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2025-12-30T10:00:00Z",
    "updatedAt": "2025-12-30T10:00:00Z"
  },
  "session": {
    "token": "eyJ...",
    "expiresAt": "2026-01-06T10:00:00Z"
  }
}
```

**Errors**:
- 401: Invalid email or password
- 400: Validation error

---

### POST /api/auth/signout

End the current session.

**Request**: Empty body

**Response** (200 OK):
```json
{ "success": true }
```

---

### GET /api/auth/session

Get the current session.

**Response** (200 OK):
```json
{
  "session": {
    "token": "eyJ...",
    "expiresAt": "2026-01-06T10:00:00Z",
    "userId": "user_abc123"
  },
  "user": {
    "id": "user_abc123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## Task Endpoints (FastAPI - Protected)

All task endpoints require `Authorization: Bearer <token>` header.

### GET /api/tasks

List all tasks for the authenticated user.

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status_filter | string | No | Filter by "completed", "pending", or "all" |
| priority | string | No | Filter by "high", "medium", "low" |
| search | string | No | Search in title and description |
| tags | string | No | Comma-separated tag names |
| sort_by | string | No | Sort field: "created_at", "priority", "title" |
| sort_order | string | No | Sort order: "asc" or "desc" |

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "user_abc123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false,
    "priority": "high",
    "created_at": "2025-12-30T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z",
    "tags": ["urgent", "shopping"]
  },
  {
    "id": 2,
    "user_id": "user_abc123",
    "title": "Finish report",
    "description": "Q4 summary",
    "is_completed": true,
    "priority": "medium",
    "created_at": "2025-12-29T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z",
    "tags": ["work"]
  }
]
```

**Errors**:
- 401: Unauthorized (missing or invalid token)

---

### POST /api/tasks

Create a new task.

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "high",
  "tags": ["urgent", "shopping"]
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "priority": "high",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z",
  "tags": ["urgent", "shopping"]
}
```

**Errors**:
- 401: Unauthorized
- 422: Validation error (invalid input)

---

### GET /api/tasks/{task_id}

Get a single task by ID.

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "priority": "high",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z",
  "tags": ["urgent", "shopping"]
}
```

**Errors**:
- 401: Unauthorized
- 404: Task not found or not owned by user

---

### PUT /api/tasks/{task_id}

Update an existing task.

**Request Body** (all fields optional):
```json
{
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, butter",
  "priority": "medium",
  "tags": ["shopping"]
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, butter",
  "is_completed": false,
  "priority": "medium",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:30:00Z",
  "tags": ["shopping"]
}
```

**Errors**:
- 401: Unauthorized
- 404: Task not found or not owned by user
- 422: Validation error

---

### PATCH /api/tasks/{task_id}

Toggle task completion status.

**Request Body**: Empty

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "user_abc123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": true,
  "priority": "high",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:30:00Z",
  "tags": ["urgent", "shopping"]
}
```

**Errors**:
- 401: Unauthorized
- 404: Task not found or not owned by user

---

### DELETE /api/tasks/{task_id}

Delete a task.

**Response** (204 No Content): Empty body

**Errors**:
- 401: Unauthorized
- 404: Task not found or not owned by user

---

## Tag Endpoints (FastAPI - Protected)

All tag endpoints require `Authorization: Bearer <token>` header.

### GET /api/tags

List all tags for the authenticated user.

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| search | string | No | Filter tags by name |

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "user_abc123",
    "name": "urgent",
    "created_at": "2025-12-30T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": "user_abc123",
    "name": "shopping",
    "created_at": "2025-12-30T10:00:00Z"
  }
]
```

**Errors**:
- 401: Unauthorized

---

### POST /api/tags

Create a new tag.

**Request Body**:
```json
{
  "name": "personal"
}
```

**Response** (201 Created):
```json
{
  "id": 3,
  "user_id": "user_abc123",
  "name": "personal",
  "created_at": "2025-12-30T10:00:00Z"
}
```

**Errors**:
- 401: Unauthorized
- 422: Validation error

---

### DELETE /api/tags/{tag_id}

Delete a tag.

**Response** (204 No Content): Empty body

**Errors**:
- 401: Unauthorized
- 404: Tag not found or not owned by user

---

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Status Codes**:
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Not authorized to access resource |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 422 | Validation Error - Input validation failed |
| 500 | Internal Server Error |

## Authentication Flow

```
1. Frontend: User clicks "Sign In"
2. Frontend: POST /api/auth/signin with credentials
3. Backend: Validate credentials, return session token
4. Frontend: Store token in cookie (Better Auth)
5. Frontend: Make API call with Authorization header
6. Backend: Verify JWT token, extract user_id
7. Backend: Filter data by user_id, return response
```
