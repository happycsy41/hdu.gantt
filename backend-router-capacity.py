from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/capacity", tags=["capacity"])

DEFAULT = {
    "eng":  {"count": 1, "loePerHead": 40},
    "sc":   {"count": 1, "loePerHead": 40},
    "prod": {"count": 1, "loePerHead": 40},
    "pm":   {"count": 1, "loePerHead": 40},
}

@router.get("/", response_model=schemas.CapacityOut)
def get_capacity(
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    cap = db.query(models.Capacity).filter(models.Capacity.owner_id == user.id).first()
    if not cap:
        cap = models.Capacity(owner_id=user.id, settings=DEFAULT)
        db.add(cap); db.commit(); db.refresh(cap)
    return cap

@router.put("/", response_model=schemas.CapacityOut)
def upsert_capacity(
    body: schemas.CapacityIn,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    cap = db.query(models.Capacity).filter(models.Capacity.owner_id == user.id).first()
    if cap:
        cap.settings = body.settings
    else:
        cap = models.Capacity(owner_id=user.id, settings=body.settings)
        db.add(cap)
    db.commit(); db.refresh(cap)
    return cap
