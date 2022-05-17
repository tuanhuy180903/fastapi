from starlette.testclient import TestClient

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Data": "Hello!"}

def test_fleet():
    response = client.get("/fleet/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Fleet not found"}