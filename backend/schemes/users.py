import uuid
from typing import Optional

from pydantic import Field
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    email: str = Field(..., alias="username")

    class Config:
        allow_population_by_field_name = True


class UserCreate(schemas.BaseUserCreate):
    email: str = Field(..., alias="username")


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[str] = Field(None, alias="username")
