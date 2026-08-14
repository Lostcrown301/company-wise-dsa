from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from app.config import settings

# neon specific postgres setup
SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True, # Handles disconnected connections gracefully
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
