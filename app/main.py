from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


import app.models as models
import app.schemas as schemas
import crud
import auth
from database import SessionLocal, engine


# Create all tables in the database
# Fast API recomends to use Alembic for migrations,
# so I should get familiar with it later on
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/accounts", response_model=list[schemas.User])
async def get_accounts(
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):

    users = crud.get_users(db)
    return users


@app.post("/accounts", response_model=schemas.User)
async def create_account(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db_user = crud.get_user_by_account_number(db, user.account_number)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account number already registered",
        )

    return crud.create_user(db, user)


@app.get("/accounts/{id}", response_model=schemas.User)
async def get_account(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):
    db_user = crud.get_user(db, id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@app.put("/accounts/{id}", response_model=schemas.User)
async def update_account(
    id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):
    db_user = crud.get_user_by_username(db, id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return crud.update_user(db, db_user, user)


@app.delete("/accounts", response_model=schemas.User)
async def delete_account_by_username(
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):
    return crud.delete_user(db, id)


@app.post("/accounts/transfer", response_model=schemas.TransferResponse)
async def transfer(
    transfer: schemas.TransferRequest,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):
    current_user = auth.get_current_user(db, token)
    from_account = crud.get_user(db, current_user.id)
    if not from_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="From user not found",
        )

    to_account = crud.get_user_by_account_number(db, transfer.to_account_number)
    if not to_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="To user not found",
        )
    if from_account.balance < transfer.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        )
    return crud.transfer_funds(db, from_account, to_account, transfer.amount)
