from sqlmodel import SQLModel

from ai_template.models.engine import engine


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
