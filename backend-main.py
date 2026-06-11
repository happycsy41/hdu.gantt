from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, projects, capacity
from .config import settings

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HDU Gantt Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(projects.router)
app.include_router(capacity.router)

@app.get("/")
def health():
    return {"status": "ok", "service": "HDU Gantt Planner API"}
