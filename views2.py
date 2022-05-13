from fastapi import APIRouter, HTTPException
from models import Driver, Route
from typing import List, Optional
import schemas
'''Driver'''

api_driver = APIRouter(prefix="/driver")

@api_driver.post("/",response_model=schemas.Driver)
async def create_driver(driver: schemas.Driver):
    driver = await Driver.create(**driver.dict())
    return schemas.Driver.from_orm(driver)

@api_driver.get("/", response_model=List[schemas.Driver])
async def get_driver_by_name(name: str):
    driver = await Driver.filter_by_name(name)
    return driver

@api_driver.get("/{id}", response_model=schemas.Driver)
async def get_driver(id:int):
    driver = await Driver.get(id)
    return schemas.Driver.from_orm(driver)

@api_driver.put("/{id}", response_model=schemas.Driver)
async def update_driver(id:int, driver: schemas.Driver):
    driver = await Driver.update(id, **driver.dict())
    return schemas.Driver.from_orm(driver)

@api_driver.delete("/{id}", response_model=bool)
async def delete_driver(id:int):
    return await Driver.delete(id)

api_drivers = APIRouter(prefix="/drivers")
@api_drivers.get("/", response_model=List[schemas.Driver])
async def get_drivers():
    driver = await Driver.get_all()
    return driver

'''Route'''

api_route = APIRouter(prefix="/route")

@api_route.post("/",response_model=schemas.Route)
async def create_route(route: schemas.Route):
    route = await Route.create(**route.dict())
    return schemas.Route.from_orm(route)

@api_route.get("/", response_model=List[schemas.Route])
async def get_route_by_name(name: str):
    route = await Route.filter_by_name(name)
    return route

@api_route.get("/{id}", response_model=schemas.Route)
async def get_route(id:int):
    route = await Route.get(id)
    return schemas.Route.from_orm(route)

@api_route.put("/{id}", response_model=schemas.Route)
async def update_route(id:int, route: schemas.Route):
    route = await Route.update(id, **route.dict())
    return schemas.Route.from_orm(route)

@api_route.delete("/{id}", response_model=bool)
async def delete_route(id:int):
    return await Route.delete(id)

api_routes = APIRouter(prefix="/routes")
@api_routes.get("/",response_model=List[schemas.Route],summary="Get all routes")
async def get_routes():
    route = await Route.get_all()
    return route