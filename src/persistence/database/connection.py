from sqlmodel import create_engine, SQLModel
from typing import Generator

DATABASE_URL = "sqlite:///./pokemon.db"

# Cambio: usar create_engine de sqlmodel
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_database() -> Generator:
    from sqlmodel import Session
    
    with Session(engine) as session:
        yield session