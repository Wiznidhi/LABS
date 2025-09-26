from fastapi import APIRouter, HTTPException, Depends
from models import Room, RoomCreate 
import uvicorn
from rbac import staff_required  # Import your RBAC dependency

from rate_limit import rate_limit_dependency

router = APIRouter()

rooms = [] 
next_id = 1 

@router.post("/rooms/", response_model=Room, dependencies=[Depends(staff_required)]) 
def create_room(room: RoomCreate): 
    global next_id 
    new = room.dict() 
    new['id'] = next_id 
    next_id += 1 
    rooms.append(new) 
    return new 

@router.get("/rooms/", response_model=list[Room], dependencies=[Depends(staff_required)]) 
def list_rooms(): 
    return rooms 

@router.get("/rooms/{room_id}", response_model=Room) 
def get_room(room_id: int): 
    for r in rooms: 
        if r['id'] == room_id: 
            return r 
    raise HTTPException(status_code=404, detail="Room not found") 

@router.put("/rooms/{room_id}", response_model=Room, dependencies=[Depends(rate_limit_dependency)]) 
def update_room(room_id: int, room: RoomCreate): 
    for r in rooms: 
        if r['id'] == room_id: 
            r.update(room.dict()) 
            return r 
    raise HTTPException(status_code=404, detail="Room not found") 

@router.delete("/rooms/{room_id}") 
def delete_room(room_id: int): 
    for i, r in enumerate(rooms): 
        if r['id'] == room_id: 
            rooms.pop(i) 
            return {"ok": True} 
    raise HTTPException(status_code=404, detail="Room not found") 

if __name__=="__main__":
    uvicorn.run("rooms_crud:app", host="localhost", port=8000, reload=True)