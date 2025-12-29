---
id: 001
title: Create Project Constitution
stage: constitution
date: 2025-12-28
surface: agent
model: claude-sonnet-4.5
feature: none
branch: add-claude-config
user: nida1khurram
command: manual
labels: ["constitution", "setup", "free-services", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: https://github.com/nida1khurram/todo-app-cli/pull/new/add-claude-config
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

User requested to create a complete constitution based on project-detail.md file for the Hackathon II "Evolution of Todo" project. Key requirements:
1. Read thoroughly the complete project-detail.md file
2. Write a complete constitution covering all 5 phases
3. Use all FREE API_KEY supported portals (zero-cost development)
4. Include available agents, skills, and commands from .claude/ directory

User follow-up: Asked to verify if all phases are included and if .claude/agents and .claude/skills are properly documented.

## Response snapshot

Created comprehensive constitution (Version 2.0.0) at `.specify/memory/constitution.md` with:

**15 Sections covering:**
1. Project Vision (5 phases, points, due dates)
2. Core Principles (SDD, AI-Native, Cloud-Native, Zero-Cost, Test-First, Security)
3. Free Services Strategy (Neon, Vercel, Groq, Oracle Cloud, Redpanda, etc.)
4. Phase I: In-Memory Python Console App (100 points)
5. Phase II: Full-Stack Web Application (150 points)
6. Phase III: AI-Powered Todo Chatbot (200 points)
7. Phase IV: Local Kubernetes Deployment (250 points)
8. Phase V: Advanced Cloud Deployment (300 points)
9. Bonus Features (+600 points)
10. Available Agents, Skills & Commands (NEW - added after user feedback)
11. Project Structure
12. Environment Variables
13. Quality Standards
14. Development Workflow
15. Timeline & Submission
16. Governance

**Free Services Recommended:**
- Neon DB (0.5GB free)
- Vercel (100GB bandwidth)
- Better Auth (open source)
- Groq API (free LLM - OpenAI compatible)
- Oracle Cloud OKE (ALWAYS FREE - 4 OCPUs, 24GB RAM)
- Redpanda Cloud (free serverless Kafka)
- GitHub Actions (2000 min/month)

**Agents Documented (5):**
- authentication-agent
- fastapi-backend-agent
- nextjs-frontend-agent
- python-console-agent
- spec-driven-dev

**Skills Documented (9):**
- python_project_structure
- cli_interface_design
- command_pattern_implementation
- data_validation
- in_memory_storage
- constitution_creation
- spec_writing
- spec_kit_structure
- claude_md_generation

**Commands Documented (13):**
- /sp.specify, /sp.plan, /sp.tasks, /sp.implement
- /sp.clarify, /sp.checklist, /sp.analyze
- /sp.adr, /sp.phr, /sp.constitution
- /sp.git.commit_pr, /sp.reverse-engineer, /sp.taskstoissues

## Outcome

- ✅ Impact: Complete project constitution created covering all 5 hackathon phases with free-tier services only
- 🧪 Tests: N/A (documentation)
- 📁 Files: 1 file created (.specify/memory/constitution.md - ~1500 lines)
- 🔁 Next prompts: /sp.specify for Phase I, create specs/ folder structure
- 🧠 Reflection: Initially missed documenting .claude/agents and .claude/skills - added Section 10 after user feedback

## Evaluation notes (flywheel)

- Failure modes observed: Did not initially include agents/skills documentation in constitution
- Graders run and results (PASS/FAIL): PASS after revision
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Auto-scan .claude/ directory and include in constitution by default
