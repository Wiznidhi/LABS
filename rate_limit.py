import time 
from fastapi import Request, HTTPException, Depends 

RATE_LIMIT = 7 # requests 
WINDOW = 60 # seconds 
_ip_store = {} # ip -> (count, window_start) 

def rate_limit_dependency(request: Request): 
    ip = request.client.host 
    now = time.time() 
    count, window_start = _ip_store.get(ip, (0, now)) 
    if now - window_start > WINDOW: 
        count, window_start = 0, now 
    count += 1 
    _ip_store[ip] = (count, window_start) 
    if count > RATE_LIMIT: 
        raise HTTPException(status_code=429, detail="Too many requests") 
    return True 
