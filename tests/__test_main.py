from starlette.testclient import TestClient
import json
import pytest

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)
from main import app

from models import CoreModel, Fleet, Vehicle, RouteDetail, Driver, Route

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Data": "Hello!"}

fleet_url = "/fleet/"

""" def test_create_fleet(test_app, monkeypatch):
    test_data = {"id": "2", "name": "asd"}

    def mock_post(**kwargs):
        return test_data

    nguyen.tin1
    phuc.mai
    nguyen.hoang2
    nguyen.khoa
    tan.mai
    thang.tran1

    monkeypatch.setattr(CoreModel, "create", mock_post)

    response = test_app.post("/fleet/", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data """

@pytest.mark.asyncio
def test_get_fleet(event_loop):
    response = client.get(fleet_url + "1")
    assert response.status_code == 200
    assert response.json() == {"id":1, "name":"qqq"}

@pytest.mark.asyncio    
def test_get_no_fleet(event_loop):
    response = client.get(fleet_url + "2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Fleet not found"}

