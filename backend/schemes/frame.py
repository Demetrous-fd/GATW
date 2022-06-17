import uuid
from datetime import datetime

from pydantic import BaseModel, conlist, Field


class FramesCreate(BaseModel):
    filenames: conlist(str, min_items=1, max_items=15)
    request_code: uuid.UUID = Field(uuid.uuid4())


class FramesResult(FramesCreate):
    pass


class FrameRead(BaseModel):
    filename: str
    create_at: datetime
