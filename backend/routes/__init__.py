from fastapi import APIRouter

from .frames import router as frames_router

routers = APIRouter()
routers.include_router(frames_router)
