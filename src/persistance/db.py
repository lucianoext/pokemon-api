# from typing import Generator
# from sqlmodel import SQLModel, create_engine, Session
# from sqlalchemy.engine import Engine
# from sqlalchemy import text

# from app.config import settings

# def _create_engine(url: str) -> Engine:
#     if url.startswith("sqlite"):
#         return create_engine(
#             url,
#             echo=settings.DB_ECHO,
#             connect_args={"check_same_thread": False}
#         )
#     return create_engine(
#         url,
#         echo=settings.DB_ECHO,
#         pool_pre_ping=True,
#         pool_size=settings.DB_POOL_SIZE,
#         max_overflow=settings.DB_MAX_OVERFLOW,
#         future=True
#     )

# engine: Engine = _create_engine(settings.DATABASE_URL)

# def get_session() -> Generator[Session, None, None]:
#     with Session(engine) as session:
#         yield session

# def init_db() -> None:
#     from app.persistence import models
#     SQLModel.metadata.create_all(engine)

# def ping_db() -> bool:
#     try:
#         with Session(engine) as s:
#             s.exec(text("SELECT 1"))
#             return True
#     except Exception:
#         return False