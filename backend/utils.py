import contextlib
from typing import Iterable, Any
from datetime import date, datetime

from fastapi import UploadFile, FastAPI, status

from backend.database import get_async_session
from backend.security import get_user_db, get_user_manager

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


def validate_upload_files(files: list[UploadFile], content_types: Iterable[str] | None = None) -> bool:
    if content_types is None:
        content_types = ["image/jpeg"]
    filter_rule = lambda file: file.content_type in content_types
    return all(map(filter_rule, files))


def get_date_isoformat(datetime_: datetime | None = None) -> str:
    _date = date.today()
    if datetime_:
        _date = datetime_.date()
    return _date.isoformat().replace("-", "")


def extend_openapi(app: FastAPI) -> dict[str, Any]:
    openapi_schema = app.openapi()
    register_schema = openapi_schema["paths"]["/auth/register"]
    register_schema["post"]["responses"].update(
        {status.HTTP_403_FORBIDDEN: {"description": "Not a superuser."}}
    )

    return openapi_schema
