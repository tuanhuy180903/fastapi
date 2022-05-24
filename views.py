from fastapi import APIRouter, HTTPException, Path
from models import Fleet, Driver, RouteDetail, Vehicle, Route
from typing import List, Optional
import schemas

'''Fleet'''

api_fleet = APIRouter(prefix="/fleets", tags=["fleet"])

@api_fleet.get("/", response_model=List[schemas.Fleet], 
    summary="Get all fleets or by its name", description="Leave parameters blank to get all")
async def get_fleet_by_name(name: Optional[str]=None):
    if not name:
        return await Fleet.get_all()
    fleet = await Fleet.filter_by_name(name)
    if fleet is None:
            raise HTTPException(status_code=404, detail=f"Fleet not found")
    return fleet

@api_fleet.get("/{id}", response_model=schemas.Fleet, summary="Get a fleet by ID")
async def get_fleet(id:int = Path(..., gt=0)):
    fleet = await Fleet.get(id)
    if fleet is None:
        raise HTTPException(status_code=404, detail="Fleet not found")
    return schemas.Fleet.from_orm(fleet)

@api_fleet.post("/",response_model=schemas.Fleet, status_code=201, summary="Create a fleet")
async def create_fleet(fleet: schemas.FleetBase):
    '''_dict = fleet.dict()
    fleet_name = await Fleet.get_by_name(_dict["name"])
    if fleet_name:
        raise HTTPException(status_code=409, detail=f"Fleet {_dict['name']} exists")
    """ fleet_id = await Fleet.get(_dict["id"])
    if fleet_id:
        raise HTTPException(status_code=409, detail=f"Fleet {_dict['id']} exists") """
    fleet = await Fleet.create(**_dict)
    #return schemas.Fleet.from_orm(fleet)
    return fleet'''
    return await Fleet.create(**fleet.dict())

@api_fleet.put("/{id}", response_model=schemas.Fleet, summary="Update a fleet")
async def update_fleet(fleet: schemas.FleetBase, id:int = Path(..., gt=0),):
    _fleet = await Fleet.get(id)
    if _fleet is None:
        raise HTTPException(status_code=404, detail="Fleet not found")
    _dict = fleet.dict()
    fleet_name = await Fleet.get_by_name(_dict['name'])
    if fleet_name:
        raise HTTPException(status_code=409, detail=f"Fleet {_dict['name']} exists")
    fleet = await Fleet.update(id, **_dict)
    return schemas.Fleet.from_orm(fleet)

@api_fleet.delete("/{id}", summary="Delete a fleet")
async def delete_fleet(id:int = Path(..., gt=0)):
    fleet = await Fleet.get(id)
    if fleet is None:
        raise HTTPException(status_code=404, detail="Fleet not found")
    await Fleet.delete(id)
    return {"detail": "Delete succesfully"}

api_fleets = APIRouter(prefix="/fleets")
@api_fleets.get("/",response_model=List[schemas.Fleet],summary="Get all fleets")
async def get_fleets():
    fleet = await Fleet.get_all()
    return fleet

'''Vehicle'''

api_vehicle = APIRouter(prefix="/vehicles",tags=["vehicle"])


@api_vehicle.get("/", response_model=List[schemas.Vehicle], 
    summary="Get all vehicles or by their name or by fleet's id",
    description="Leave parameters blank to get all")
async def get_vehicle(owner_id: Optional[int]=None, name:Optional[str]=None):
    if not (owner_id or name):
        return await Vehicle.get_all()

    result = await Vehicle.filter_both(owner_id, name)
    if result == []:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return result

