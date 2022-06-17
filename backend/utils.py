from datetime import date, datetime
from typing import Iterable

from fastapi import UploadFile


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
