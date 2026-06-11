from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    username   = Column(String, unique=True, index=True, nullable=False)
    hashed_pw  = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    projects  = relationship("Project",  back_populates="owner", cascade="all, delete-orphan")
    capacities = relationship("Capacity", back_populates="owner", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"
    id         = Column(Integer, primary_key=True, index=True)
    owner_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    wbs        = Column(String, nullable=False)          # WBS No / Ref No
    name       = Column(String, nullable=False)
    start_week = Column(Integer, nullable=False)
    year       = Column(Integer, nullable=False)
    phases     = Column(JSON, nullable=False, default={}) # {po, eng, mat, proc, prod, hol, doc, float}
    loe        = Column(JSON, nullable=False, default={}) # {eng, sc, prod, pm}
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="projects")


class Capacity(Base):
    __tablename__ = "capacities"
    id           = Column(Integer, primary_key=True, index=True)
    owner_id     = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    # stored as JSON: {eng:{count,loePerHead}, sc:{...}, prod:{...}, pm:{...}}
    settings     = Column(JSON, nullable=False, default={})
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="capacities")
