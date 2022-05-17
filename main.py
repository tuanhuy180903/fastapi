import uvicorn
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

@app.get("/")
async def home():
    return {"Data": "Hello!"}

from views import *
apis = [api_fleets, api_fleet, api_vehicles, api_vehicle,  api_drivers, api_driver, 
api_routes, api_route, api_routedetails, api_routedetail]

for api in apis:
    app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app=app)





""" app.include_router(api_fleet)
app.include_router(api_fleets)
app.include_router(api_vehicle)
app.include_router(api_vehicles)
app.include_router(api_driver)
app.include_router(api_drivers)
app.include_router(api_route)
app.include_router(api_routes)
app.include_router(api_routedetail)
app.include_router(api_routedetails) """