# Context7 MCP Setup Instructions

## Prerequisites

1. Node.js 18+ installed
2. npm installed
3. Claude Desktop installed

## Installation Steps

### Step 1: Install Context7 MCP Server

```bash
npm install -g @context7/mcp-server
```

### Step 2: Create Claude Desktop Config

**File Location**: `%APPDATA%\Claude\claude_desktop_config.json`

**Full Path**: `C:\Users\YOUR_USERNAME\AppData\Roaming\Claude\claude_desktop_config.json`

**Content**:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"],
      "env": {
        "CONTEXT7_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop application for changes to take effect.

### Step 4: Verify Installation

In Claude Desktop, type:
```
@context7/help
```

If successful, you'll see Context7 commands.

## Phase II Project Libraries

### Frontend Stack (Next.js 15+)

Add these libraries to Context7:

```bash
@context7/add next@15
@context7/add react@19
@context7/add typescript@5
@context7/add tailwindcss@3
@context7/add better-auth@1
@context7/add zod@3
```

**Additional Frontend Libraries**:
- `@types/node` - TypeScript types for Node.js
- `@types/react` - TypeScript types for React
- `@types/react-dom` - TypeScript types for React DOM
- `autoprefixer` - PostCSS plugin for Tailwind
- `postcss` - CSS transformations

### Backend Stack (FastAPI + Python)

Add these libraries to Context7:

```bash
@context7/add fastapi@0.115
@context7/add sqlmodel@0.0.22
@context7/add pydantic@2
@context7/add python-jose
@context7/add passlib
@context7/add uvicorn@0.30
@context7/add asyncpg@0.29
```

**Additional Backend Libraries**:
- `python-multipart` - Form data parsing
- `bcrypt` - Password hashing
- `cryptography` - JWT encryption

### Database

```bash
@context7/add postgresql@16
```

## Context Switching

### Available Contexts

1. **authentication** - User auth, JWT, Better Auth
2. **database** - SQLModel, PostgreSQL, async queries
3. **frontend-ui** - Next.js, React components, Tailwind
4. **api** - FastAPI endpoints, Pydantic schemas

### Usage Examples

```bash
# Switch to authentication context
@context7/use authentication

# Work with auth-related code...

# Switch to frontend context
@context7/use frontend-ui

# Work with UI components...

# Switch to API context
@context7/use api

# Work with backend endpoints...
```

## Context7 Common Commands

| Command | Description |
|---------|-------------|
| `@context7/add <lib>` | Add library to context |
| `@context7/remove <lib>` | Remove library from context |
| `@context7/list` | Show all available contexts |
| `@context7/current` | Show current active context |
| `@context7/use <name>` | Switch to specific context |
| `@context7/help` | Show all commands |

## Project-Specific Setup

This project has `.context7.json` configuration file with predefined contexts:

- **authentication**: JWT tokens, Better Auth, password hashing
- **database**: SQLModel ORM, PostgreSQL, async connections
- **frontend-ui**: Next.js App Router, React Server/Client Components, Tailwind CSS
- **api**: FastAPI routes, Pydantic schemas, request/response models

## Troubleshooting

### Context7 Not Found

If `@context7/add` doesn't work:

1. Verify Context7 MCP is installed:
   ```bash
   npm list -g @context7/mcp-server
   ```

2. Check Claude Desktop config exists:
   ```bash
   cat %APPDATA%\Claude\claude_desktop_config.json
   ```

3. Restart Claude Desktop completely

### API Key Issues

If you need a Context7 API key:

1. Visit Context7 website
2. Create an account
3. Generate API key
4. Add to `claude_desktop_config.json`

### Permission Errors

If you get permission errors:

```bash
# Run as administrator
npm install -g @context7/mcp-server --force
```

## Best Practices

1. **Use specific contexts** for different tasks:
   - Use `authentication` when working on auth
   - Use `frontend-ui` for UI components
   - Use `api` for backend endpoints
   - Use `database` for models and queries

2. **Add libraries incrementally**:
   - Start with core libraries
   - Add additional libraries as needed
   - Keep contexts focused and small

3. **Version pinning**:
   - Use specific versions in production
   - Use `@latest` for experiments

4. **Context switching**:
   - Switch contexts before starting new tasks
   - Keeps Claude focused on relevant docs

## Next Steps

After setup:

1. Run `/sp.plan` to create implementation plan
2. Use Context7 contexts during implementation
3. Switch contexts as you work on different parts

## Support

- Context7 Documentation: https://context7.dev/docs
- Claude MCP Guide: https://docs.anthropic.com/mcp
- Project Issues: Open issue in project repository
