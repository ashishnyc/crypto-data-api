import os
from sqlmodel import SQLModel, create_engine, Session
import logging

logger = logging.getLogger(__name__)


def get_db_connection_str():
    uname = os.environ.get("DB_USER", "")
    passwd = os.environ.get("DB_PASS", "")
    host = os.environ.get("DB_HOST", "")
    port = os.environ.get("DB_PORT", "")
    db = os.environ.get("DB_NAME", "")
    return f"postgresql+psycopg2://{uname}:{passwd}@{host}:{port}/{db}"


def get_engine():
    return create_engine(get_db_connection_str(), future=True)


def create_db_and_tables():
    logger.info("Creating Database and Tables")
    SQLModel.metadata.create_all(get_engine())


def get_session():
    db = Session(get_engine())
    try:
        yield db
    finally:
        db.close()
