from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from typing import Dict 
from fastapi import FastAPI
import uvicorn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

fake_users_db: Dict[str, Dict] = { 
 "alice": {"username": "alice", "password": "wonderland", "role": "staff"}, 
 "bob": {"username": "bob", "password": "builder", "role": "guest"}, 
} 

def authenticate_user(username: str, password: str): 
    user = fake_users_db.get(username) 
    if not user or user["password"] != password: 
        return None 
    return user 

from fastapi import APIRouter 

router = APIRouter() 

@router.post("/token") 
def login(form_data: OAuth2PasswordRequestForm = Depends()): 
    user = authenticate_user(form_data.username, form_data.password) 
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Invalid credentials") 
    # For lab: return a fake token (in prod use JWT) 
    return {"access_token": user["username"], "token_type": "bearer"} 

async def get_current_user(token: str = Depends(oauth2_scheme)): 
    user = fake_users_db.get(token) 
    if not user: 
        raise HTTPException(status_code=401, detail="Invalid token") 
    return user 

if __name__=="__main__":
    uvicorn.run("auth:app", host="localhost", port=8000, reload=True)