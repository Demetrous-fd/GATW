from fastapi import APIRouter

from .frames import router as frames_router
from .auth import router as auth_router
from .docs import create_docs_route

routers = APIRouter()
routers.include_router(frames_router)
routers.include_router(auth_router)
