from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Create database engine with pool_pre_ping enabled for production resilience
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

# Session local factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator that yields a database session.
    Guarantees the session is closed when the request lifecycle ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
