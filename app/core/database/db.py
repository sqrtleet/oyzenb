from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import POSTGRES_URL


engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    try:
        db_session = SessionLocal()
        yield db_session
    finally:
        db_session.close()
