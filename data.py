from db import SessionLocal, Room, Booking
from datetime import date
 
# Create a new DB session
db = SessionLocal()
 
try:
    # Create a new Room instance
    room1 = Room(number="103", type="Standard", price=150, capacity=3)
    room2 = Room(number="104", type="Suit", price=170, capacity=2)
    room3 = Room(number="105", type="Standard", price=190, capacity=3)
    room4 = Room(number="106", type="Deluxe", price=200, capacity=2)
    db.add_all([room1,room2,room3,room4])
    db.commit()
 
 
    # Create a new Booking instance for the room
    new_booking = Booking(
        room_id= room3.id,
        start_date=date(2025, 10, 10),
        end_date=date(2025, 10, 15),
        guest_name="Alice Smith"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
 
    print(f"Created booking with id={new_booking.id}")
 
finally:
    db.close()