import pytest
from pydantic import parse_obj_as

from backend.tests.utils import create_image
from backend.schemes import FramesResult, FrameRead


def test_create_frames(temp_db, api_client, default_credentials):
    response = api_client.post("/frames", files={"files": create_image()})
    assert response.status_code == 401

    response = api_client.post("/frames", files={"test": create_image("png")}, headers=default_credentials)
    assert response.status_code == 422

    response = api_client.post("/frames", files={"frames": create_image("png")}, headers=default_credentials)
    assert response.status_code == 400

    files = [("frames", create_image()) for _ in range(15)]
    response = api_client.post("/frames", files=files, headers=default_credentials)
    assert response.status_code == 200

    data = response.json()
    assert FramesResult.parse_obj(data)
    assert len(data["filenames"]) == len(files)


def test_get_frames(temp_db, api_client, default_credentials, get_request_code_from_table, get_filenames_from_table):
    response = api_client.get(f"/frames/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 401

    response = api_client.get(f"/frames/00000000", headers=default_credentials)
    assert response.status_code == 422

    response = api_client.get(f"/frames/00000000-0000-0000-0000-000000000000", headers=default_credentials)
    assert response.status_code == 404

    response = api_client.get(f"/frames/{get_request_code_from_table}", headers=default_credentials)
    assert response.status_code == 200

    data = response.json()
    assert parse_obj_as(list[FrameRead], data)
    filenames = [frame["filename"] for frame in data]
    assert filenames == get_filenames_from_table


def test_remove_frames(temp_db, api_client, default_credentials, get_request_code_from_table):
    response = api_client.delete(f"/frames/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 401

    response = api_client.delete(f"/frames/00000000", headers=default_credentials)
    assert response.status_code == 422

    response = api_client.delete(f"/frames/00000000-0000-0000-0000-000000000000", headers=default_credentials)
    assert response.status_code == 404

    response = api_client.delete(f"/frames/{get_request_code_from_table}", headers=default_credentials)
    assert response.status_code == 200
