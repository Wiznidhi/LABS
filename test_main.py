from fastapi import FastAPI
from fastapi.testclient import TestClient 
from auth import get_current_user

from rooms_crud import router

def override_get_current_user():
    return {"username": "test_staff", "role": "staff"}

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_current_user] = override_get_current_user
client = TestClient(app)

def test_read_root(): 
    r = client.get("/") 
    assert r.status_code == 200 
    assert r.json()=={"message": "Welcome to the Hotel API!"}

def test_create_and_get_room(): 
    payload = {"number":"200","type":"double","price":120,"capacity":2} 
    r = client.post("/rooms/", json=payload) 
    assert r.status_code == 200 
    data = r.json() 
    assert data["number"] == "200" 
    rid = data["id"] 
    r2 = client.get(f"/rooms/{rid}") 
    assert r2.status_code == 200 