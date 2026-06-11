from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Project).filter(models.Project.owner_id == user.id).all()

@router.post("/", response_model=schemas.ProjectOut, status_code=201)
def create_project(
    body: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    proj = models.Project(**body.model_dump(), owner_id=user.id)
    db.add(proj); db.commit(); db.refresh(proj)
    return proj

@router.put("/{proj_id}", response_model=schemas.ProjectOut)
def update_project(
    proj_id: int,
    body: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    proj = db.query(models.Project).filter(
        models.Project.id == proj_id,
        models.Project.owner_id == user.id
    ).first()
    if not proj:
        raise HTTPException(404, "Project not found")
    for k, v in body.model_dump().items():
        setattr(proj, k, v)
    db.commit(); db.refresh(proj)
    return proj

@router.delete("/{proj_id}", status_code=204)
def delete_project(
    proj_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    proj = db.query(models.Project).filter(
        models.Project.id == proj_id,
        models.Project.owner_id == user.id
    ).first()
    if not proj:
        raise HTTPException(404, "Project not found")
    db.delete(proj); db.commit()
