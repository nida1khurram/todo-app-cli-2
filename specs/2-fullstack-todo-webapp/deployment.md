# Deployment Guide

## Overview

This guide covers deploying the Full-Stack Todo Web Application with:
- **Frontend**: Vercel (Next.js)
- **Backend**: Railway or Render (FastAPI)
- **Database**: Neon PostgreSQL (already configured)

---

## Prerequisites

1. GitHub repository with the codebase
2. Neon PostgreSQL database (already set up)
3. Accounts on:
   - [Vercel](https://vercel.com) for frontend
   - [Railway](https://railway.app) or [Render](https://render.com) for backend

---

## Backend Deployment (Railway)

### Option A: Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Service**
   - Set root directory: `backend`
   - Railway auto-detects Python/FastAPI

4. **Set Environment Variables**
   ```
   DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require
   JWT_SECRET=your-secret-key
   JWT_EXPIRATION_DAYS=7
   CORS_ORIGINS=https://your-frontend.vercel.app
   PYTHON_ENV=production
   ```

5. **Configure Start Command**
   ```
   uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

6. **Deploy**
   - Railway will auto-deploy on push to main branch
   - Note the deployed URL (e.g., `https://your-app.railway.app`)

### Option B: Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign in with GitHub

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   ```
   Name: todo-api
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   - Same as Railway above

5. **Deploy**
   - Click "Create Web Service"
   - Note the deployed URL

---

## Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository

3. **Configure Project**
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   ```

4. **Set Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   BETTER_AUTH_SECRET=your-auth-secret
   BETTER_AUTH_URL=https://your-frontend.vercel.app
   ```

5. **Deploy**
   - Click "Deploy"
   - Vercel will auto-deploy on push to main branch

---

## Post-Deployment Checklist

### 1. Update CORS Origins
Update backend `CORS_ORIGINS` to include your Vercel domain:
```
CORS_ORIGINS=https://your-app.vercel.app
```

### 2. Test Authentication Flow
- [ ] Register new user
- [ ] Login with credentials
- [ ] Verify JWT token in requests
- [ ] Test logout

### 3. Test API Endpoints
- [ ] Create task
- [ ] List tasks
- [ ] Update task
- [ ] Delete task
- [ ] Filter/search tasks

### 4. Verify Database
- [ ] Check Neon dashboard for connections
- [ ] Verify tables created correctly
- [ ] Test data persistence

---

## Environment Variables Reference

### Backend (Railway/Render)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql+asyncpg://...` |
| `JWT_SECRET` | Secret for JWT signing | Random 32+ char string |
| `JWT_EXPIRATION_DAYS` | Token expiration | `7` |
| `CORS_ORIGINS` | Allowed frontend origins | `https://app.vercel.app` |
| `PYTHON_ENV` | Environment mode | `production` |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://api.railway.app` |
| `BETTER_AUTH_SECRET` | Auth secret key | Random 32+ char string |
| `BETTER_AUTH_URL` | Frontend URL | `https://app.vercel.app` |

---

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure `CORS_ORIGINS` includes your frontend URL
   - Check for trailing slashes

2. **Database Connection Failed**
   - Verify `DATABASE_URL` format uses `postgresql+asyncpg://`
   - Ensure `ssl=require` is in connection string

3. **JWT Errors**
   - Ensure `JWT_SECRET` is the same across deployments
   - Check token expiration settings

4. **Build Failures**
   - Check Python version (3.11+)
   - Check Node version (18+)
   - Verify all dependencies in requirements.txt/package.json

---

## Continuous Deployment

Both Vercel and Railway support automatic deployments:

1. **Push to main branch** → Auto-deploy
2. **Pull request** → Preview deployment (Vercel)

### Branch Protection (Recommended)
- Enable branch protection on `main`
- Require PR reviews before merge
- Run tests in CI before deploy

---

## Monitoring

### Railway
- View logs in dashboard
- Set up alerts for errors

### Vercel
- View function logs
- Analytics dashboard for performance

### Neon
- Monitor connection count
- View query performance
