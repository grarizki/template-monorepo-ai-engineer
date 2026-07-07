from collections.abc import Generator

from sqlmodel import Session, create_engine

from ai_template.core.settings import settings

engine = create_engine(settings.database_url, echo=True)


def db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
