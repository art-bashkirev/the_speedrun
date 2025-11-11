from fastapi import FastAPI
from models import *

app = FastAPI()

# Auth
@app.post("/auth/login")
async def login(data: LoginModel):
    # TODO: Implement login logic
    return {"message": "Login successful"}

# Admin
@app.get("/admin/cache/clear")
async def clear_cache():
    # TODO: Implement cache clearing logic
    return {"message": "Cache cleared"}