from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    account_number: int
    balance: int = 0


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    disabled: bool = True

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str


class TransferRequest(BaseModel):
    from_account_number: int
    to_account_number: int
    amount: int
    description: str


class TransferResponse(BaseModel):
    success: bool
    new_balance: int
    message: str
