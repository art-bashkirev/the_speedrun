from fastapi import FastAPI
from models import *

from cache_manager import *
from permissions_manager import *

from database import Database

app = FastAPI()

db = Database()

# Auth
@app.post("/auth/login")
async def login(data: LoginModel):
    user = db.get_user_by_username(data.username)
    if user and user.password != data.password:
            return {"error": "Invalid password"} 
    return {"message": "Login successful"}

# Admin
@app.get("/admin/cache/clear")
async def clear_cache():
    # TODO: Implement cache clearing logic
    return {"message": "Cache cleared"}