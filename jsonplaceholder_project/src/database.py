from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=2,
    max_overflow=0,
    pool_recycle=600,
    echo=True,
    echo_pool=True,
    future=True)
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    future=True)

@contextmanager
def get_session() -> Session:
    session =  SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()