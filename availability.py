from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from datetime import date 
from db import get_db, Room, Booking
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Hotel API", version="0.1") 

# @app.get("/") 
# def read_root(): 
#     return {"message": "Welcome to the Hotel API!"} 

router = APIRouter() 

@router.get("/search/") 
def search(start_date: date, end_date: date, min_capacity: int = 1, db: Session 
= Depends(get_db)): 
    # rooms meeting capacity 
    candidate_rooms = db.query(Room).filter(Room.capacity >= 
    min_capacity).all() 
    available = [] 
    for room in candidate_rooms: 
        overlaps = db.query(Booking).filter( 
            Booking.room_id == room.id, 
            Booking.start_date < end_date, 
            Booking.end_date > start_date 
        ).count() 
        if overlaps == 0: 
            available.append(room) 
    return available

# if __name__=="__main__":
#     uvicorn.run("availability:app", host="127.0.0.1", port=8000, reload=True)