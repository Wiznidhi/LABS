from fastapi import Depends, HTTPException 
from auth import get_current_user 

def staff_required(current_user = Depends(get_current_user)): 
    if current_user.get("role") != "staff": 
         raise HTTPException(status_code=403, detail="staff role required") 
    return current_user 

# usage in an endpoint: 
# @app.post("/rooms/", dependencies=[Depends(staff_required)]) 