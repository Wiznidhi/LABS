from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from settings import get_settings

settings = get_settings()

# Parse DB URL
url = make_url(settings.database_url)

# Handle SQLite-specific option
connect_args = {}
if url.drivername.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine
engine = create_engine(settings.database_url, connect_args=connect_args)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class
Base = declarative_base()


# Models
class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    type = Column(String)
    price = Column(Integer)
    capacity = Column(Integer)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    guest_name = Column(String)


# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
