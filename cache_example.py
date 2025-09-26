from functools import lru_cache 
import time 

@lru_cache(maxsize=32) 
def expensive_stats(year: int): 
    # simulate heavy calculation 
    time.sleep(4) 
    return {"year": year, "total_bookings": 1234} 

# endpoint usage: 
# @app.get("/stats/{year}") 
# def stats(year: int): 
# return expensive_stats(year) 
