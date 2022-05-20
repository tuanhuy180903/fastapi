import pytest, json
from starlette.testclient import TestClient

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)

from models import *
from main import app

client = TestClient(app)
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

def test_fleet_get(test_app, monkeypatch):
    test_data = [{"id":6,"name":"string"},{"id":1,"name":"qqq"},{"id":4,"name":"aaa"}]

    async def mock_get():
        return test_data

    monkeypatch.setattr(Fleet, "get_all", mock_get)

    response = test_app.get("/fleets")
    assert response.status_code == 200
    assert response.json() == test_data