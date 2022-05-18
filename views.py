from http.client import HTTPException
from fastapi import APIRouter
from models import Fleet, Driver, RouteDetail, Vehicle, Route
from typing import List, Optional
import schemas

'''Fleet'''

api_fleet = APIRouter(prefix="/fleet")

@api_fleet.post("/",response_model=schemas.Fleet)
async def create_fleet(fleet: schemas.Fleet):
    fleet = await Fleet.create(**fleet.dict())
    return schemas.Fleet.from_orm(fleet)

@api_fleet.get("/", response_model=List[schemas.Fleet])
async def get_fleet_by_name(name: str):
    fleet = await Fleet.filter_by_name(name)
    return fleet

@api_fleet.get("/{id}", response_model=schemas.Fleet)
async def get_fleet(id:int):
    fleet = await Fleet.get(id)
    return schemas.Fleet.from_orm(fleet)

@api_fleet.put("/{id}", response_model=schemas.Fleet)
async def update_fleet(id:int, fleet: schemas.FleetBase):
    await Fleet.get(id)
    fleet = await Fleet.update(id, **fleet.dict())
    return schemas.Fleet.from_orm(fleet)

@api_fleet.delete("/{id}", response_model=bool)
async def delete_fleet(id:int):
    await Fleet.get(id)
    return await Fleet.delete(id)

api_fleets = APIRouter(prefix="/fleets")
@api_fleets.get("/",response_model=List[schemas.Fleet],summary="Get all fleets")
async def get_fleets():
    fleet = await Fleet.get_all()
    return fleet

'''Vehicle'''

api_vehicle = APIRouter(prefix="/vehicle")

@api_vehicle.post("/",response_model=schemas.Vehicle)
async def create_vehicle(vehicle: schemas.Vehicle):
    vehicle = await Vehicle.create(**vehicle.dict())
    return schemas.Vehicle.from_orm(vehicle)

@api_vehicle.put("/{id}", response_model=schemas.Vehicle)
async def update_vehicle(id:int, vehicle: schemas.VehicleBase):
    vehicle = await Vehicle.update(id, **vehicle.dict())
    return schemas.Vehicle.from_orm(vehicle)

@api_vehicle.delete("/{id}", response_model=bool)
async def delete_vehicle(id:int):
    return await Vehicle.delete(id)

""" @api_vehicle.get("/",response_model=List[schemas.Vehicle], summary="Get vehicle by fleet's ID")
async def get_vehicle_by_owner_id(id:int):
    vehicle = await Vehicle.filter_by_owner_id(id)
    return vehicle

@api_vehicle.get("/",response_model=List[schemas.Vehicle])
async def get_vehicle_by_name(name:str):
    vehicle = await Vehicle.filter_by_name(name)
    return vehicle """

api_vehicles = APIRouter(prefix="/vehicles")

@api_vehicles.get("/",response_model=List[schemas.Vehicle],summary="Get all vehicles")
async def get_vehicles():
    vehicle = await Vehicle.get_all()
    return vehicle

@api_vehicle.get("/", response_model=List[schemas.Vehicle])
async def get_vehicle(id: Optional[int]=None, name:Optional[str]=None):
    if id:
        vehicle = await Vehicle.filter_by_owner_id(id)
        return vehicle
    if name:
        vehicle = await Vehicle.filter_by_name(name)
        return vehicle

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
async def update_driver(id:int, driver: schemas.DriverBase):
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

@api_route.get("/", response_model=schemas.Route)
async def get_route_by_name(name:str):
    _list = []
    routes = await Route.filter_by_name(name)
    for route in routes:
        _id = schemas.Route.from_orm(route).id
        routedetail = await RouteDetail.get_id(_id)
        print(routedetail)
    print(routes)
    #routes.append(routedetail)
    #print(route.keys())
    return await schemas.Route.from_orm(routes)

api_routes = APIRouter(prefix="/routes")
@api_routes.get("/",response_model=List[schemas.Route],summary="Get all routes")
async def get_routes():
    route = await Route.get_all()
    return route

'''RouteDetail'''

api_routedetail = APIRouter(prefix="/routedetail")

@api_routedetail.post("/",response_model=schemas.RouteDetail)
async def create_routedetail(routedetail: schemas.RouteDetail):
    routedetail = await RouteDetail.create(**routedetail.dict())
    kk = schemas.RouteDetail.construct(routedetail)
    print('kk=',kk)
    return schemas.RouteDetail.from_orm(routedetail)

@api_routedetail.get("/", response_model=List[schemas.RouteDetail])
async def get_routedetail_by_name(name: str):
    routedetail = await RouteDetail.filter_by_name(name)
    return RouteDetail

@api_routedetail.get("/{id}", response_model=schemas.RouteDetail)
async def get_routedetail(id:int):
    routedetail = await RouteDetail.get(id)
    return schemas.RouteDetail.from_orm(routedetail)

@api_routedetail.put("/{id}", response_model=schemas.RouteDetail)
async def update_routedetail(id:int, routedetail: schemas.RouteDetail):
    routedetail = await RouteDetail.update(id, **RouteDetail.dict())
    return schemas.RouteDetail.from_orm(routedetail)

@api_routedetail.delete("/{id}", response_model=bool)
async def delete_routedetail(id:int):
    return await RouteDetail.delete_id(id)

api_routedetails = APIRouter(prefix="/routedetails")
@api_routedetails.get("/",response_model=List[schemas.RouteDetail],summary="Get all RouteDetails")
async def get_routedetails():
    routedetail = await RouteDetail.get_all()
    return routedetail