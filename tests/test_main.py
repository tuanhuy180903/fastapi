import pytest
import json

from httpx import AsyncClient

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)
from main import app

pytestmark = pytest.mark.anyio

""" @pytest.fixture(scope="module")
def test_app():
    client = AsyncClient(app)
    yield client """

base_url = "http://127.0.0.1:8000"

async def test_root():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Data": "Hello!"}

async def test_create_fleet(event_loop):
    test_data = {"id": 3, "name": "eee"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/fleet/", data=json.dumps(test_data),)
    assert response.status_code == 200
    assert response.json() == test_data

async def test_fleet(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/fleet/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Fleet not found"}
    
async def test_no_fleet(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/fleet/1")
    assert response.status_code == 200
    assert response.json() == {"id":1, "name":"qqq"}

async def test_update_fleet(event_loop):
    test_data = {"id": 3, "name": "rrr"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put("/fleet/3", data=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == test_data

async def test_delete_fleet(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("/fleet/3")
    assert response.status_code == 200
    assert response.json() == True

fleet_dict = [{"id":6,"name":"string"},{"id":1,"name":"qqq"},{"id":4,"name":"aaa"},]
async def test_get_fleets(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/fleets/")
    assert response.status_code == 200
    assert response.json() == fleet_dict


""" @pytest.mark.anyio
async def test_drive():
    test_data = {"id": "4", "name": "aas"}
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/fleet") as ac:
        response = await ac.get("/4")
    assert response.status_code == 200
    assert response.json() == test_data """

""" @pytest.mark.anyio
async def test_read_fleet(monkeypatch):
    test_data = {"id": "4", "name": "aas"}

    def mock_post(id):
        return test_data

    monkeypatch.setattr(Fleet, "get", mock_post)
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/fleet") as ac:
        response = await ac.get("/4")
    assert response.status_code == 200
    assert response.json() == test_data """

""" async def test_get():
    fleet = await get_fleet(1)

    assert fleet == {"id":1, "name":"qqq"} """
