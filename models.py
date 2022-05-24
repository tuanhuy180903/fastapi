from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, join
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete

from sqlalchemy.future import select
from sqlalchemy.orm import relationship, backref

from database import db, Base

class CoreModel:
    @classmethod
    async def create(cls, **kwargs):
        var = cls(**kwargs)
        db.add(var)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return var

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id==id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return await cls.get(id)

    @classmethod
    async def get_all(cls):
        query = select(cls)
        results = await db.execute(query)
        return results.scalars().all()

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id==id)
        results = await db.execute(query)
        _result = results.scalar()
        #print(_result)
        """ if _result is None:
            name_cls = str(cls)
            raise HTTPException(status_code=404, detail=f"{name_cls[15:(len(name_cls)-2)]} not found") """
        return _result

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id==id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    @classmethod
    async def filter_by_name(cls, name):
        query = select(cls).where(cls.name==name)
        results = await db.execute(query)
        _result = results.scalars().all()
        """ if _result == []:
            name_cls = str(cls)
            raise HTTPException(status_code=404, detail=f"{name_cls[15:(len(name_cls)-2)]} not found") """
        return _result


class Fleet(Base, CoreModel):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    #vehicles = relationship("Vehicle", cascade="delete-orphan", backref="vehicles")
    #vehicle = relationship("Vehicle", back_populates="owner", cascade="delete", passive_deletes=True)
    vehicle = relationship("Vehicle", cascade="delete", passive_deletes=True)
    __mapper_args__ = {"eager_defaults": True}

    """ @classmethod
    async def get_by_name(cls, name):
        query = select(cls).where(cls.name==name)
        results = await db.execute(query)
        _result = results.scalars().all()
        return _result """

class Vehicle(Base, CoreModel):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("fleets.id", ondelete="cascade"))
    #owner = relationship("Fleet", backref=backref("fleets", cascade="delete"))
    #owner = relationship("Fleet", back_populates="vehicle")
    __mapper_args__ = {"eager_defaults": True}

    #route_detail = relationship("RouteDetail", back_populates="vehicle", cascade="delete-orphan")
    route_detail = relationship("RouteDetail", cascade = "delete", passive_deletes=True)

    @classmethod
    async def filter_both(cls,id, name):
        query = select(cls)
        if id:
            query = query.filter(cls.owner_id==id)
        if name:
            query = query.filter(cls.name==name)

        results = await db.execute(query)
        return results.scalars().all()

class Driver(Base, CoreModel):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    #route_detail = relationship("RouteDetail", back_populates="driver", cascade="all, delete-orphan")
    route_detail = relationship("RouteDetail", cascade = "delete", passive_deletes=True)

    @classmethod
    async def get_id_by_name(cls, name):
        query = select(cls.id).where(cls.name==name)
        results = await db.execute(query)
        _result = results.scalars().all()
        print(_result)
        if _result == []:
            raise HTTPException(status_code=404, detail="Driver not found")
        return _result

class Route(Base, CoreModel):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    #route_detail = relationship("RouteDetail", back_populates="route", cascade="all, delete-orphan")
    route_detail = relationship("RouteDetail", cascade = "delete", passive_deletes=True)

    @classmethod
    async def get_id_by_name(cls, name):
        query = select(cls.id).where(cls.name==name)
        results = await db.execute(query)
        _result = results.scalars().all()
        print(_result)
        if _result == []:
            raise HTTPException(status_code=404, detail="Driver not found")
        return _result

class RouteDetail(Base, CoreModel):
    __tablename__ = "routedetail"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))

    route = relationship("Route", back_populates="route_detail")
    vehicle = relationship("Vehicle", back_populates="route_detail")
    driver = relationship("Driver", back_populates="route_detail")

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.route_id==id)
        results = await db.execute(query)
        _result = results.scalars().all()
        return _result
    
    @classmethod
    async def get_driver_id(cls, id):
        query = select(cls).where(cls.driver_id==id)
        results = await db.execute(query)
        _result = results.scalars().all()
        """ if _result == []:
            raise HTTPException(status_code=404, detail="Route not found") """
        return _result
    
    @classmethod
    async def get_vehicle_id(cls, id):
        query = select(cls).where(cls.vehicle_id==id)
        results = await db.execute(query)
        _result = results.scalars().all()
        """ if _result == []:
            raise HTTPException(status_code=404, detail="Route not found") """
        return _result

    @classmethod
    async def join_route(cls, route_name,vehicle_name, driver_name):
        if not (route_name or driver_name or vehicle_name):
            return []

        _join = join(cls, Route, cls.route_id==Route.id).join(Vehicle, cls.vehicle_id==Vehicle.id).join(Driver, cls.driver_id==Driver.id)
        
        if route_name:
            if vehicle_name:
                if driver_name:
                    query = select(cls).select_from(_join).where(Route.name==route_name,Vehicle.name==vehicle_name, Driver.name==driver_name)
                else:
                    query = select(cls).select_from(_join).where(Route.name==route_name,Vehicle.name==vehicle_name)
            else:
                if driver_name:
                    query = select(cls).select_from(_join).where(Route.name==route_name,Driver.name==driver_name)
                else:
                    query = select(cls).select_from(_join).where(Route.name==route_name)
        elif vehicle_name:
            if driver_name:
                query = select(cls).select_from(_join).where(Driver.name==driver_name,Vehicle.name==vehicle_name)
            else:
                query = select(cls).select_from(_join).where(Vehicle.name==vehicle_name)
        else:
            query = select(cls).select_from(_join).where(Driver.name==driver_name)

        results = await db.execute(query)
        print(results)
        return results.scalars().all()

    @classmethod
    async def get_by_name(cls, route_name, vehicle_name, driver_name):

        _join = join(cls, Route, cls.route_id==Route.id
        ).join(Vehicle, cls.vehicle_id==Vehicle.id
        ).join(Driver, cls.driver_id==Driver.id)
    
        query = select(cls).select_from(_join)        
        if route_name:
            query = query.filter(Route.name==route_name)
        if vehicle_name:
            query = query.filter(Vehicle.name==vehicle_name)
        if driver_name:
            query = query.filter(Driver.name==driver_name)

        results = await db.execute(query)
        return results.scalars().all()
        
    @classmethod
    async def delete_id(cls,route_id, vehicle_id, driver_id):
        query = sqlalchemy_delete(cls).where(cls.route_id==route_id, cls.vehicle_id==vehicle_id, cls.driver_id==driver_id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True