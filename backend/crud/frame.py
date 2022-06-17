import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from pydantic import parse_obj_as
from sqlalchemy.sql import Select
from sqlalchemy import select

from backend.schemes import FramesCreate, FramesResult, FrameRead
from backend.models import Frame


class CRUDFrame:
    @staticmethod
    def _select_query(request_code: uuid.UUID) -> Select:
        query = select(
            [
                Frame.columns.filename,
                Frame.columns.create_at
            ]
        ).where(
            Frame.columns.request_code == str(request_code)
        )
        return query

    @staticmethod
    def create(session: Session, frames: FramesCreate) -> FramesResult:
        session.execute(
            Frame.insert(),
            [{"request_code": str(frames.request_code), "filename": filename} for filename in frames.filenames]
        )
        session.commit()
        return FramesResult(**frames.dict())

    @staticmethod
    def read(session: Session, request_code: uuid.UUID) -> list[FrameRead]:
        frames = session.execute(
            CRUDFrame._select_query(request_code)
        ).fetchall()
        return parse_obj_as(list[FrameRead], frames)

    @staticmethod
    async def async_read(session: AsyncSession, request_code: uuid.UUID) -> list[FrameRead]:
        frames = await session.execute(
            CRUDFrame._select_query(request_code)
        )
        return parse_obj_as(list[FrameRead], frames.fetchall())

    @staticmethod
    def update(session: Session) -> None:
        pass

    @staticmethod
    def delete(session: Session, request_code: uuid.UUID) -> None:
        session.execute(
            Frame.delete().where(
                Frame.columns.request_code == str(request_code)
            )
        )
        session.commit()
