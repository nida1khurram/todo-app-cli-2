# Todo App Evolution - Complete Project Constitution

> **Project Name:** Evolution of Todo - From CLI to Cloud-Native AI
> **Hackathon:** Hackathon II - Mastering Spec-Driven Development & Cloud Native AI
> **Version:** 2.0.0
> **Created:** 2025-12-28
> **Methodology:** Spec-Driven Development (SDD) with Claude Code
> **Total Points:** 1000 + 600 Bonus = 1600 Maximum

---

## Table of Contents

1. [Project Vision](#1-project-vision)
2. [Core Principles](#2-core-principles)
3. [Free Services Strategy](#3-free-services-strategy)
4. [Phase I: In-Memory Python Console App](#4-phase-i-in-memory-python-console-app)
5. [Phase II: Full-Stack Web Application](#5-phase-ii-full-stack-web-application)
6. [Phase III: AI-Powered Todo Chatbot](#6-phase-iii-ai-powered-todo-chatbot)
7. [Phase IV: Local Kubernetes Deployment](#7-phase-iv-local-kubernetes-deployment)
8. [Phase V: Advanced Cloud Deployment](#8-phase-v-advanced-cloud-deployment)
9. [Bonus Features](#9-bonus-features)
10. [Project Structure](#10-project-structure)
11. [Environment Variables](#11-environment-variables)
12. [Quality Standards](#12-quality-standards)
13. [Development Workflow](#13-development-workflow)
14. [Timeline & Submission](#14-timeline--submission)
15. [Governance](#15-governance)

---

## 1. Project Vision

### 1.1 Purpose
Build a production-grade Todo application that evolves through 5 phases, simulating real-world software evolution from a simple script to a Kubernetes-managed, event-driven, AI-powered distributed system.

### 1.2 Core Philosophy
- **Role:** Act as Product Architect, not syntax writer
- **Method:** Use AI (Claude Code) to build progressively complex software
- **Constraint:** No manual coding - refine specs until Claude generates correct output
- **Goal:** Master the Nine Pillars of AI-Driven Development

### 1.3 Learning Outcomes
- Spec-Driven Development using Claude Code and Spec-Kit Plus
- Reusable Intelligence: Agents, Skills, and Subagent Development
- Full-Stack Development with Next.js, FastAPI, SQLModel, Neon DB
- AI Agent Development using OpenAI Agents SDK and Official MCP SDK
- Cloud-Native Deployment with Docker, Kubernetes, Minikube, Helm Charts
- Event-Driven Architecture using Kafka and Dapr
- AIOps with kubectl-ai, kagent, and Claude Code

### 1.4 Phase Overview

| Phase | Description | Points | Due Date |
|-------|-------------|--------|----------|
| Phase I | In-Memory Python Console App | 100 | Dec 7, 2025 |
| Phase II | Full-Stack Web Application | 150 | Dec 14, 2025 |
| Phase III | AI-Powered Todo Chatbot | 200 | Dec 21, 2025 |
| Phase IV | Local Kubernetes Deployment | 250 | Jan 4, 2026 |
| Phase V | Advanced Cloud Deployment | 300 | Jan 18, 2026 |
| **TOTAL** | | **1000** | |
| **BONUS** | Reusable Intelligence, Blueprints, Urdu, Voice | **+600** | |

---

## 2. Core Principles

### I. Spec-Driven Development (SDD) - NON-NEGOTIABLE
```
Specify → Plan → Tasks → Implement
```
- **No code without spec:** Every implementation must trace back to a specification
- **AI-first:** Claude Code generates ALL implementation code
- **Constraint:** Manual coding is PROHIBITED
- **Process:** Write spec → Generate plan → Break into tasks → Implement via Claude Code
- **Judgment:** Process, prompts, and iterations will be reviewed

### II. AI-Native Architecture
- Use AI agents for development (Claude Code)
- Use AI agents for operations (kubectl-ai, kagent, Gordon)
- Implement conversational interfaces (ChatKit, MCP)
- Leverage MCP (Model Context Protocol) for tool integration

### III. Cloud-Native Design
- Containerization with Docker
- Orchestration with Kubernetes
- Event-driven architecture with Kafka/Dapr
- Stateless services for horizontal scalability

### IV. Zero-Cost Development - CRITICAL
- **All services MUST have free tiers**
- No paid API keys required for core functionality
- Use open-source alternatives where possible
- Cloud credits only for final deployment (Oracle Cloud preferred - always free)

### V. Test-First Quality
- TDD approach: Write tests → Fail → Implement → Pass
- Minimum 80% code coverage
- Integration tests for API endpoints
- E2E tests for critical user journeys

### VI. Security by Default
- No hardcoded secrets (use .env files)
- JWT token-based authentication
- Input validation on all endpoints
- CORS configuration for production

---

## 3. Free Services Strategy

### 3.1 Complete Free Tier Reference

| Service | URL | Free Tier Details | Use Case |
|---------|-----|-------------------|----------|
| **Neon DB** | neon.tech | 0.5GB storage, 190 compute hrs/month, 1 project | PostgreSQL Database |
| **Vercel** | vercel.com | 100GB bandwidth, serverless functions, auto HTTPS | Frontend Hosting |
| **Better Auth** | better-auth.com | Open source, unlimited | Authentication |
| **Groq** | console.groq.com | Free rate-limited access, OpenAI-compatible API | LLM (Development) |
| **Google Gemini** | aistudio.google.com | 60 requests/minute free | LLM Alternative |
| **Together AI** | together.ai | $25 free credits | LLM Alternative |
| **Oracle Cloud** | oracle.com/cloud/free | **ALWAYS FREE**: 4 OCPUs, 24GB RAM, OKE | Kubernetes (Phase V) |
| **Azure** | azure.microsoft.com/free | $200 credit for 30 days | Kubernetes Alternative |
| **Google Cloud** | cloud.google.com/free | $300 credit for 90 days | Kubernetes Alternative |
| **Redpanda Cloud** | redpanda.com/cloud | Free serverless tier, Kafka-compatible | Message Broker |
| **CloudKarafka** | cloudkarafka.com | "Developer Duck" free plan, 5 topics | Kafka Alternative |
| **Strimzi** | strimzi.io | Free (self-hosted in K8s) | Kafka in Kubernetes |
| **GitHub Actions** | github.com | 2000 min/month private, unlimited public | CI/CD |
| **Docker Desktop** | docker.com | Free for personal use | Containerization |

### 3.2 Recommended Free Stack

```
Phase I:   Python + UV + Rich + Pydantic (all free)
Phase II:  Neon DB + Vercel + Better Auth (all free)
Phase III: Groq API + MCP SDK (free - OpenAI-compatible)
Phase IV:  Docker + Minikube + Helm (all free)
Phase V:   Oracle Cloud OKE + Redpanda Cloud + Dapr (all free)
```

### 3.3 LLM Strategy for Phase III

**Problem:** OpenAI ChatKit requires OpenAI API (pay-as-you-go)

**Solution:** Use Groq API for development (FREE, OpenAI-compatible)

```python
# Groq is OpenAI-compatible - same code works!
from openai import OpenAI

# For Development (FREE)
client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# For Hackathon Submission (if ChatKit required)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

**Free LLM Models via Groq:**
- `llama-3.3-70b-versatile` (Best for chat)
- `mixtral-8x7b-32768` (Good for complex tasks)
- `gemma2-9b-it` (Fast responses)

---

## 4. Phase I: In-Memory Python Console App

### 4.1 Objective
Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.

### 4.2 Points: 100 | Due: Dec 7, 2025

### 4.3 Technology Stack

| Component | Technology | Cost |
|-----------|------------|------|
| Runtime | Python 3.13+ | Free |
| Package Manager | UV | Free |
| CLI Framework | Rich | Free |
| Data Validation | Pydantic v2 | Free |
| Storage | In-Memory (Dict) | Free |
| Dev Tool | Claude Code | Free |
| Spec Tool | Spec-Kit Plus | Free |

### 4.4 Required Features (Basic Level)

| Feature | Description | Acceptance Criteria |
|---------|-------------|---------------------|
| Add Task | Create new todo items | Title required (1-200 chars), description optional (max 1000 chars) |
| Delete Task | Remove tasks from list | By ID, confirm before deletion |
| Update Task | Modify existing task details | Update title and/or description |
| View Task List | Display all tasks | Show title, status, created date |
| Mark as Complete | Toggle task completion status | Visual indicator (✓/✗) |

### 4.5 Project Structure

```
src/
├── __init__.py
├── main.py                 # Entry point with Rich menu
├── models.py               # Pydantic Task model
├── storage.py              # In-memory storage class
└── commands/
    ├── __init__.py
    ├── add.py              # AddTaskCommand
    ├── delete.py           # DeleteTaskCommand
    ├── update.py           # UpdateTaskCommand
    ├── list.py             # ListTasksCommand
    └── complete.py         # CompleteTaskCommand
```

### 4.6 Data Models

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Task(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### 4.7 Storage Pattern

```python
class TaskStorage:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task: ...
    def get(self, task_id: int) -> Optional[Task]: ...
    def get_all(self) -> list[Task]: ...
    def update(self, task_id: int, **kwargs) -> Optional[Task]: ...
    def delete(self, task_id: int) -> bool: ...
```

### 4.8 Deliverables Checklist

- [ ] GitHub repository with source code
- [ ] Constitution file (`.specify/memory/constitution.md`)
- [ ] Specs history folder (`specs/` or `history/prompts/`)
- [ ] `/src` folder with Python source code
- [ ] `README.md` with setup instructions
- [ ] `CLAUDE.md` with Claude Code instructions
- [ ] Working console application demonstrating all 5 features
- [ ] `pyproject.toml` with UV configuration

### 4.9 Windows Users: WSL 2 Setup

```bash
# Install WSL 2
wsl --install

# Set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu-22.04
```

---

## 5. Phase II: Full-Stack Web Application

### 5.1 Objective
Transform the console app into a modern multi-user web application with persistent storage using Claude Code and Spec-Kit Plus.

### 5.2 Points: 150 | Due: Dec 14, 2025

### 5.3 Technology Stack

| Layer | Technology | Free Tier |
|-------|------------|-----------|
| Frontend | Next.js 16+ (App Router) | Free |
| Frontend Hosting | Vercel | 100GB bandwidth |
| Backend | Python FastAPI | Free |
| ORM | SQLModel | Free |
| Database | Neon Serverless PostgreSQL | 0.5GB, 190 compute hrs |
| Authentication | Better Auth | Open source |
| JWT | PyJWT / Better Auth JWT Plugin | Free |

### 5.4 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

### 5.5 Authentication Flow (Better Auth + FastAPI JWT)

```
1. User logs in on Frontend → Better Auth creates session + JWT token
2. Frontend makes API call → Includes JWT in Authorization: Bearer <token>
3. Backend receives request → Extracts token, verifies signature
4. Backend identifies user → Decodes token to get user_id
5. Backend filters data → Returns only tasks belonging to that user
```

### 5.6 JWT Integration

**Frontend (Better Auth Config):**
```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  database: { /* Neon connection */ },
  emailAndPassword: { enabled: true },
  jwt: {
    enabled: true,
    secret: process.env.BETTER_AUTH_SECRET
  }
})
```

**Backend (FastAPI JWT Verification):**
```python
# auth.py
from fastapi import Depends, HTTPException, Header
import jwt

async def verify_jwt(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(
            token,
            os.environ["BETTER_AUTH_SECRET"],
            algorithms=["HS256"]
        )
        return payload["sub"]  # user_id
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

### 5.7 Database Schema

```sql
-- Users table (managed by Better Auth)
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

### 5.8 Monorepo Structure

```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   └── database/
│       └── schema.md
├── frontend/
│   ├── CLAUDE.md
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── (auth)/
│   │   │   ├── signin/page.tsx
│   │   │   └── signup/page.tsx
│   │   └── dashboard/page.tsx
│   ├── components/
│   ├── lib/
│   │   ├── auth.ts
│   │   └── api.ts
│   └── package.json
├── backend/
│   ├── CLAUDE.md
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── routes/
│   │   └── tasks.py
│   └── pyproject.toml
├── CLAUDE.md
├── docker-compose.yml
└── README.md
```

### 5.9 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| User Isolation | Each user only sees their own tasks |
| Stateless Auth | Backend verifies JWT independently |
| Token Expiry | JWTs expire after 7 days |
| No Shared DB Session | Frontend/backend verify auth independently |
| HTTPS | Enforced in production (Vercel) |

### 5.10 Deliverables Checklist

- [ ] All Phase I deliverables
- [ ] `/frontend` - Next.js 16+ application
- [ ] `/backend` - FastAPI application
- [ ] Neon database integration
- [ ] Better Auth with JWT
- [ ] RESTful API with all 6 endpoints
- [ ] Responsive frontend interface
- [ ] Deployed on Vercel (frontend)
- [ ] Backend deployed (Vercel/Railway/Render)

---

## 6. Phase III: AI-Powered Todo Chatbot

### 6.1 Objective
Create an AI-powered chatbot interface for managing todos through natural language using MCP server architecture.

### 6.2 Points: 200 | Due: Dec 21, 2025

### 6.3 Technology Stack

| Component | Technology | Free Tier |
|-----------|------------|-----------|
| Chat UI | OpenAI ChatKit | Free (domain allowlist) |
| AI Framework | OpenAI Agents SDK | Pay-as-you-go* |
| **LLM (Dev)** | **Groq API** | **Free (rate limited)** |
| **LLM (Alt)** | **Google Gemini** | **Free (60 req/min)** |
| MCP Server | Official MCP SDK | Free |
| Database | Neon PostgreSQL | Free tier |
| Authentication | Better Auth | Free |

> *Use Groq for development (free), OpenAI for final submission if ChatKit requires it

### 6.4 Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │    Neon DB      │
│  (Frontend)     │     │  │  POST /api/{user_id}/chat              │  │     │  (PostgreSQL)   │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │  - tasks        │
│                 │     │                  ▼                           │     │  - conversations│
│                 │     │  ┌────────────────────────────────────────┐  │     │  - messages     │
│                 │◀────│  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Server                     │  │     │                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

### 6.5 Database Models (Phase III additions)

```sql
-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 6.6 Chat API Endpoint

**POST `/api/{user_id}/chat`**

Request:
```json
{
    "conversation_id": 123,      // Optional - creates new if not provided
    "message": "Add a task to buy groceries"
}
```

Response:
```json
{
    "conversation_id": 123,
    "response": "I've added 'Buy groceries' to your task list!",
    "tool_calls": [
        {"tool": "add_task", "args": {"title": "Buy groceries"}}
    ]
}
```

### 6.7 MCP Tools Specification

#### Tool: `add_task`
| Field | Value |
|-------|-------|
| Purpose | Create a new task |
| Parameters | `user_id` (string, required), `title` (string, required), `description` (string, optional) |
| Returns | `task_id`, `status`, `title` |
| Example Input | `{"user_id": "user123", "title": "Buy groceries", "description": "Milk, eggs, bread"}` |
| Example Output | `{"task_id": 5, "status": "created", "title": "Buy groceries"}` |

#### Tool: `list_tasks`
| Field | Value |
|-------|-------|
| Purpose | Retrieve tasks from the list |
| Parameters | `user_id` (string, required), `status` (string, optional: "all", "pending", "completed") |
| Returns | Array of task objects |
| Example Input | `{"user_id": "user123", "status": "pending"}` |
| Example Output | `[{"id": 1, "title": "Buy groceries", "completed": false}, ...]` |

#### Tool: `complete_task`
| Field | Value |
|-------|-------|
| Purpose | Mark a task as complete |
| Parameters | `user_id` (string, required), `task_id` (integer, required) |
| Returns | `task_id`, `status`, `title` |
| Example Input | `{"user_id": "user123", "task_id": 3}` |
| Example Output | `{"task_id": 3, "status": "completed", "title": "Call mom"}` |

#### Tool: `delete_task`
| Field | Value |
|-------|-------|
| Purpose | Remove a task from the list |
| Parameters | `user_id` (string, required), `task_id` (integer, required) |
| Returns | `task_id`, `status`, `title` |
| Example Input | `{"user_id": "user123", "task_id": 2}` |
| Example Output | `{"task_id": 2, "status": "deleted", "title": "Old task"}` |

#### Tool: `update_task`
| Field | Value |
|-------|-------|
| Purpose | Modify task title or description |
| Parameters | `user_id` (string, required), `task_id` (integer, required), `title` (string, optional), `description` (string, optional) |
| Returns | `task_id`, `status`, `title` |
| Example Input | `{"user_id": "user123", "task_id": 1, "title": "Buy groceries and fruits"}` |
| Example Output | `{"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}` |

### 6.8 Agent Behavior Specification

| Behavior | Description |
|----------|-------------|
| Task Creation | When user mentions adding/creating/remembering something, use `add_task` |
| Task Listing | When user asks to see/show/list tasks, use `list_tasks` with appropriate filter |
| Task Completion | When user says done/complete/finished, use `complete_task` |
| Task Deletion | When user says delete/remove/cancel, use `delete_task` |
| Task Update | When user says change/update/rename, use `update_task` |
| Confirmation | Always confirm actions with friendly response |
| Error Handling | Gracefully handle task not found and other errors |

### 6.9 Natural Language Commands

| User Says | Agent Should |
|-----------|--------------|
| "Add a task to buy groceries" | Call `add_task` with title "Buy groceries" |
| "Show me all my tasks" | Call `list_tasks` with status "all" |
| "What's pending?" | Call `list_tasks` with status "pending" |
| "Mark task 3 as complete" | Call `complete_task` with task_id 3 |
| "Delete the meeting task" | Call `list_tasks` first, then `delete_task` |
| "Change task 1 to 'Call mom tonight'" | Call `update_task` with new title |
| "I need to remember to pay bills" | Call `add_task` with title "Pay bills" |
| "What have I completed?" | Call `list_tasks` with status "completed" |

### 6.10 Conversation Flow (Stateless Request Cycle)

```
1. Receive user message
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client
9. Server holds NO state (ready for next request)
```

### 6.11 ChatKit Setup (OpenAI Domain Allowlist)

```
1. Deploy frontend to get production URL (e.g., https://your-app.vercel.app)
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Click "Add domain" and enter your frontend URL
4. Save and get domain key
5. Set environment variable: NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

### 6.12 Deliverables Checklist

- [ ] All Phase II deliverables
- [ ] `/frontend` with ChatKit-based UI
- [ ] `/backend` with FastAPI + Agents SDK + MCP
- [ ] `/specs` with agent and MCP tool specifications
- [ ] MCP server with 5 tools (add, list, complete, delete, update)
- [ ] Database migration scripts for conversations/messages
- [ ] Stateless chat endpoint
- [ ] Conversation persistence and resume after restart
- [ ] Natural language task management
- [ ] Helpful responses with action confirmations
- [ ] Graceful error handling

---

## 7. Phase IV: Local Kubernetes Deployment

### 7.1 Objective
Deploy the Todo Chatbot on a local Kubernetes cluster using Minikube and Helm Charts.

### 7.2 Points: 250 | Due: Jan 4, 2026

### 7.3 Technology Stack

| Component | Technology | Cost |
|-----------|------------|------|
| Containerization | Docker Desktop | Free |
| Docker AI | Gordon (Docker AI Agent) | Free |
| Local K8s | Minikube | Free |
| Package Manager | Helm | Free |
| AI DevOps | kubectl-ai | Free |
| AI DevOps | kagent | Free |

### 7.4 Requirements

- [ ] Containerize frontend and backend applications
- [ ] Use Docker AI Agent (Gordon) for AI-assisted Docker operations
- [ ] Create Helm charts for deployment
- [ ] Use kubectl-ai and kagent for AI-assisted K8s operations
- [ ] Deploy on Minikube locally

### 7.5 AIOps Commands

**Docker AI (Gordon):**
```bash
# Enable: Docker Desktop 4.53+ → Settings → Beta features → Toggle on
docker ai "What can you do?"
docker ai "Build a Dockerfile for my FastAPI backend"
docker ai "Optimize my container image size"
```

**kubectl-ai:**
```bash
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "scale the backend to handle more load"
kubectl-ai "check why the pods are failing"
kubectl-ai "create a service for the backend"
```

**kagent:**
```bash
kagent "analyze the cluster health"
kagent "optimize resource allocation"
kagent "troubleshoot networking issues"
```

### 7.6 Kubernetes Structure

```
k8s/
├── helm/
│   ├── todo-app/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── frontend-deployment.yaml
│   │       ├── frontend-service.yaml
│   │       ├── backend-deployment.yaml
│   │       ├── backend-service.yaml
│   │       ├── configmap.yaml
│   │       └── secrets.yaml
├── manifests/
│   ├── namespace.yaml
│   └── ingress.yaml
└── README.md
```

### 7.7 Dockerfile Templates

**Backend (FastAPI):**
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv sync
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend (Next.js):**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

### 7.8 Deliverables Checklist

- [ ] All Phase III deliverables
- [ ] Dockerfiles for frontend and backend
- [ ] `docker-compose.yml` for local development
- [ ] Helm charts in `/k8s/helm/`
- [ ] Working deployment on Minikube
- [ ] Documentation of kubectl-ai/kagent usage
- [ ] README with local setup instructions

---

## 8. Phase V: Advanced Cloud Deployment

### 8.1 Objective
Implement advanced features and deploy to production-grade Kubernetes on cloud with event-driven architecture.

### 8.2 Points: 300 | Due: Jan 18, 2026

### 8.3 Technology Stack

| Component | Technology | Free Tier |
|-----------|------------|-----------|
| **Kubernetes** | **Oracle Cloud (OKE)** | **Always free: 4 OCPUs, 24GB RAM** |
| K8s Alternative | Azure (AKS) | $200 credit / 30 days |
| K8s Alternative | Google Cloud (GKE) | $300 credit / 90 days |
| **Message Broker** | **Redpanda Cloud** | **Free serverless tier** |
| Broker Alternative | Strimzi (self-hosted) | Free in K8s |
| Broker Alternative | CloudKarafka | Free "Developer Duck" plan |
| Runtime | Dapr | Free |
| CI/CD | GitHub Actions | Free (2000 min/month) |

### 8.4 Part A: Advanced Features

#### Intermediate Level Features
| Feature | Description |
|---------|-------------|
| Priorities | Assign High/Medium/Low levels |
| Tags/Categories | Labels like work/home/personal |
| Search | Search by keyword in title/description |
| Filter | Filter by status, priority, or date |
| Sort | Sort by due date, priority, or alphabetically |

#### Advanced Level Features
| Feature | Description |
|---------|-------------|
| Recurring Tasks | Auto-reschedule (daily, weekly, monthly) |
| Due Dates & Reminders | Date/time picker with browser notifications |

### 8.5 Part B: Local Deployment
- Deploy to Minikube first
- Deploy Dapr on Minikube
- Use Full Dapr: Pub/Sub, State, Bindings (cron), Secrets, Service Invocation

### 8.6 Part C: Cloud Deployment
- Deploy to Oracle Cloud (OKE) / Azure (AKS) / Google Cloud (GKE)
- Deploy Dapr on cloud K8s
- Use Kafka on Redpanda Cloud
- Set up CI/CD pipeline with GitHub Actions
- Configure monitoring and logging

### 8.7 Kafka Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              KUBERNETES CLUSTER                                       │
│                                                                                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────────────────────────────┐ │
│  │  Frontend   │   │  Chat API   │   │              KAFKA CLUSTER                  │ │
│  │  Service    │──▶│  + MCP      │──▶│  ┌─────────────┐  ┌─────────────────────┐  │ │
│  └─────────────┘   │  Tools      │   │  │ task-events │  │ reminders           │  │ │
│                    └──────┬──────┘   │  └─────────────┘  └─────────────────────┘  │ │
│                           │          └──────────┬────────────────────┬────────────┘ │
│                           │                     │                    │              │
│                           ▼                     ▼                    ▼              │
│                    ┌─────────────┐   ┌─────────────────┐   ┌─────────────────┐     │
│                    │   Neon DB   │   │ Recurring Task  │   │  Notification   │     │
│                    │  (External) │   │    Service      │   │    Service      │     │
│                    └─────────────┘   └─────────────────┘   └─────────────────┘     │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.8 Kafka Topics

| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `task-events` | Chat API (MCP Tools) | Recurring Task Service, Audit Service | All task CRUD operations |
| `reminders` | Chat API (when due date set) | Notification Service | Scheduled reminder triggers |
| `task-updates` | Chat API | WebSocket Service | Real-time client sync |

### 8.9 Kafka Event Schemas

**Task Event:**
```json
{
    "event_type": "created|updated|completed|deleted",
    "task_id": 123,
    "task_data": { /* full task object */ },
    "user_id": "user123",
    "timestamp": "2025-01-15T10:30:00Z"
}
```

**Reminder Event:**
```json
{
    "task_id": 123,
    "title": "Buy groceries",
    "due_at": "2025-01-15T14:00:00Z",
    "remind_at": "2025-01-15T13:30:00Z",
    "user_id": "user123"
}
```

### 8.10 Dapr Integration

#### Dapr Building Blocks

| Block | Use Case |
|-------|----------|
| Pub/Sub | Kafka abstraction - publish/subscribe without Kafka client code |
| State Management | Conversation state storage |
| Service Invocation | Frontend → Backend with retries |
| Bindings | Cron triggers for scheduled reminders |
| Secrets Management | API keys, DB credentials |

#### Dapr Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              KUBERNETES CLUSTER                                       │
│                                                                                       │
│  ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐        │
│  │    Frontend Pod     │   │    Backend Pod      │   │  Notification Pod   │        │
│  │ ┌───────┐ ┌───────┐ │   │ ┌───────┐ ┌───────┐ │   │ ┌───────┐ ┌───────┐ │        │
│  │ │ Next  │ │ Dapr  │ │   │ │FastAPI│ │ Dapr  │ │   │ │Notif  │ │ Dapr  │ │        │
│  │ │  App  │◀┼▶Sidecar│ │   │ │+ MCP  │◀┼▶Sidecar│ │   │ │Service│◀┼▶Sidecar│ │        │
│  │ └───────┘ └───────┘ │   │ └───────┘ └───────┘ │   │ └───────┘ └───────┘ │        │
│  └──────────┬──────────┘   └──────────┬──────────┘   └──────────┬──────────┘        │
│             │                         │                         │                    │
│             └─────────────────────────┼─────────────────────────┘                    │
│                                       │                                              │
│                          ┌────────────▼────────────┐                                 │
│                          │    DAPR COMPONENTS      │                                 │
│                          │  ┌──────────────────┐   │                                 │
│                          │  │ pubsub.kafka     │───┼────▶ Redpanda Cloud             │
│                          │  ├──────────────────┤   │                                 │
│                          │  │ state.postgresql │───┼────▶ Neon DB                    │
│                          │  ├──────────────────┤   │                                 │
│                          │  │ bindings.cron    │   │  (Scheduled triggers)           │
│                          │  ├──────────────────┤   │                                 │
│                          │  │ secretstores.k8s │   │  (API keys, credentials)        │
│                          │  └──────────────────┘   │                                 │
│                          └─────────────────────────┘                                 │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

#### Dapr Pub/Sub Example (Without Kafka Library)

```python
import httpx

# Publish via Dapr sidecar (no kafka-python needed!)
await httpx.post(
    "http://localhost:3500/v1.0/publish/kafka-pubsub/task-events",
    json={"event_type": "created", "task_id": 1}
)
```

#### Dapr Component: Kafka Pub/Sub

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "xxx.cloud.redpanda.com:9092"
    - name: consumerGroup
      value: "todo-service"
    - name: authRequired
      value: "true"
    - name: saslUsername
      secretKeyRef:
        name: kafka-secrets
        key: username
    - name: saslPassword
      secretKeyRef:
        name: kafka-secrets
        key: password
```

### 8.11 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Frontend
        run: |
          cd frontend
          docker build -t todo-frontend:${{ github.sha }} .

      - name: Build Backend
        run: |
          cd backend
          docker build -t todo-backend:${{ github.sha }} .

      - name: Push to Registry
        run: |
          # Push to Oracle Cloud Container Registry / Docker Hub
          docker push todo-frontend:${{ github.sha }}
          docker push todo-backend:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          helm upgrade --install todo-app ./k8s/helm/todo-app \
            --set frontend.image.tag=${{ github.sha }} \
            --set backend.image.tag=${{ github.sha }}
```

### 8.12 Cloud Provider Setup

#### Oracle Cloud (RECOMMENDED - Always Free)
```bash
# Sign up: https://www.oracle.com/cloud/free/
# Always free includes:
# - 4 Arm-based Ampere A1 cores
# - 24 GB memory
# - OKE (Oracle Kubernetes Engine)
# - No credit card charge after trial!

# Create OKE cluster
oci ce cluster create \
  --compartment-id <compartment-id> \
  --name todo-cluster \
  --kubernetes-version v1.28.2

# Configure kubectl
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-id> \
  --file $HOME/.kube/config
```

#### Redpanda Cloud Setup
```bash
# Sign up: https://redpanda.com/cloud
# Create Serverless cluster (free tier)
# Create topics: task-events, reminders, task-updates

# Connection details for Dapr component:
REDPANDA_BROKERS="xxx.cloud.redpanda.com:9092"
REDPANDA_USERNAME="xxx"
REDPANDA_PASSWORD="xxx"
```

### 8.13 Deliverables Checklist

- [ ] All Phase IV deliverables
- [ ] Intermediate features (Priorities, Tags, Search, Filter, Sort)
- [ ] Advanced features (Recurring Tasks, Due Dates, Reminders)
- [ ] Kafka integration with event schemas
- [ ] Dapr components (Pub/Sub, State, Bindings, Secrets)
- [ ] Deployment on Oracle Cloud OKE (or Azure/GCP)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Monitoring and logging configured
- [ ] Production-ready documentation

---

## 9. Bonus Features

### 9.1 Points Summary

| Bonus Feature | Points |
|---------------|--------|
| Reusable Intelligence (Subagents/Skills) | +200 |
| Cloud-Native Blueprints via Agent Skills | +200 |
| Multi-language Support (Urdu) | +100 |
| Voice Commands | +200 |
| **TOTAL BONUS** | **+600** |

### 9.2 Reusable Intelligence (+200)

Create Claude Code subagents and agent skills that can be reused:
- Task management agent
- Authentication agent
- Deployment agent
- Custom skills for common operations

### 9.3 Cloud-Native Blueprints (+200)

Create Agent Skills for infrastructure automation:
- Kubernetes deployment blueprints
- Helm chart generation skills
- Dapr component templates
- CI/CD pipeline templates

### 9.4 Multi-language Support - Urdu (+100)

Add Urdu language support to the chatbot:
- Urdu task creation: "کام شامل کریں: گروسری خریدنا"
- Urdu responses
- RTL UI support

### 9.5 Voice Commands (+200)

Add voice input for todo commands:
- Speech-to-text integration
- Voice command recognition
- "Add task to buy groceries" via voice

---

## 10. Available Agents, Skills & Commands

### 10.1 Claude Code Agents (`.claude/agents/`)

| Agent | File | Description | Use When |
|-------|------|-------------|----------|
| **authentication-agent** | `authentication-agent.md` | Authentication & authorization expert | Better Auth setup, JWT handling, protected routes, login/signup flows, 401/403 debugging |
| **fastapi-backend-agent** | `fastapi-backend-agent.md` | FastAPI backend architect | CRUD APIs, SQLModel models, Neon PostgreSQL, JWT middleware, API endpoints |
| **nextjs-frontend-agent** | `nextjs-frontend-agent.md` | Next.js 16+ frontend developer | App Router pages, React Server Components, Tailwind CSS, Better Auth integration |
| **python-console-agent** | `python-console-agent.md` | Python CLI application developer | Terminal apps with Rich, UV package management, Pydantic validation, Command pattern |
| **spec-driven-dev** | `spec-driven-dev.md` | Spec-Kit Plus methodology expert | Constitution files, feature specs, API specs, project specification structure |

#### Agent Usage by Phase

| Phase | Primary Agent(s) |
|-------|------------------|
| Phase I | `python-console-agent`, `spec-driven-dev` |
| Phase II | `fastapi-backend-agent`, `nextjs-frontend-agent`, `authentication-agent` |
| Phase III | `fastapi-backend-agent`, `nextjs-frontend-agent`, `authentication-agent` |
| Phase IV | All agents + AIOps tools |
| Phase V | All agents + AIOps tools |

### 10.2 Claude Code Skills (`.claude/skills/`)

| Skill | Description | Phase |
|-------|-------------|-------|
| **python_project_structure** | Set up Python 3.13+ project with UV, pyproject.toml, src/ directory, tests/ | Phase I |
| **cli_interface_design** | Create CLIs using Rich library (Console, Table, Prompt, menus) | Phase I |
| **command_pattern_implementation** | Implement Command pattern with abstract base class and dependency injection | Phase I |
| **data_validation** | Pydantic BaseModel validation with Field constraints and custom validators | Phase I, II, III |
| **in_memory_storage** | Type-safe in-memory storage with CRUD operations and auto-incrementing IDs | Phase I |
| **constitution_creation** | Create constitution.md with vision, principles, constraints, tech stack | All Phases |
| **spec_writing** | Write feature specs with user stories, acceptance criteria, constraints | All Phases |
| **spec_kit_structure** | Initialize Spec-Kit Plus folder structure for spec-driven development | All Phases |
| **claude_md_generation** | Generate CLAUDE.md files with project context for AI assistants | All Phases |

#### Skill Usage by Phase

| Phase | Skills to Use |
|-------|---------------|
| Phase I | `python_project_structure`, `cli_interface_design`, `command_pattern_implementation`, `data_validation`, `in_memory_storage` |
| Phase II | `data_validation`, `spec_writing`, `spec_kit_structure` |
| Phase III | `data_validation`, `spec_writing` |
| Phase IV-V | `spec_writing`, `claude_md_generation` |

### 10.3 Spec-Kit Plus Commands (`.claude/commands/`)

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/sp.specify` | Create feature specification from description | Start of any feature |
| `/sp.plan` | Execute implementation planning workflow | After specification |
| `/sp.tasks` | Generate actionable tasks.md from design artifacts | After planning |
| `/sp.implement` | Execute implementation plan from tasks.md | During development |
| `/sp.clarify` | Identify underspecified areas with clarification questions | When requirements unclear |
| `/sp.checklist` | Generate custom checklist for features | Before implementation |
| `/sp.analyze` | Cross-artifact consistency and quality analysis | After task generation |
| `/sp.adr` | Create Architecture Decision Records | For significant decisions |
| `/sp.phr` | Record Prompt History Record for traceability | After every interaction |
| `/sp.constitution` | Create or update project constitution | Project setup |
| `/sp.git.commit_pr` | Autonomous Git workflow for commits and PRs | Code complete |
| `/sp.reverse-engineer` | Reverse engineer codebase into SDD artifacts | Legacy code |
| `/sp.taskstoissues` | Convert tasks to GitHub issues | Project management |

#### Command Workflow by Phase

```
Phase I Workflow:
1. /sp.constitution    → Define project principles (DONE)
2. /sp.specify         → Create Phase I spec
3. /sp.plan            → Design console app architecture
4. /sp.tasks           → Break into implementable tasks
5. /sp.implement       → Build using python-console-agent
6. /sp.phr             → Record prompt history
7. /sp.git.commit_pr   → Commit and create PR

Phase II-V Workflow:
Same pattern with phase-specific agents and specs
```

### 10.4 Pre-Action Checklist (MANDATORY)

Before running ANY action, Claude Code MUST:

```
1. ✅ Check .claude/agents/ for available agents
2. ✅ Check .claude/skills/ for available skills
3. ✅ Check .claude/commands/ for available commands
4. ✅ Select appropriate agent/skill for the task
5. ✅ Update CLAUDE.md if new agents/skills added
```

---

## 11. Project Structure

```
todo-app-evolution/
├── .specify/                          # Spec-Kit Plus
│   ├── memory/
│   │   └── constitution.md            # THIS FILE
│   ├── templates/
│   └── scripts/
├── .claude/                           # Claude Code config
│   ├── agents/
│   │   ├── authentication-agent.md
│   │   ├── fastapi-backend-agent.md
│   │   ├── nextjs-frontend-agent.md
│   │   ├── python-console-agent.md
│   │   └── spec-driven-dev.md
│   ├── skills/
│   │   ├── cli_interface_design/
│   │   ├── data_validation/
│   │   └── ...
│   └── commands/
│       ├── sp.specify.md
│       ├── sp.plan.md
│       ├── sp.tasks.md
│       └── ...
├── specs/                             # Feature specifications
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   ├── api/
│   │   ├── rest-endpoints.md
│   │   └── mcp-tools.md
│   └── database/
│       └── schema.md
├── history/                           # Development history
│   ├── prompts/                       # PHRs
│   │   ├── constitution/
│   │   ├── general/
│   │   └── <feature-name>/
│   └── adr/                           # Architecture decisions
├── src/                               # Phase I: Console app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   └── commands/
│       ├── add.py
│       ├── delete.py
│       ├── update.py
│       ├── list.py
│       └── complete.py
├── frontend/                          # Phase II+: Next.js
│   ├── CLAUDE.md
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── (auth)/
│   │   │   ├── signin/page.tsx
│   │   │   └── signup/page.tsx
│   │   ├── dashboard/page.tsx
│   │   └── chat/page.tsx              # Phase III
│   ├── components/
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── ChatInterface.tsx          # Phase III
│   ├── lib/
│   │   ├── auth.ts
│   │   └── api.ts
│   └── package.json
├── backend/                           # Phase II+: FastAPI
│   ├── CLAUDE.md
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── routes/
│   │   ├── tasks.py
│   │   └── chat.py                    # Phase III
│   ├── mcp/                           # Phase III
│   │   ├── server.py
│   │   └── tools/
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── complete_task.py
│   │       ├── delete_task.py
│   │       └── update_task.py
│   └── pyproject.toml
├── k8s/                               # Phase IV+: Kubernetes
│   ├── helm/
│   │   └── todo-app/
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       └── templates/
│   ├── dapr/                          # Phase V
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   └── secrets.yaml
│   └── manifests/
├── .github/
│   └── workflows/
│       └── deploy.yml                 # Phase V
├── docker-compose.yml
├── Dockerfile.frontend
├── Dockerfile.backend
├── CLAUDE.md
├── AGENTS.md
├── README.md
├── pyproject.toml
└── .env.example
```

---

## 11. Environment Variables

```bash
# .env.example - Copy to .env and fill values

# ============================================
# PHASE I: Console App (No env needed)
# ============================================

# ============================================
# PHASE II: Full-Stack Web Application
# ============================================

# Neon Database (FREE - neon.tech)
DATABASE_URL="postgresql://user:pass@ep-xxx.region.aws.neon.tech/dbname?sslmode=require"

# Better Auth (Self-hosted - FREE)
BETTER_AUTH_SECRET="your-secret-key-minimum-32-characters-long"
BETTER_AUTH_URL="http://localhost:3000"
NEXTAUTH_URL="http://localhost:3000"

# ============================================
# PHASE III: AI Chatbot
# ============================================

# Option 1: OpenAI (Required for ChatKit submission)
OPENAI_API_KEY="sk-xxxxxxxxxxxx"

# Option 2: Groq (FREE - RECOMMENDED FOR DEVELOPMENT)
GROQ_API_KEY="gsk_xxxxxxxxxxxx"
LLM_BASE_URL="https://api.groq.com/openai/v1"
LLM_MODEL="llama-3.3-70b-versatile"

# Option 3: Google Gemini (FREE - 60 req/min)
GOOGLE_API_KEY="AIza_xxxxxxxxxxxx"

# Option 4: Together AI (FREE $25 credits)
TOGETHER_API_KEY="xxxxxxxxxxxx"

# ChatKit Domain Key (after Vercel deployment)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY="your-domain-key"

# ============================================
# PHASE IV: Local Kubernetes (Minikube)
# ============================================

# No additional env vars - uses K8s secrets

# ============================================
# PHASE V: Cloud Deployment
# ============================================

# Redpanda Cloud (FREE Serverless Kafka)
KAFKA_BROKERS="xxx.cloud.redpanda.com:9092"
KAFKA_USERNAME="xxx"
KAFKA_PASSWORD="xxx"
KAFKA_SECURITY_PROTOCOL="SASL_SSL"
KAFKA_SASL_MECHANISM="SCRAM-SHA-256"

# Oracle Cloud (ALWAYS FREE)
OCI_TENANCY_OCID="ocid1.tenancy.oc1..xxx"
OCI_USER_OCID="ocid1.user.oc1..xxx"
OCI_FINGERPRINT="xx:xx:xx:xx"
OCI_REGION="us-ashburn-1"
OCI_PRIVATE_KEY_PATH="~/.oci/oci_api_key.pem"

# Alternative: Azure (AKS)
AZURE_SUBSCRIPTION_ID="xxx"
AZURE_RESOURCE_GROUP="todo-app-rg"
AZURE_CLUSTER_NAME="todo-cluster"

# Alternative: Google Cloud (GKE)
GCP_PROJECT_ID="xxx"
GCP_REGION="us-central1"
GCP_CLUSTER_NAME="todo-cluster"
```

---

## 12. Quality Standards

### 12.1 Code Quality

| Standard | Requirement |
|----------|-------------|
| Type Safety | Full type hints (Python), strict TypeScript |
| Validation | Pydantic models for all data |
| Error Handling | Graceful errors with user-friendly messages |
| Documentation | Docstrings for all public functions |
| Linting | Ruff for Python, ESLint for TypeScript |
| Formatting | Black for Python, Prettier for TypeScript |

### 12.2 Testing Requirements

| Test Type | Coverage |
|-----------|----------|
| Unit Tests | Business logic, models, utilities |
| Integration Tests | API endpoints, database operations |
| E2E Tests | Critical user journeys |
| Minimum Coverage | 80% |

### 12.3 Security Checklist

- [ ] No hardcoded secrets (use .env)
- [ ] JWT token expiration (7 days max)
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention via ORM
- [ ] XSS prevention in frontend
- [ ] CORS configuration for production
- [ ] HTTPS in production
- [ ] Rate limiting on API endpoints

### 12.4 Performance Targets

| Metric | Target |
|--------|--------|
| API Response Time | < 500ms (p95) |
| Frontend LCP | < 2.5s |
| Database Queries | < 100ms |
| Container Startup | < 30s |
| Chat Response | < 3s |

---

## 13. Development Workflow

### 13.1 Spec-Driven Loop (MANDATORY)

```
1. /sp.specify  → Define WHAT to build (requirements)
2. /sp.plan     → Design HOW to build (architecture)
3. /sp.tasks    → Break into atomic tasks
4. /sp.implement → Execute via Claude Code
5. /sp.phr      → Record prompt history
```

### 13.2 Git Workflow

- Main branch: `main`
- Feature branches: `feature/<phase>-<feature>`
- PR required for all changes
- Use `/sp.git.commit_pr` for commits

### 13.3 Claude Code Rules

1. Always check agents/skills before actions (`.claude/agents/`, `.claude/skills/`)
2. Create PHR for every significant interaction
3. Suggest ADR for architectural decisions
4. Reference specs in all implementations
5. Update CLAUDE.md when adding new agents/skills

### 13.4 Before Every Action

```
1. Check .claude/agents/ for available agents
2. Check .claude/skills/ for available skills
3. Check .claude/commands/ for available commands
4. Update CLAUDE.md if new ones added
```

---

## 14. Timeline & Submission

### 14.1 Schedule

| Milestone | Date | Description |
|-----------|------|-------------|
| Hackathon Start | Mon, Dec 1, 2025 | Documentation released |
| Phase I Due | Sun, Dec 7, 2025 | Console app checkpoint |
| Phase II Due | Sun, Dec 14, 2025 | Web app checkpoint |
| Phase III Due | Sun, Dec 21, 2025 | Chatbot checkpoint |
| Phase IV Due | Sun, Jan 4, 2026 | Local K8s checkpoint |
| Final Submission | Sun, Jan 18, 2026 | All phases complete |
| Live Presentations | Sundays 8:00 PM | Top submissions present |

### 14.2 Submission Requirements

For each phase, submit via: https://forms.gle/KMKEKaFUD6ZX4UtY8

- [ ] Public GitHub Repository Link
- [ ] Published App Link (Vercel)
- [ ] Demo Video Link (max 90 seconds - judges only watch first 90s)
- [ ] WhatsApp number (for presentation invitation)

### 14.3 Repository Requirements

- [ ] All source code for completed phases
- [ ] `/specs` folder with all specification files
- [ ] `CLAUDE.md` with Claude Code instructions
- [ ] `README.md` with comprehensive documentation
- [ ] Clear folder structure for each phase
- [ ] Constitution file (`.specify/memory/constitution.md`)

### 14.4 Live Presentations

- Time: 8:00 PM on Sundays
- Zoom: https://us06web.zoom.us/j/84976847088?pwd=Z7t7NaeXwVmmR5fysCv7NiMbfbhIda.1
- Meeting ID: 849 7684 7088
- Passcode: 305850
- Top submissions invited via WhatsApp

---

## 15. Governance

### 15.1 Constitution Authority

This constitution is the **authoritative source** for all project decisions. It supersedes all other practices.

### 15.2 Amendment Process

Any changes require:
1. Documentation of the proposed change
2. Impact analysis
3. Update to this file with version increment
4. ADR if architecturally significant

### 15.3 Compliance

All PRs and code reviews must verify compliance with this constitution.

### 15.4 Hierarchy

```
Constitution > Specify > Plan > Tasks
```

If conflict arises between spec files, this hierarchy applies.

---

## Quick Reference: Free Services

| Service | URL | What's Free |
|---------|-----|-------------|
| Neon DB | neon.tech | 0.5GB, 190 compute hrs |
| Vercel | vercel.com | 100GB bandwidth |
| Better Auth | better-auth.com | Open source, unlimited |
| Groq | console.groq.com | Free LLM API |
| Gemini | aistudio.google.com | 60 req/min |
| Oracle Cloud | oracle.com/cloud/free | **4 OCPUs, 24GB RAM (FOREVER)** |
| Redpanda | redpanda.com/cloud | Free serverless Kafka |
| GitHub Actions | github.com | 2000 min/month |
| Docker Desktop | docker.com | Free personal use |
| Minikube | minikube.sigs.k8s.io | Free |
| Helm | helm.sh | Free |
| Dapr | dapr.io | Free |

---

**Version**: 2.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28

Good luck, and may your specs be clear and your code be clean!
— The Panaversity, PIAIC, and GIAIC Teams
