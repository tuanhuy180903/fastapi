from fastapi import APIRouter, HTTPException
from models import Fleet, Driver, Vehicle, Route
from typing import List
import schemas

api_fleet = APIRouter(prefix="/fleet")

@api_fleet.post("/",response_model=schemas.Fleet)
async def create_fleet(fleet: schemas.Fleet):
    fleet = await Fleet.create(**fleet.dict())
    return schemas.Fleet.from_orm(fleet)

@api_fleet.get("/", response_model=schemas.Fleet)
async def get_fleet_by_name(name: str):
    fleet = await Fleet.filter_by_name(name)
    return schemas.Fleet.from_orm(fleet)

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
    _list = []
    for i in fleet:
        (k,) = i
        _list.append(k)
        print(k)
    print(_list)
    #return schemas.Fleet.from_orm(fleet)
    return _list
