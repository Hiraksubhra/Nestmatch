
# NestMatch

> *Find your space, find your people.*

NestMatch is a student-first housing platform designed to solve student accommodation challenges through verified listings, secure platform interactions, and lifestyle-based flatmate matching.

---

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, shadcn/ui inspired components, Lucide icons, Zustand, React Router v6, Axios
- **Backend**: FastAPI (Python 3.12+), SQLAlchemy 2.0 (async), Pydantic v2, Alembic, python-jose, bcrypt
- **Database & Cache**: PostgreSQL 16, Redis
- **Media & Communications**: Cloudinary (photo storage), SendGrid (email)

---

## Quickstart

### 1. Prerequisites
- Node.js 18+ (v20+ recommended)
- Python 3.11+
- Docker & Docker Compose (optional for local Postgres & Redis)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
Interactive API docs are available at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Frontend application will be accessible at: `http://localhost:5173`

### 4. Running via Docker Compose
To run PostgreSQL and Redis for backend services:
```bash
docker-compose -f backend/docker-compose.yml up -d
```

---

## Project Structure
Refer to [gemini.md](gemini.md) for master architecture and sprint details, and [brandRules_Student_Rental.md](brandRules_Student_Rental.md) for UI/UX specifications.
