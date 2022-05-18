from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete

from sqlalchemy.future import select
from sqlalchemy.orm import relationship, backref

from database import db, Base

class CoreModel:
    @classmethod
    async def create(cls, **kwargs):
        db.add(cls(**kwargs))
        #await db.commit()
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return cls(**kwargs)

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
        _result = results.fetchone()
        if _result is None:
            name_cls = str(cls)
            raise HTTPException(status_code=404, detail=f"{name_cls[15:(len(name_cls)-2)]} not found")
        (result,) = _result
        return result

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
        #print(_result)
        if _result == []:
            name_cls = str(cls)
            raise HTTPException(status_code=404, detail=f"{name_cls[15:(len(name_cls)-2)]} not found")
        return _result


class Fleet(Base, CoreModel):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    #vehicles = relationship("Vehicle", cascade="delete-orphan", backref="vehicles")
    vehicle = relationship("Vehicle", back_populates="owner", cascade="delete", passive_deletes=True)
    __mapper_args__ = {"eager_defaults": True}

class Vehicle(Base, CoreModel):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("fleets.id", ondelete="CASCADE"))
    #owner = relationship("Fleet", backref=backref("fleets", cascade="delete"))
    owner = relationship("Fleet", back_populates="vehicle")
    __mapper_args__ = {"eager_defaults": True}

    route_detail = relationship("RouteDetail", back_populates="vehicle", cascade="all, delete-orphan")

    @classmethod
    async def filter_by_owner_id(cls, owner_id):
        query = select(cls).where(cls.owner_id==owner_id)
        results = await db.execute(query)
        return results.scalars().all()

class Driver(Base, CoreModel):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    route_detail = relationship("RouteDetail", back_populates="driver", cascade="all, delete-orphan")

class Route(Base, CoreModel):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    route_detail = relationship("RouteDetail", back_populates="route", cascade="all, delete-orphan")

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
        _result = results.fetchone()
        if _result is None:
            name_cls = str(cls)
            raise HTTPException(status_code=404, detail=f"{name_cls[15:(len(name_cls)-2)]} not found")
        (result,) = _result
        return result

    @classmethod
    async def delete_id(cls,id):
        query = sqlalchemy_delete(cls).where(cls.route_id==id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True