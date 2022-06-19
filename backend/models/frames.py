from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, String, DateTime

from backend.database import metadata

Frame = Table(
    "inbox",
    metadata,
    Column("request_code", UUID, nullable=False),
    Column("filename", String(64), nullable=False),
    Column("create_at", DateTime, default=datetime.now(), nullable=False)
)
