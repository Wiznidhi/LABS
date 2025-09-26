from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
import uvicorn

from availability import router as r
from bookings import router as br
from auth import router as ar
from rooms_crud import router as rr
from images import router as ir
from pagination import router as pr
from background_tasks import router as btr
from ws import router as wsr
from routers import info
from settings import get_settings
from middleware_and_exceptions import log_requests, value_error_handler
from rate_limit import rate_limit_dependency
from cache_example import expensive_stats

settings = get_settings()
app = FastAPI(title=settings.app_name)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    return await log_requests(request, call_next)

# Exception handler for ValueError
@app.exception_handler(ValueError)
async def value_error_handler_wrapper(request: Request, exc: ValueError):
    return await value_error_handler(request, exc)

# Exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Routers
app.include_router(r, tags=["availability"])
app.include_router(br,tags=["bookings"])
app.include_router(ar,tags=["auth"])
app.include_router(rr, tags=["rooms_crud"])
app.include_router(ir, tags=["images"])
app.include_router(pr, tags=["pagination"])
app.include_router(btr, tags=["background_tasks"])
app.include_router(wsr, tags=["websocket"])
app.include_router(info.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel API!"}

@app.get("/test-error/")
def test_error():
    raise ValueError("This is a test error")

@app.get("/limited-endpoint", dependencies=[Depends(rate_limit_dependency)])
def limited_endpoint():
    return {"message": "Request successful!"}

@app.get("/stats/{year}") 
def stats(year: int): 
    return expensive_stats(year) 

@app.on_event("startup")
def on_startup():
    init_db()

# Run the app
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="localhost", port=8000, reload=True)