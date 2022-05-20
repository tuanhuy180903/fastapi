from fastapi import APIRouter, HTTPException
from models import Fleet, Driver, RouteDetail, Vehicle, Route
from typing import List, Optional
import schemas

'''Fleet'''

api_fleet = APIRouter(prefix="/fleet")

@api_fleet.get("/", response_model=schemas.Fleet)
async def get_fleet_by_name(name: str):
    fleet = await Fleet.get_by_name(name)
    if fleet is None:
            raise HTTPException(status_code=404, detail=f"Fleet not found")
    return fleet

@api_fleet.get("/{id}", response_model=schemas.Fleet)
async def get_fleet(id:int):
    fleet = await Fleet.get(id)
    return schemas.Fleet.from_orm(fleet)

@api_fleet.post("/",response_model=schemas.Fleet, status_code=201)
async def create_fleet(fleet: schemas.Fleet):
    _dict = fleet.dict()
    _fleet = await Fleet.get_by_name(_dict["name"])
    if _fleet:
        raise HTTPException(status_code=409, detail=f"Fleet {_dict['name']} exists")
    fleet = await Fleet.create(**fleet.dict())
    #return schemas.Fleet.from_orm(fleet)
    return fleet

@api_fleet.put("/{id}", response_model=schemas.Fleet)
async def update_fleet(id:int, fleet: schemas.FleetBase):
    await Fleet.get(id)
    fleet = await Fleet.update(id, **fleet.dict())
    return schemas.Fleet.from_orm(fleet)

@api_fleet.delete("/{id}")
async def delete_fleet(id:int):
    await Fleet.get(id)
    await Fleet.delete(id)
    return {"detail": "Delete succesfully"}

api_fleets = APIRouter(prefix="/fleets")
@api_fleets.get("/",response_model=List[schemas.Fleet],summary="Get all fleets")
async def get_fleets():
    fleet = await Fleet.get_all()
    return fleet

'''Vehicle'''

api_vehicle = APIRouter(prefix="/vehicle")


@api_vehicle.get("/", response_model=List[schemas.Vehicle], summary="Get vehicles by name or by fleet's id")
async def get_vehicle(owner_id: Optional[int]=None, name:Optional[str]=None):
    if not (owner_id or name):
        return []

    result = await Vehicle.filter_both(owner_id, name)
    if result == []:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return result

@api_vehicle.get("/{id}", response_model=schemas.Vehicle)
async def get_vehicle_id(id:int):
    vehicle = await Vehicle.get(id)
    return schemas.Fleet.from_orm(vehicle)

@api_vehicle.post("/",response_model=schemas.Vehicle,status_code=201)
async def create_vehicle(vehicle: schemas.Vehicle):
    result = await Fleet.get(vehicle.dict()['owner_id'])
    if result is None:
        raise HTTPException(status_code=404, detail=f"Fleet not found")
    vehicle = await Vehicle.create(**vehicle.dict())
    return vehicle

@api_vehicle.put("/{id}", response_model=schemas.Vehicle)
async def update_vehicle(id:int, vehicle: schemas.VehicleBase):
    vehicle = await Vehicle.update(id, **vehicle.dict())
    return schemas.Vehicle.from_orm(vehicle)

@api_vehicle.delete("/{id}")
async def delete_vehicle(id:int):
    await Vehicle.get(id)
    await Vehicle.delete(id)
    return {"detail": "Delete succesfully"}

api_vehicles = APIRouter(prefix="/vehicles")

@api_vehicles.get("/",response_model=List[schemas.Vehicle],summary="Get all vehicles")
async def get_vehicles():
    vehicle = await Vehicle.get_all()
    return vehicle

'''Driver'''

api_driver = APIRouter(prefix="/driver")

@api_driver.post("/",response_model=schemas.Driver, status_code=201)
async def create_driver(driver: schemas.Driver):
    driver = await Driver.create(**driver.dict())
    return driver

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

