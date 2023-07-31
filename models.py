from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    account_number = Column(Integer, unique=True)
    balance = Column(Integer)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=True)
