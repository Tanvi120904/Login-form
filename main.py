from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import create_db, get_user, add_user, verify_password

app = FastAPI()
create_db()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: User):
    if get_user(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    add_user(user.email, user.password)
    return {"message": "Signup successful"}

@app.post("/login")
def login(user: User):
    db_user = get_user(user.email)
    if not db_user or not verify_password(user.password, db_user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
