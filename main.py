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
def home():
    return {"Data": "Hello!"}

from views import *
apis = [api_fleets, api_fleet, api_vehicles, api_vehicle, api_drivers, api_driver, 
api_routes, api_route, api_routedetails, api_routedetail]

for api in apis:
    app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app=app)