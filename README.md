# NestMatch 🏠

> *Find your space, find your people.*

NestMatch is a student-first housing platform designed to solve student accommodation challenges through verified listings, secure platform interactions, and lifestyle-based flatmate matching.

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

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide icons, Zustand, React Router v6, Axios
- **Backend**: FastAPI (Python 3.12+), SQLAlchemy 2.0 (async), Pydantic v2, Alembic, python-jose, bcrypt
- **Database & Cache**: PostgreSQL 16, Redis (SQLite in-memory for testing)
- **Media & Communications**: Cloudinary (photo storage), SendGrid (email)

---

## Quick Start — Local Dev

### Prerequisites
- Node.js 20+
- Python 3.12
- Docker Desktop (for Postgres & Redis)

### 1. Clone the repository
```bash
git clone https://github.com/Tanishk2006/Nestmatch.git
cd Nestmatch
```

### 2. Start Database and Redis
```bash
docker compose up -d
```
*(Alternatively: `docker-compose -f backend/docker-compose.yml up -d`)*

### 3. Set up the backend
```bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
Interactive API documentation: `http://localhost:8000/docs`

### 4. Set up the frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Frontend development server: `http://localhost:5173`

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

**Commit format:**
```
feat(listings): add photo upload with Cloudinary
fix(auth): refresh token not clearing correctly
chore(ci): add pytest to GitHub Actions
```

---

## PR Rules
- Every PR requires review from at least 1 other member
- CI checks must pass before merging
- No API keys in frontend code — use `VITE_` environment variables
- No `console.log` in production code
- New environment variables must be documented in `.env.example`

---

## Project Structure

```
nestmatch/
├── .github/
│   ├── workflows/ci.yml          ← GitHub Actions CI pipeline
│   └── PULL_REQUEST_TEMPLATE.md  ← Pull request template
├── frontend/                     ← React + Vite frontend
│   ├── src/
│   ├── .env.example
│   └── vercel.json
├── backend/                      ← FastAPI + Python backend
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   └── railway.json
├── docker-compose.yml            ← Local Postgres + Redis dev services
├── TM1_SETUP_GUIDE.md            ← Deployment & cloud setup guide
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
