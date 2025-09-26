from fastapi import BackgroundTasks, APIRouter 
from bookings import create_booking # assume function that saves booking
import time

router = APIRouter() 

def send_confirmation_email(booking_id: int, email: str): 
    # simulated long-running action  
    time.sleep(1) 
    print(f"Sent confirmation for booking {booking_id} to {email}") 

@router.post("/bookings_with_email/") 
def book_with_email(payload, background_tasks: BackgroundTasks): 
    booking = create_booking(payload) # synchronous for demo 
    background_tasks.add_task(send_confirmation_email, booking.id, 
    payload.guest_email or "guest@example.com") 
    return {"booking_id": booking.id, "status": "confirmed (email queued)"} 
