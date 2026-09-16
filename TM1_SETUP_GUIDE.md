# TM1 Setup Guide — Step by Step
> Follow this top to bottom. Each step builds on the last.

---

## PHASE 1 — GitHub Repo Setup (Day 1, ~30 mins)

### Step 1: Create the GitHub repo

1. Go to https://github.com and log in
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - Repository name: `nestmatch`
   - Description: `Student housing platform — NestMatch`
   - Visibility: **Private** (change to Public later if needed)
   - ✅ Check "Add a README file"
4. Click **Create repository**
5. Go to **Settings → Collaborators → Add people** → invite TM2, TM3, TM4, TM5

---

### Step 2: Create the develop branch

On the GitHub website:
1. Click the branch dropdown (shows `main`)
2. Type `develop` in the box
3. Click **Create branch: develop from main**

---

### Step 3: Protect the main branch

1. Go to **Settings → Branches → Add branch protection rule**
2. Branch name pattern: `main`
3. ✅ Require a pull request before merging
4. ✅ Require status checks to pass before merging
5. ✅ Require branches to be up to date before merging
6. Click **Create**

---

### Step 4: Upload the project files

On your computer, open terminal and run:

```bash
# Clone your new repo
git clone https://github.com/YOUR_USERNAME/nestmatch.git
cd nestmatch

# Copy all the generated files into this folder
# (from the ZIP you downloaded from Claude)

# Add everything
git add .
git commit -m "chore: initial project setup — CI, docker, env, readme"
git push origin main

# Also push to develop
git checkout -b develop
git push origin develop
```

---

## PHASE 2 — Deploy Frontend (Vercel, ~20 mins)

### Step 5: Deploy to Vercel

1. Go to https://vercel.com and sign in with GitHub
2. Click **Add New → Project**
3. Select your `nestmatch` repo
4. Set **Root Directory** to `frontend`
5. Framework preset will auto-detect as **Vite**
6. Under **Environment Variables**, add:
   ```
   VITE_API_URL = https://your-railway-backend-url.railway.app
   ```
   (you'll get this URL in Step 7 — leave it blank for now, add later)
7. Click **Deploy**

Your frontend URL will be: `https://nestmatch.vercel.app` (or similar)

---

## PHASE 3 — Deploy Backend (Railway, ~20 mins)

### Step 6: Create a Railway account

1. Go to https://railway.app and sign in with GitHub
2. Click **New Project → Deploy from GitHub repo**
3. Select `nestmatch`
4. Set **Root Directory** to `backend`

### Step 7: Add environment variables on Railway

In your Railway project → **Variables** tab, add each line from `backend/.env.example`:
- For `SECRET_KEY`, run this in your terminal and paste the output:
  ```bash
  openssl rand -hex 32
  ```
- For `DATABASE_URL`, use the Neon.tech URL (Step 8)

### Step 8: Set up the database (Neon.tech — free)

1. Go to https://neon.tech and create a free account
2. Create a new project: `nestmatch`
3. Copy the **Connection string** (looks like `postgresql://user:pass@ep-xxx.neon.tech/nestmatch`)
4. Change `postgresql://` to `postgresql+asyncpg://`
5. Paste this as `DATABASE_URL` in Railway variables

---

## PHASE 4 — Third-Party Services (~45 mins)

### Step 9: Cloudinary (image storage)

1. Go to https://cloudinary.com → Sign up free
2. Dashboard → copy **Cloud name**, **API Key**, **API Secret**
3. Add to Railway env vars: `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`

### Step 10: SendGrid (email)

1. Go to https://sendgrid.com → Sign up free
2. Go to **Settings → API Keys → Create API Key**
3. Name: `nestmatch`, Permission: Full Access
4. Copy the key → add as `SENDGRID_API_KEY` in Railway

### Step 11: Google OAuth

1. Go to https://console.cloud.google.com
2. Create a new project: `nestmatch`
3. Go to **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID**
4. Application type: **Web application**
5. Authorized redirect URIs: add `http://localhost:8000/api/auth/google/callback`
6. Copy **Client ID** and **Client Secret**
7. Add to both Railway (backend) and Vercel (frontend) env vars

---

## PHASE 5 — Tell Your Team (Day 2)

Send this message to your team:

```
Hey team! Repo is set up.

Clone: https://github.com/YOUR_USERNAME/nestmatch

Rules:
- Always branch off develop, never main
- Branch naming: feature/tmX/short-description
- Commit format: feat(area): what you did
- Every PR needs 1 reviewer before merge
- CI must pass before merging

TM2: Set up frontend/ with Vite + React + Tailwind
TM3: Set up backend/ with FastAPI + requirements.txt
Everyone: copy .env.example to .env and fill in your values

Standups: Monday 30min sync, Friday demo
```

---

## Daily Workflow (once setup is done)

```bash
# Start of every work session:
git checkout develop
git pull origin develop

# Create your branch:
git checkout -b feature/tm1/admin-dashboard

# Work, then commit:
git add .
git commit -m "feat(admin): add metrics dashboard"

# Push and open PR:
git push origin feature/tm1/admin-dashboard
# Go to GitHub → open PR → set base to develop
```

---

## Checklist — Sprint 0 Done When:

- [ ] GitHub repo created with main + develop branches
- [ ] main branch is protected
- [ ] All 5 teammates added as collaborators
- [ ] CI workflow file is in `.github/workflows/ci.yml`
- [ ] PR template is in `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] `.env.example` committed (not `.env`)
- [ ] `docker-compose.yml` committed and working locally
- [ ] Frontend skeleton deployed on Vercel
- [ ] Backend skeleton deployed on Railway
- [ ] All third-party accounts created: Cloudinary, SendGrid, Google OAuth, Neon.tech
- [ ] Shared the accounts/keys with team securely (NOT via Git — use WhatsApp/email)
