# HDU Gantt Planner — Setup Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (local) **or** a free Render PostgreSQL instance (cloud)

---

## Running locally

### 1 — PostgreSQL
```bash
# macOS (Homebrew)
brew install postgresql@16 && brew services start postgresql@16
createdb hdu_gantt

# Ubuntu / Debian
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb hdu_gantt
```

### 2 — Backend
```bash
cd backend

# Create & activate virtual env
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL, SECRET_KEY, ALLOWED_ORIGINS

# Run (tables are auto-created on first start)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: http://localhost:8000/docs

### 3 — Frontend
```bash
cd frontend

npm install

# No .env needed locally — Vite proxies /api → http://localhost:8000
npm run dev
```

Open: http://localhost:5173

---

## Deploying to Render (backend) + Vercel (frontend)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/hdu-gantt.git
git push -u origin main
```

### Step 2 — Render (Backend + Database)

1. Go to https://render.com → **New → Blueprint**
2. Connect your GitHub repo and select the `backend/` folder
3. Render reads `render.yaml` and automatically:
   - Creates a **PostgreSQL** database (`hdu-gantt-db`)
   - Creates a **Web Service** (`hdu-gantt-api`)
   - Injects `DATABASE_URL` and generates a `SECRET_KEY`
4. After deploy, **copy the service URL** (e.g. `https://hdu-gantt-api.onrender.com`)
5. In Render dashboard → Environment → set:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app
   ```
   (You'll get the Vercel URL in Step 3; update this after.)

> **Note:** Render's free tier spins down after 15 min inactivity. The first request after sleep takes ~30 s. Upgrade to a paid instance to avoid this.

### Step 3 — Vercel (Frontend)

1. Go to https://vercel.com → **Add New Project**
2. Import your GitHub repo
3. Set **Root Directory** to `frontend`
4. Add **Environment Variable**:
   ```
   VITE_API_URL=https://hdu-gantt-api.onrender.com
   ```
5. Click **Deploy**
6. Copy the Vercel URL (e.g. `https://hdu-gantt.vercel.app`) and paste it back into Render's `ALLOWED_ORIGINS`

### Step 4 — Verify
- Open your Vercel URL
- Register an account → add a project → confirm it persists across refreshes ✓

---

## Environment variable reference

### backend/.env
| Variable | Example | Notes |
|---|---|---|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/hdu_gantt` | Render injects this automatically |
| `SECRET_KEY` | `a-very-long-random-string` | Render auto-generates via `generateValue: true` |
| `ALLOWED_ORIGINS` | `https://your-app.vercel.app` | Comma-separated list |

### frontend/.env (local dev only)
| Variable | Value | Notes |
|---|---|---|
| `VITE_API_URL` | *(empty)* | Vite proxy handles `/api` locally |

### Vercel dashboard env
| Variable | Example |
|---|---|
| `VITE_API_URL` | `https://hdu-gantt-api.onrender.com` |

---

## Project structure recap
```
hdu-gantt/
├── backend/
│   ├── main.py            # FastAPI app + CORS + table creation
│   ├── config.py          # Pydantic settings from .env
│   ├── database.py        # SQLAlchemy engine + session
│   ├── models.py          # User, Project, Capacity ORM models
│   ├── schemas.py         # Pydantic request/response schemas
│   ├── auth.py            # JWT + bcrypt helpers + OAuth2 guard
│   ├── routers/
│   │   ├── users.py       # POST /api/auth/register, /login, GET /me
│   │   ├── projects.py    # CRUD /api/projects/
│   │   └── capacity.py    # GET/PUT /api/capacity/
│   ├── requirements.txt
│   ├── render.yaml        # Render Blueprint (DB + web service)
│   └── .env.example
└── frontend/
    ├── public/index.html
    ├── src/
    │   ├── main.jsx        # React entry point
    │   ├── App.jsx         # Root component, state orchestration
    │   ├── api.js          # Axios client + all API calls
    │   ├── components/
    │   │   ├── Header.jsx
    │   │   ├── AuthModal.jsx
    │   │   ├── GanttChart.jsx
    │   │   ├── TotalsTable.jsx
    │   │   ├── ProjectModal.jsx
    │   │   └── CapacityModal.jsx
    │   └── utils/gantt.js  # Phase defs, week math, LoE calculations
    ├── vite.config.js      # Dev proxy + React plugin
    ├── vercel.json         # SPA rewrite rule
    ├── package.json
    └── .env.example
```
