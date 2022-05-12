from pydantic import BaseModel

class Fleet(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Vehicle(BaseModel):
    name: str
    owner_id: int

    class Config:
        orm_mode = True

class Driver(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Route(BaseModel):
    name: str

    class Config:
        orm_mode = True

class RouteDetail(BaseModel):
    vehicle_id: int
    route_id: int
    driver_id: int
