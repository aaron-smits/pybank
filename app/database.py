# https://fastapi.tiangolo.com/tutorial/sql-databases/?h=database
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

# read the url from the .env file
POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise ValueError("No POSTGRES_URL set")
engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def test_create_user(client):
    response = client.post(
        "/accounts",
        json={
            "username": "testuser",
            "email": "test@testing.com",
            "full_name": "Test User",
            "account_number": 1234567890,
            "balance": 1000,
        }),
    assert response.status_code == 200
    data = response.json()
    assert data.email == "test@testing.com"
    assert data.username == "testuser"
    assert data.full_name == "Test User"
    assert data.account_number == 1234567890
    assert data.balance == 1000
