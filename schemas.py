from typing import Optional
from pydantic import BaseModel

class FleetBase(BaseModel):
    name: str

class Fleet(FleetBase):
    id: int

    class Config:
        orm_mode = True

class VehicleBase(BaseModel):
    name: str
    owner_id: int

class Vehicle(VehicleBase):
    id: int

    class Config:
        orm_mode = True

class DriverBase(BaseModel):
    name: str

class Driver(DriverBase):
    id: int

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

