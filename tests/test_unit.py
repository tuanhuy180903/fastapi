import pytest, json
from starlette.testclient import TestClient

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)

from models import *
from main import app

#client = TestClient(app)
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

def test_fleet_get_all(test_app, monkeypatch):
    test_data = [
        {"name": "ABC", "id": 1}, {"name": "DEF", "id": 2},
        {"name": "GHI", "id": 3 }, {"name": "JKL", "id": 4}
    ]
    async def mock_get():
        return test_data

    monkeypatch.setattr(Fleet, "get_all", mock_get)

    response = test_app.get("/fleet")
    assert response.status_code == 200
    assert response.json() == test_data

def test_fleet_create(test_app, monkeypatch):
    test_payload = {"id": "5", "name": "QQQ"}
    
    async def mock_post(Fleet):
        return 1

    monkeypatch.setattr(Fleet, "create", mock_post)

    response = test_app.post("/fleet/", data=json.dumps(test_payload),)

    assert response.status_code == 201
    assert response.json() == test_payload