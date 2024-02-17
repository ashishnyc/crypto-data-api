from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import (
    DB_HOST as host,
    DB_PORT as port,
    DB_USERNAME as uname,
    DB_PASSWORD as passwd,
    DB_NAME as db,
)

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{uname}:{passwd}@{host}:{port}/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
