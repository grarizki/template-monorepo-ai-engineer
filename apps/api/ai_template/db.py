"""Database engine and table definitions."""

from pathlib import Path

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

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


class Benchmark(Base):
    __tablename__ = "benchmarks"

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"))
    name = Column(String, nullable=False)
    dataset_size = Column(Integer)
    metrics = Column(JSON)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    version = Column(String, nullable=False)
    metrics = Column(JSON)
    artifact_path = Column(String)
    created_at = Column(DateTime, server_default=func.now())


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