@api_driver.delete("/{id}")
async def delete_driver(id:int):
    await Driver.get(id)
    await Driver.delete(id)
    return {"detail": "Delete succesfully"}

api_drivers = APIRouter(prefix="/drivers")
@api_drivers.get("/", response_model=List[schemas.Driver], summary="Get all drivers")
async def get_drivers():
    driver = await Driver.get_all()
    return driver

'''Route'''

api_route = APIRouter(prefix="/route")

@api_route.post("/",response_model=schemas.Route, status_code=201)
async def create_route(route: schemas.Route):
    route = await Route.create(**route.dict())
    return route

@api_route.get("/{id}", response_model=schemas.Route)
async def get_route(id:int):
    route = await Route.get(id)
    return schemas.Route.from_orm(route)

@api_route.put("/{id}", response_model=schemas.Route)
async def update_route(id:int, route: schemas.RouteBase):
    route = await Route.update(id, **route.dict())
    return schemas.Route.from_orm(route)

@api_route.delete("/{id}")
async def delete_route(id:int):
    await Route.get(id)
    await Route.delete(id)
    return {"detail": "Delete succesfully"}

@api_route.get("/", response_model=List[schemas.Route])
async def get_route_by_name(name:str):
    routes = await Route.filter_by_name(name)
    return routes

api_routes = APIRouter(prefix="/routes")
@api_routes.get("/",response_model=List[schemas.Route],summary="Get all routes")
async def get_routes():
    route = await Route.get_all()
    return route

'''RouteDetail'''

api_routedetail = APIRouter(prefix="/routedetail")

@api_routedetail.get("/", response_model=List[schemas.RouteDetail])
async def get_route_detail_by_name(route_name: Optional[str]=None, vehicle_name: Optional[str]=None, driver_name: Optional[str]=None):
    if not (route_name or vehicle_name or driver_name):
        return []
    result = await RouteDetail.get_by_name(route_name, vehicle_name, driver_name)
    return result

@api_routedetail.post("/",response_model=schemas.RouteDetail, status_code=201)
async def create_route_detail(routedetail: schemas.RouteDetail):
    routedetail = await RouteDetail.create(**routedetail.dict())
    return schemas.RouteDetail.from_orm(routedetail)

@api_routedetail.delete("/")
async def delete_route_detail(route_id:int, vehicle_id: int, driver_id:int):
    await RouteDetail.get_id(route_id)
    await RouteDetail.delete_id(route_id, vehicle_id, driver_id)
    return {"detail": "Delete succesfully"}

@api_routedetail.get("/{id}", response_model=List[schemas.RouteDetail])
async def get_route_detail(id:int):
    routedetail = await RouteDetail.get_id(id)
    if routedetail == []:
        raise HTTPException(status_code=404, detail="Route not found")
    return routedetail

api_routedetails = APIRouter(prefix="/routedetails")
@api_routedetails.get("/",response_model=List[schemas.RouteDetail],summary="Get all route details")
async def get_routedetails():
    routedetail = await RouteDetail.get_all()
    return routedetail




""" @api_routedetail.get("/join", response_model=List[schemas.RouteDetail])
async def get_route_detail_by_name_temp(route_name: Optional[str]=None, vehicle_name: Optional[str]=None, driver_name: Optional[str]=None):
    if not (route_name or vehicle_name or driver_name):
        return []

    routedetail = []

    if route_name:
        routes = await Route.get_id_by_name(route_name)
        for route in routes:
            routedetail.extend(await RouteDetail.get_id(route))
        return routedetail

    if vehicle_name:
        vehicles = await Vehicle.get_id_by_name(vehicle_name)
        for vehicle in vehicles:
            routedetail.extend(await RouteDetail.get_vehicle_id(vehicle))
        return routedetail

    drivers = await Driver.get_id_by_name(driver_name)
    for driver in drivers:
        routedetail.extend(await RouteDetail.get_driver_id(driver))
    return routedetail """