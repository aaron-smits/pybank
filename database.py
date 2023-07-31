# https://fastapi.tiangolo.com/tutorial/sql-databases/?h=database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/postgres"
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
