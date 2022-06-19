from fastapi import APIRouter

from backend.security import fastapi_users, auth_backend, current_admin
from backend.schemes.users import UserRead, UserUpdate, UserCreate
from fastapi import Depends
from fastapi.openapi.docs import get_swagger_ui_html

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(current_admin)]
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

