# NestMatch 🏠
> *Find your space, find your people.*

Student housing platform for India — verified listings, safe messaging, roommate matching.

---

## Team

| Member | Role | Area |
|---|---|---|
| TM1 | Tech Lead & DevOps | CI/CD, deployment, admin panel |
| TM2 | Frontend Lead | Auth UI, landlord flows, chat UI |
| TM3 | Backend Core | Auth, listings CRUD, photos, email |
| TM4 | Backend Search & Realtime | Search, WebSockets, messaging, booking |
| TM5 | Frontend Discovery | Search page, listing detail, map |

---

## Quick Start — Local Dev

### Prerequisites
Install these before starting:
- [Node.js 20+](https://nodejs.org)
- [Python 3.12](https://python.org)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — for Postgres + Redis

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_ORG/nestmatch.git
cd nestmatch
```

### 2. Start the database and Redis
```bash
docker compose up -d
```
This starts Postgres on port 5432 and Redis on port 6379. Run once, leave it running.

### 3. Set up the backend
```bash
cd backend
python -m venv .venv

# Mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt

# Copy env file and fill in values
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload --port 8000
```
Backend is now at: http://localhost:8000  
API docs at: http://localhost:8000/docs

### 4. Set up the frontend
```bash
cd frontend
npm install

# Copy env file
cp .env.example .env.local

# Start the frontend dev server
npm run dev
```
Frontend is now at: http://localhost:5173

---

## Branching Strategy

```
main        ← production only, protected, requires PR + CI
develop     ← integration branch, all PRs merge here
```

**Branch naming:**
```
feature/tm2/listing-wizard
feature/tm3/auth-endpoints
fix/tm1/ci-config
chore/setup-docker
```

**Commit messages (Conventional Commits):**
```
feat(listings): add photo upload with Cloudinary
fix(auth): refresh token not clearing correctly
chore(ci): add pytest to GitHub Actions
```

---

## PR Rules
- Every PR requires review from at least 1 other member
- CI must pass before merging
- No API keys in frontend code — use `VITE_` env vars
- No `console.log` in production code
- New env vars must be added to `.env.example`

---

## Project Structure

```
nestmatch/
├── .github/
│   ├── workflows/ci.yml          ← GitHub Actions CI
│   └── PULL_REQUEST_TEMPLATE.md
├── frontend/                     ← React + Vite (TM2, TM5)
│   ├── src/
│   ├── .env.example
│   └── vercel.json
├── backend/                      ← FastAPI + Python (TM3, TM4)
│   ├── app/
│   ├── alembic/
│   ├── .env.example
│   └── railway.json
├── docker-compose.yml            ← Local Postgres + Redis
└── README.md
```

---

## Deployment

| Service | Platform | URL |
|---|---|---|
| Frontend | Vercel | https://nestmatch.vercel.app |
| Backend | Railway | https://nestmatch-api.railway.app |
| Database | Neon.tech | (serverless Postgres) |
| Images | Cloudinary | (free tier) |
| Email | SendGrid | (free tier, 100/day) |

---

*See `CLAUDE.md` for full product requirements, data models, API contracts, and sprint plan.*
