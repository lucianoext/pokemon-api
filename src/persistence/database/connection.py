from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

DATABASE_URL = "sqlite:///./pokemon.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_database() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session