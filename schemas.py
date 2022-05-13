from typing import Optional
from pydantic import BaseModel

class Fleet(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Vehicle(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True

class Driver(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class RouteDetail(BaseModel):
    route_id: int
    vehicle_id: int
    driver_id: int

    class Config:
        orm_mode = True


class Route(BaseModel):
    id: int
    name: str
    routedetail: Optional[RouteDetail] = None

    class Config:
        orm_mode = True

