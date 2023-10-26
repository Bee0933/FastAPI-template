from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from ..config import Settings

# from pydantic import BaseSettings


settings = Settings()

DB_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:5432/{settings.database_name}"

engine = create_engine(url=DB_URL, echo=True)

Base = declarative_base()

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
