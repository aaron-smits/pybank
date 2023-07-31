# https://fastapi.tiangolo.com/tutorial/sql-databases/?h=database
# import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from dotenv import load_dotenv

# load_dotenv()

# read the url from the .env file
POSTGRES_URL = "postgresql://postgres:mysecretpassword1234@test-postgres:5432/postgres-db?sslmode=disable"
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
