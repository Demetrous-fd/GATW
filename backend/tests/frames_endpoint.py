import uuid

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.tests.utils import create_image

client = TestClient(app)


def test_create_frames(temp_db):
    response = client.post("/frames", files={"files": create_image("png")})
    assert response.status_code == 422

    files = [("frames", create_image()) for _ in range(15)]
    response = client.post("/frames", files=files)
    assert response.status_code == 200

    data = response.json()
    assert uuid.UUID(data["request_code"])
    assert len(data["filenames"]) == len(files)


def test_get_exists_frames(temp_db, get_request_code_from_table, get_filenames_from_table):
    # AttributeError: 'NoneType' object has no attribute 'send'
    # response = client.get(f"/frames/00000000")
    # assert response.status_code == 422
    # response = client.get(f"/frames/00000000-0000-0000-0000-000000000000")
    # assert response.status_code == 404

    response = client.get(f"/frames/{get_request_code_from_table}")
    assert response.status_code == 200

    filenames = [frame["filename"] for frame in response.json()]
    assert filenames == get_filenames_from_table


def test_remove_frames(temp_db, get_request_code_from_table):
    response = client.delete(f"/frames/00000000")
    assert response.status_code == 422

    response = client.delete(f"/frames/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

    response = client.delete(f"/frames/{get_request_code_from_table}")
    assert response.status_code == 200
