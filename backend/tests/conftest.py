from pathlib import Path
import os

import pytest

from sqlalchemy_utils import create_database, drop_database
from sqlalchemy import select
from alembic.config import Config
from alembic import command

os.environ['TESTING'] = "True"

from backend.config import settings
from backend.database import SessionLocal
from backend.models import Frame


@pytest.fixture(scope="module")
def temp_db():
    create_database(
        settings.POSTGRES_URL,
        template="template0"
    )
    alembic_cfg = Path(__file__).resolve().parent.parent.parent / "alembic.ini"
    alembic_cfg = Config(str(alembic_cfg))
    command.upgrade(alembic_cfg, "head")

    try:
        yield settings.POSTGRES_URL
    finally:
        drop_database(settings.POSTGRES_URL)


@pytest.fixture(scope='module')
def db_session():
    with SessionLocal.begin() as session:
        yield session


@pytest.fixture(scope="module")
def get_request_code_from_table(db_session) -> str:
    return db_session.execute(select([Frame.columns.request_code])).fetchone()[0]


@pytest.fixture(scope="module")
def get_filenames_from_table(db_session) -> list[str]:
    data = db_session.execute(select([Frame.columns.filename])).fetchall()
    return [frame.filename for frame in data]
