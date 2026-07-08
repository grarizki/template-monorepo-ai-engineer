from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from ai_template.main import app
from ai_template.models.engine import engine

client = TestClient(app)


def init_test_db():
    SQLModel.metadata.create_all(engine)


init_test_db()
