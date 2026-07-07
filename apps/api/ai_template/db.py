"""Database engine and table definitions."""

from pathlib import Path

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "db.sqlite"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    image_url = Column(String)


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, server_default=func.now())
    artifact_path = Column(String)
    metrics = Column(JSON)


class TrainingScript(Base):
    __tablename__ = "training_scripts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    model_id = Column(Integer, ForeignKey("models.id"))
    created_at = Column(DateTime, server_default=func.now())
    image_url = Column(String)


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    status = Column(String, default="pending")
    deployed_at = Column(DateTime, server_default=func.now())
    url = Column(String)


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
