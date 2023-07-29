from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/accounts")
async def get_accounts():
    return {"message": "Hello World"}


@app.post("/accounts")
async def create_account():
    return {"message": "Hello World"}


@app.get("/accounts/{account_id}")
async def get_account(account_id: int):
    return {"message": "Hello World"}


@app.put("/accounts/{account_id}")
async def update_account(account_id: int):
    return {"message": "Hello World"}


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: int):
    return {"message": "Hello World"}


@app.post("/transfer")
async def transfer():
    return {"message": "Hello World"}


@app.get("/login")
async def login():
    return {"message": "Hello World"}
