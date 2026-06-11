from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

# ── Auth ──────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# ── Projects ──────────────────────────────────────────────────────────────
class ProjectCreate(BaseModel):
    wbs: str
    name: str
    start_week: int
    year: int
    phases: Dict[str, Any]
    loe: Dict[str, Any]

class ProjectUpdate(ProjectCreate):
    pass

class ProjectOut(ProjectCreate):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

# ── Capacity ──────────────────────────────────────────────────────────────
class CapacityIn(BaseModel):
    settings: Dict[str, Any]

class CapacityOut(CapacityIn):
    id: int
    owner_id: int
    class Config:
        from_attributes = True
