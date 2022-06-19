from pathlib import Path
import os

os.environ['TESTING'] = "True"

import pytest
from sqlalchemy_utils import create_database, drop_database
from alembic.config import Config
from sqlalchemy import select
from alembic import command
from multiprocessing import Process
import uvicorn
import httpx

from backend.database import SessionLocal
from backend.config import settings
from backend.models import Frame
from backend.app import app


def run_server():
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT
    )


@pytest.fixture(scope="module")
def server():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    yield
    proc.kill() # Cleanup after test


@pytest.fixture(scope="module")
def temp_db(server):
    create_database(
        settings.POSTGRES_URL,
        template="template0"
    )
    alembic_cfg = Path(__file__).resolve().parent.parent.parent / "alembic.ini"
    alembic_cfg = Config(str(alembic_cfg))
    try:
        command.upgrade(alembic_cfg, "b91b0987b75d")
        command.upgrade(alembic_cfg, "head")

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


@pytest.fixture
def api_client():
    with httpx.Client(base_url=f"http://{settings.APP_HOST}:{settings.APP_PORT}") as client:
        yield client


@pytest.fixture
def default_credentials(api_client):
    response = api_client.post(
        "/auth/jwt/login",
        data={
            "username": settings.APP_DEFAULT_USER,
            "password": settings.APP_DEFAULT_PASSWORD
        }
    )
    access_token = response.json()["access_token"]
    header = {
        "Authorization": f"Bearer {access_token}"
    }
    return header
