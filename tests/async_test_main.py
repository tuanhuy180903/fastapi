import pytest

from httpx import AsyncClient

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)
from main import app

#@pytest.mark.anyio
@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Data": "Hello!"}

async def test_fleet():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/fleet") as ac:
        response = await ac.get("/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Fleet not found"}

async def test_drive():
    return

