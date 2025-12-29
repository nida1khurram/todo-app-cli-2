# Context7 MCP Setup Instructions

## ✅ Status: INSTALLED & CONNECTED

Context7 MCP server is already installed and connected to your Claude Code!

```bash
context7: npx @upstash/context7-mcp - ✓ Connected
```

---

## Prerequisites

1. Node.js 18+ installed ✅
2. npm installed ✅
3. Claude Code CLI installed ✅

## Installation Steps (Already Completed)

### Step 1: Install Context7 MCP Server ✅

```bash
npm install -g @upstash/context7-mcp
```

### Step 2: Add Context7 to Claude Code ✅

```bash
claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp
```

### Step 3: Verify Installation ✅

```bash
claude mcp list
# Output: context7: npx @upstash/context7-mcp - ✓ Connected
```

---

## How to Use Context7

### Basic Usage

In your prompts, use the `use context7` command to fetch documentation:

```
use context7 for next.js 15
use context7 for fastapi 0.115
use context7 for react 19
use context7 for tailwindcss 3
```

### Project-Specific Libraries

For this Phase II full-stack todo app, use Context7 for these libraries:

#### Frontend Stack
```
use context7 for next.js 15
use context7 for react 19
use context7 for typescript 5
use context7 for tailwindcss 3
use context7 for better-auth 1
use context7 for zod 3
```

#### Backend Stack
```
use context7 for fastapi 0.115
use context7 for sqlmodel 0.0.22
use context7 for pydantic 2
use context7 for uvicorn 0.30
use context7 for python-jose
use context7 for passlib
```

#### Database
```
use context7 for postgresql 16
use context7 for asyncpg 0.29
```

### Example Prompts

**When building authentication:**
```
use context7 for better-auth and python-jose

Help me implement JWT authentication with Better Auth on the frontend
and python-jose on the backend.
```

**When creating database models:**
```
use context7 for sqlmodel and postgresql

Create SQLModel database models for User, Task, Tag, and TaskTag tables
with proper relationships and indexes.
```

**When building UI components:**
```
use context7 for next.js 15 and tailwindcss 3

Create a responsive task list component using Next.js App Router
and Tailwind CSS with mobile-first design.
```

**When creating API endpoints:**
```
use context7 for fastapi and pydantic

Create FastAPI endpoints for task CRUD operations with Pydantic schemas
for validation.
```

---

## MCP Server Management

### List All MCP Servers
```bash
claude mcp list
```

### Get Context7 Details
```bash
claude mcp get context7
```

### Remove Context7 (if needed)
```bash
claude mcp remove context7 -s local
```

### Re-add Context7
```bash
claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp
```

---

## Context7 Features

1. **Real-time Documentation**: Fetches latest docs from official sources
2. **Version-Specific**: Get docs for exact library versions
3. **Code Examples**: Includes practical code snippets
4. **Up-to-date**: Always current, no stale documentation
5. **Direct Integration**: Works seamlessly with Claude Code

---

## Troubleshooting

### Context7 Not Responding

If Context7 stops responding:

1. Check server status:
   ```bash
   claude mcp list
   ```

2. Restart Claude Code session

3. If still issues, reinstall:
   ```bash
   claude mcp remove context7 -s local
   npm install -g @upstash/context7-mcp --force
   claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp
   ```

### NPM Install Issues

If you get permission errors:

```bash
# Windows (run as administrator)
npm install -g @upstash/context7-mcp --force

# Alternative: use npx without global install
claude mcp add --transport stdio context7 -- npx -y @upstash/context7-mcp
```

### Verify Node.js Version

Context7 requires Node.js 18+:

```bash
node --version
# Should show v18.x.x or higher
```

---

## Best Practices

1. **Be Specific**: Always include version numbers
   - ✅ `use context7 for next.js 15`
   - ❌ `use context7 for next.js`

2. **Combine Related Libraries**: 
   ```
   use context7 for fastapi, sqlmodel, and pydantic
   ```

3. **Use in Planning Phase**:
   - Before `/sp.plan`: Get architecture docs
   - During implementation: Get specific API docs

4. **Context Switching**:
   - Frontend work: `use context7 for next.js, react, tailwindcss`
   - Backend work: `use context7 for fastapi, sqlmodel`
   - Auth work: `use context7 for better-auth, python-jose`

---

## Next Steps

Now that Context7 is installed:

1. ✅ Context7 MCP is connected
2. ⏭️ Run `/sp.plan` to create implementation plan
3. 💡 Use `use context7` commands during implementation
4. 🚀 Build Phase II full-stack todo app!

---

## Resources

- **Context7 GitHub**: https://github.com/upstash/context7
- **NPM Package**: https://www.npmjs.com/package/@upstash/context7-mcp
- **MCP Documentation**: https://code.claude.com/docs/en/mcp
- **Claude Code Docs**: https://code.claude.com/docs

---

## Project Configuration

This project has `.context7.json` with predefined contexts:

- **authentication**: JWT tokens, Better Auth, password hashing
- **database**: SQLModel ORM, PostgreSQL, async connections
- **frontend-ui**: Next.js App Router, React Components, Tailwind CSS
- **api**: FastAPI routes, Pydantic schemas, request/response models

---

**Installation Status**: ✅ COMPLETE
**Server Status**: ✅ CONNECTED
**Ready to Use**: ✅ YES

Start using Context7 in your prompts with `use context7 for <library>`!
