from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from db import get_db, Booking, Room 
from models import BookingCreate 
from fastapi import FastAPI
from ws import manager  # import the manager

app=FastAPI()

router = APIRouter() 

@router.post("/bookings/") 
async def create_booking(payload: BookingCreate, db: Session = Depends(get_db)): 
    if payload.start_date >= payload.end_date: 
        raise HTTPException(status_code=400, detail="end_date must be after start_date") 
    room = db.query(Room).filter(Room.id == payload.room_id).first() 
    if not room: 
        raise HTTPException(status_code=404, detail="room not found") 

    conflict = db.query(Booking).filter( 
    Booking.room_id == payload.room_id, 
    Booking.start_date < payload.end_date, 
    Booking.end_date > payload.start_date 
    ).first() 
    if conflict: 
        raise HTTPException(status_code=409, detail="room already booked for these dates") 
    b = Booking(room_id=payload.room_id, start_date=payload.start_date, 
    end_date=payload.end_date, guest_name=payload.guest_name) 
    db.add(b) 
    db.commit() 
    db.refresh(b) 
    await manager.broadcast({
        "type": "booking_created",
        "booking_id": b.id,
        "guest_name": b.guest_name,
        "room_id": b.room_id,
        "start_date": str(b.start_date),
        "end_date": str(b.end_date)
    })
    return b

# if __name__=="__main__":
#     uvicorn.run("bookings:app", host="localhost", port=8000, reload=True)