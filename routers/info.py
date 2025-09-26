from fastapi import APIRouter, Depends
from settings import get_settings, Settings

router = APIRouter()

@router.get("/info")
def get_info(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}