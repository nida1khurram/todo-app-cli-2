# Context7 Quick Reference

## ✅ Status
- **Installed**: ✅ `@upstash/context7-mcp@1.0.26`
- **Connected**: ✅ `claude mcp list` shows connected
- **Ready**: ✅ Use in prompts now

---

## Quick Commands

### Use Context7 in Prompts

```
use context7 for <library> <version>
```

### Common Usage Patterns

```
# Single library
use context7 for next.js 15

# Multiple libraries
use context7 for fastapi, sqlmodel, and pydantic

# With specific versions
use context7 for react 19 and typescript 5
```

---

## Phase II Project Libraries

### Frontend (use together)
```
use context7 for next.js 15, react 19, and tailwindcss 3
use context7 for better-auth 1 and zod 3
```

### Backend (use together)
```
use context7 for fastapi 0.115, sqlmodel, and pydantic 2
use context7 for uvicorn, python-jose, and passlib
```

### Database
```
use context7 for postgresql 16 and asyncpg
```

---

## By Development Phase

### 🔐 Authentication Implementation
```
use context7 for better-auth 1 and python-jose

Create JWT authentication system with Better Auth frontend
and python-jose backend verification.
```

### 💾 Database Models
```
use context7 for sqlmodel and postgresql

Create User, Task, Tag, TaskTag models with relationships
and proper indexes.
```

### 🎨 UI Components
```
use context7 for next.js 15, react 19, and tailwindcss 3

Build responsive task list with App Router server and client
components using Tailwind CSS.
```

### 🔌 API Endpoints
```
use context7 for fastapi and pydantic

Create RESTful CRUD endpoints with request/response validation.
```

---

## Example Prompts

### Creating Auth System
```
use context7 for better-auth 1 and python-jose 3

I need to:
1. Set up Better Auth with email/password on Next.js frontend
2. Create JWT verification middleware for FastAPI backend
3. Implement user isolation for all task endpoints

Show me the complete implementation.
```

### Building Database Layer
```
use context7 for sqlmodel 0.0.22 and postgresql 16

Create database models for:
- User (id, email, password_hash, created_at)
- Task (id, user_id, title, description, status, priority, created_at, updated_at)
- Tag (id, user_id, name)
- TaskTag (task_id, tag_id) junction table

Include proper foreign keys, indexes, and relationships.
```

### Building UI
```
use context7 for next.js 15, react 19, and tailwindcss 3

Create:
1. Task list component with server-side data fetching
2. Task form component (client) with validation
3. Priority badges with colored styling (red/yellow/green)
4. Tag display with multi-select filtering

Use App Router patterns and Tailwind for responsive design.
```

---

## Verification

### Check Context7 Status
```bash
claude mcp list
# Should show: ✓ Connected
```

### Test Context7
In Claude Code, type:
```
use context7 for fastapi

What's the latest way to create async endpoints?
```

---

## Management Commands

```bash
# List all MCP servers
claude mcp list

# Get Context7 details
claude mcp get context7

# Remove Context7
claude mcp remove context7 -s local

# Re-add Context7
claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp
```

---

## Tips

✅ **DO:**
- Include version numbers
- Combine related libraries
- Use before planning and implementation
- Be specific about what you need

❌ **DON'T:**
- Use without version numbers
- Request too many unrelated libraries
- Forget to use when working with new APIs

---

## Next Steps

1. ✅ Context7 is ready
2. 📝 Run `/sp.plan` for Phase II
3. 💻 Use `use context7` during implementation
4. 🚀 Build full-stack todo app!

---

**Quick Test**: Type in Claude Code:
```
use context7 for next.js 15

How do I create a server component that fetches data?
```

If you get documentation back, Context7 is working! 🎉
