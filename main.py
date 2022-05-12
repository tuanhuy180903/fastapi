from database import db
from fastapi import FastAPI

db.init()
app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.create_all()

@app.on_event("shutdown")
async def shutdown():
    await db.close()

from views import api_fleet, api_fleets, api_vehicle, api_vehicles

app.include_router(api_fleet)
app.include_router(api_fleets)
app.include_router(api_vehicle)
app.include_router(api_vehicles)