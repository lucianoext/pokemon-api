from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./pokemon.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_database() -> Generator[Session]:
    with Session(engine) as session:
        yield session
