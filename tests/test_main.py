import pytest
import json
from httpx import AsyncClient

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'fastapi')))
print(sys.path)

from main import app

pytestmark = pytest.mark.anyio
base_url = "http://127.0.0.1:8000"

async def test_root():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Data": "Hello!"}

"""Fleet"""

async def test_create_fleet(event_loop):
    test_data = {"id": 3, "name": "eee"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/fleet/", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data

async def test_get_fleet(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/fleet/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Fleet not found"}

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
    assert response.json() == {"detail": "Delete succesfully"}

async def test_get_fleet_by_name(event_loop):
    test_data = {"id": 4, "name": "aaa"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/fleet/?name=aaa")
    assert response.status_code == 200
    assert response.json() == test_data
    

fleet_list = [{"id":6,"name":"string"},{"id":1,"name":"qqq"},{"id":4,"name":"aaa"},]
async def test_get_fleets(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/fleets/")
    assert response.status_code == 200
    assert response.json() == fleet_list

"""Vehicle"""

async def test_create_vehicle(event_loop):
    test_data = {"name": "eee", "owner_id": 6, "id": 3}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/vehicle/", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data

async def test_update_vehicle(event_loop):
    test_data = {"name": "rrr", "owner_id": 6, "id":3}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put("/vehicle/3", data=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == test_data

async def test_delete_vehicle(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("/vehicle/3")
    assert response.status_code == 200
    assert response.json() == {"detail": "Delete succesfully"}

async def test_get_vehicle_by_name(event_loop):
    test_data = [
        {"name": "aaa", "owner_id": 1, "id": 2},
        {"name": "aaa", "owner_id": 4, "id": 4}
    ]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/vehicle/?name=aaa")
    assert response.status_code == 200
    assert response.json() == test_data

async def test_get_vehicle_by_fleet_id(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/vehicle/?owner_id=2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}

    test_data = [
        {"name": "aaa", "owner_id": 1, "id": 2},
        {"name": "bbb", "owner_id": 1, "id": 1}
    ]

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/vehicle/?owner_id=1")
    assert response.status_code == 200
    assert response.json() == test_data

    test_data_2 = [{"name": "aaa", "owner_id": 1, "id": 2}]

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/vehicle/?owner_id=1&name=aaa")
    assert response.status_code == 200
    assert response.json() == test_data_2

vehicle_list = [
    {'name': 'aaa', 'owner_id': 1, 'id': 2}, 
    {'name': 'aaa', 'owner_id': 4, 'id': 4}, 
    {'name': 'asdf', 'owner_id': 4, 'id': 5}, 
    {'name': 'bbb', 'owner_id': 1, 'id': 1}
]
async def test_get_vehicles(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/vehicles/")
    assert response.status_code == 200
    assert response.json() == vehicle_list

"""Driver"""

async def test_get_driver(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/driver/5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Driver not found"}

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/driver/2")
    assert response.status_code == 200
    assert response.json() == {"id":2, "name":"www"}

async def test_create_driver(event_loop):
    test_data = {"id": 5, "name": "zzz"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/driver/", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data

async def test_update_driver(event_loop):
    test_data = {"id": 5, "name": "aaa"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put("/driver/5", data=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == test_data

async def test_delete_driver(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("/driver/5")
    assert response.status_code == 200
    assert response.json() == {"detail": "Delete succesfully"}

async def test_get_driver_by_name(event_loop):
    test_data = [{"name": "qqq", "id": 1},{"name": "qqq", "id": 4}]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/driver/?name=qqq")
    assert response.status_code == 200
    assert response.json() == test_data
    
driver_list = [
    {"name": "qqq", "id": 1}, {"name": "www", "id": 2},
    {"name": "eee", "id": 3}, {"name": "qqq", "id": 4}
]

async def test_get_drivers(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/drivers/")
    assert response.status_code == 200
    assert response.json() == driver_list

"""Route"""

async def test_get_route(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/route/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Route not found"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/route/4")
    assert response.status_code == 200
    assert response.json() == {"id":4, "name":"ccc"}

async def test_get_route_by_name(event_loop):
    test_data = [{"name": "eee", "id": 3}]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/route/?name=eee")
    assert response.status_code == 200
    assert response.json() == test_data

async def test_create_route(event_loop):
    test_data = {"id": 5, "name": "zzz"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/route/", data=json.dumps(test_data),)
    assert response.status_code == 201
    assert response.json() == test_data

async def test_update_route(event_loop):
    test_data = {"id": 5, "name": "aaa"}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put("/route/5", data=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == test_data

async def test_delete_route(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("/route/5")
    assert response.status_code == 200
    assert response.json() == {"detail": "Delete succesfully"}

route_list = [{"name": "qqq", "id": 1},{"name": "eee", "id": 3},{"name": "ccc","id": 4}]

async def test_get_routes(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routes/")
    assert response.status_code == 200
    assert response.json() == route_list

"""Route Detail"""

async def test_create_routedetail(event_loop):
    test_data = {"route_id": 4, "vehicle_id": 4, "driver_id": 3}
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/routedetail/", data=json.dumps(test_data))
    assert response.status_code == 201
    assert response.json() == test_data

    
async def test_get_routedetail(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetail/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Route not found"}

    test_data = [{"route_id": 3, "vehicle_id": 2, "driver_id": 1}]

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetail/3")
    assert response.status_code == 200
    assert response.json() == test_data

async def test_get_detail_by_name(event_loop):
    test_data_1 = [
        {"route_id": 1,"vehicle_id": 1,"driver_id": 1},
        {"route_id": 1,"vehicle_id": 2,"driver_id": 2}
    ]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetail/?route_name=qqq")
    assert response.status_code == 200
    assert response.json() == test_data_1

    test_data_2 = [{"route_id": 1,"vehicle_id": 2,"driver_id": 2}]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetail/?route_name=qqq&vehicle_name=aaa")
    assert response.status_code == 200
    assert response.json() == test_data_2

    test_data_3 = [
        {"route_id": 1, "vehicle_id": 1, "driver_id": 1},
        {"route_id": 3, "vehicle_id": 2, "driver_id": 1}
    ]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetail/?driver_name=qqq")
    assert response.status_code == 200
    assert response.json() == test_data_3

    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetail/")
    assert response.status_code == 200
    assert response.json() == []

async def test_delete_routedetail(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.delete("/routedetail/?route_id=4&vehicle_id=4&driver_id=3")
    assert response.status_code == 200
    assert response.json() == {"detail": "Delete succesfully"}

route_list = [
    {"route_id": 1,"vehicle_id": 1,"driver_id": 1},
    {"route_id": 1,"vehicle_id": 2,"driver_id": 2},
    {"route_id": 3,"vehicle_id": 2,"driver_id": 1}
]

async def test_get_routes(event_loop):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/routedetails/")
    assert response.status_code == 200
    assert response.json() == route_list













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
