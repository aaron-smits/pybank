
from sqlalchemy.orm import Session

from . import auth, models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_account_number(db: Session, account_number: int):
    return db.query(models.User).filter(models.User.account_number == account_number).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        account_number=user.account_number,
        balance=user.balance,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, username: str, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    db_user.username = user.username
    db_user.email = user.email
    db_user.full_name = user.full_name
    db_user.account_number = user.account_number
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    db.delete(db_user)
    db.commit()
    return db_user


def transfer_funds(db: Session, from_account: schemas.User, to_account: schemas.User, amount: int):
    from_account.balance -= amount
    to_account.balance += amount
    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)
    return from_account
