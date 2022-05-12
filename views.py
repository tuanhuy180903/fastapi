from site import venv
from fastapi import APIRouter, HTTPException
from models import Fleet, Driver, Vehicle, Route
from typing import List
import schemas

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
async def update_fleet(id:int, fleet: schemas.Fleet):
    fleet = await Fleet.update(id, **fleet.dict())
    return schemas.Fleet.from_orm(fleet)

@api_fleet.delete("/{id}", response_model=bool)
async def delete_fleet(id:int):
    return await Fleet.delete(id)

api_fleets = APIRouter(prefix="/fleets")

@api_fleets.get("/",response_model=List[schemas.Fleet],summary="Get all fleets")
#@api_fleets.get("/",response_model=schemas.Fleet,summary="Get all fleets")
async def get_fleets():
    fleet = await Fleet.get_all()
    return fleet

api_vehicle = APIRouter(prefix="/vehicle")

@api_vehicle.post("/",response_model=schemas.Vehicle)
async def create_vehicle(vehicle: schemas.Vehicle):
    vehicle = await Vehicle.create(**vehicle.dict())
    return schemas.Vehicle.from_orm(vehicle)

@api_vehicle.get("/",response_model=List[schemas.Vehicle])
async def get_vehicle_by_id(id:int):
    vehicle = await Vehicle.filter_by_owner_id(id)
    return vehicle

@api_vehicle.get("/",response_model=List[schemas.Vehicle])
async def get_vehicle_by_name(name:str):
    vehicle = await Vehicle.filter_by_name(name)
    return vehicle

api_vehicles = APIRouter(prefix="/vehicles")

@api_vehicles.get("/",response_model=List[schemas.Vehicle],summary="Get all vehicles")
#@api_vehicles.get("/",response_model=schemas.vehicle,summary="Get all vehicles")
async def get_vehicles():
    vehicle = await Vehicle.get_all()
    return vehicle