@api_vehicle.get("/{id}", response_model=schemas.Vehicle, summary="Get a vehicle by ID")
async def get_vehicle_id(id:int = Path(..., gt=0)):
    vehicle = await Vehicle.get(id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    #return schemas.Fleet.from_orm(vehicle)
    return vehicle

@api_vehicle.post("/",response_model=schemas.Vehicle,status_code=201, summary="Create a vehicle")
async def create_vehicle(vehicle: schemas.VehicleBase):
    _dict = vehicle.dict()
    result = await Fleet.get(_dict['owner_id'])
    if result is None:
        raise HTTPException(status_code=404, detail=f"Fleet not found")
    """ _id = await Vehicle.get(_dict["id"])
    if _id:
        raise HTTPException(status_code=409, detail=f"Vehicle {_dict['id']} exists")    """ 
    vehicle = await Vehicle.create(**_dict)
    return vehicle

@api_vehicle.put("/{id}", response_model=schemas.Vehicle, summary="Update a vehicle")
async def update_vehicle(vehicle: schemas.VehicleBase, id:int = Path(..., gt=0),):
    _vehicle = await Vehicle.get(id)
    if _vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    vehicle = await Vehicle.update(id, **vehicle.dict())
    return schemas.Vehicle.from_orm(vehicle)

@api_vehicle.delete("/{id}", summary="Delete a vehicle")
async def delete_vehicle(id:int = Path(..., gt=0)):
    vehicle = await Vehicle.get(id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    await Vehicle.delete(id)
    return {"detail": "Delete succesfully"}

api_vehicles = APIRouter(prefix="/vehicles")

@api_vehicles.get("/",response_model=List[schemas.Vehicle],summary="Get all vehicles")
async def get_vehicles():
    vehicle = await Vehicle.get_all()
    return vehicle

'''Driver'''

api_driver = APIRouter(prefix="/drivers",tags=["driver"])

@api_driver.post("/",response_model=schemas.Driver, status_code=201, summary="Create a driver")
async def create_driver(driver: schemas.DriverBase):
    _dict = driver.dict()
    """ _id = await Driver.get(_dict["id"])
    if _id:
        raise HTTPException(status_code=409, detail=f"Driver {_dict['id']} exists")    """ 
    driver = await Driver.create(**_dict)
    return driver

@api_driver.get("/", response_model=List[schemas.Driver], 
    summary="Get all drivers or by their name", description="Leave parameters blank to get all")
async def get_driver_by_name(name: Optional[str]=None):
    if not name:
        return await Driver.get_all()
    driver = await Driver.filter_by_name(name)
    if driver == []:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

@api_driver.get("/{id}", response_model=schemas.Driver, summary="Get a driver by ID")
async def get_driver(id:int = Path(..., gt=0)):
    driver = await Driver.get(id)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return schemas.Driver.from_orm(driver)

@api_driver.put("/{id}", response_model=schemas.Driver, summary="Update a driver")
async def update_driver(driver: schemas.DriverBase, id:int = Path(..., gt=0),):
    _driver = await Driver.get(id)
    if _driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver = await Driver.update(id, **driver.dict())
    return schemas.Driver.from_orm(driver)

@api_driver.delete("/{id}", summary="Delete a driver")
async def delete_driver(id:int = Path(..., gt=0)):
    driver = await Driver.get(id)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    await Driver.delete(id)
    return {"detail": "Delete succesfully"}

api_drivers = APIRouter(prefix="/drivers")
@api_drivers.get("/", response_model=List[schemas.Driver], summary="Get all drivers")
async def get_drivers():
    driver = await Driver.get_all()
    return driver

'''Route'''

api_route = APIRouter(prefix="/routes",tags=["route"])

@api_route.post("/",response_model=schemas.Route, status_code=201, summary="Create a route")
async def create_route(route: schemas.RouteBase):
    _dict = route.dict()
    """ _id = await Route.get(_dict["id"])
    if _id:
        raise HTTPException(status_code=409, detail=f"Route {_dict['id']} exists")   """  
    route = await Route.create(**_dict)
    return route

@api_route.get("/{id}", response_model=schemas.Route, summary="Get a route by ID")
async def get_route(id:int = Path(..., gt=0)):
    route = await Route.get(id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return schemas.Route.from_orm(route)

@api_route.put("/{id}", response_model=schemas.Route, summary="Update a route")
async def update_route(route: schemas.RouteBase, id:int = Path(..., gt=0),):
    _route = await Route.get(id)
    if _route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    route = await Route.update(id, **route.dict())
    return schemas.Route.from_orm(route)

@api_route.delete("/{id}", summary="Delete a route")
async def delete_route(id:int = Path(..., gt=0)):
    route = await Route.get(id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    await Route.delete(id)
    return {"detail": "Delete succesfully"}

@api_route.get("/", response_model=List[schemas.Route], 
    summary="Get all routes or by their name", description="Leave parameters blank to get all")
async def get_route_by_name(name:Optional[str]=None):
    if not name:
        return await Route.get_all()
    routes = await Route.filter_by_name(name)
    if routes == []:
        raise HTTPException(status_code=404, detail="Route not found")
    return routes

api_routes = APIRouter(prefix="/routes")
@api_routes.get("/",response_model=List[schemas.Route],summary="Get all routes")
async def get_routes():
    route = await Route.get_all()
    return route

'''RouteDetail'''

api_routedetail = APIRouter(prefix="/routedetail",tags=["routedetail"])

@api_routedetail.get("/", response_model=List[schemas.RouteDetail], 
    summary="Get all route details or by route's name, vehicle's name or driver's name", 
    description="Leave parameters blank to get all")
async def get_route_detail_by_name(route_name: Optional[str]=None, vehicle_name: Optional[str]=None, driver_name: Optional[str]=None):
    if not (route_name or vehicle_name or driver_name):
        return await RouteDetail.get_all()
    result = await RouteDetail.get_by_name(route_name, vehicle_name, driver_name)
    return result

@api_routedetail.post("/",response_model=schemas.RouteDetail, status_code=201, summary="Create a route detail")
async def create_route_detail(routedetail: schemas.RouteDetail):
    routedetail = await RouteDetail.create(**routedetail.dict())
    return schemas.RouteDetail.from_orm(routedetail)

@api_routedetail.delete("/", summary="Delete a route detail")
async def delete_route_detail(route_id:int, vehicle_id: int, driver_id:int):
    route = await RouteDetail.get_id(route_id)
    if route == []:
        raise HTTPException(status_code=404, detail="Route not found")
    await RouteDetail.delete_id(route_id, vehicle_id, driver_id)
    return {"detail": "Delete succesfully"}

@api_routedetail.get("/{id}", response_model=List[schemas.RouteDetail], summary="Get route details by ID")
async def get_route_detail(id:int = Path(..., gt=0)):
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