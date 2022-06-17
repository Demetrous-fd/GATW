from datetime import datetime

import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from backend.config import settings
from backend.database import metadata

Frame = sqlalchemy.Table(
    "inbox",
    metadata,
    sqlalchemy.Column("request_code", UUID, nullable=False),
    sqlalchemy.Column("filename", sqlalchemy.String(64), nullable=False),
    sqlalchemy.Column("create_at", sqlalchemy.DateTime, default=datetime.now(), nullable=False)
)