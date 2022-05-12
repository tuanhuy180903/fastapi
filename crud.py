from sqlalchemy.orm import Session
import models, schemas

#Fleet

def get_fleet(db: Session, fleet_id: int):
    return db.query(models.Fleet).filter(models.Fleet.id == fleet_id).first()

def get_fleet_name(db: Session, name:str):
    return db.query(models.Fleet).filter(models.Fleet.name == name).first()

def get_fleets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Fleet).offset(skip).limit(limit).all()

def create_fleet(db: Session, fleet: schemas.Fleet):
    db_fleet = models.Fleet(name=fleet.name)
    db.add(db_fleet)
    db.commit()
    db.refresh(db_fleet)
    return db_fleet

def update_fleet(db: Session, fleet_id: int, fleet:schemas.Fleet):
    db_fleet = get_fleet(db, fleet_id=fleet_id)
    db_fleet.name = fleet.name
    db.commit()
    db.refresh(db_fleet)
    return db_fleet

def delete_fleet(db: Session, fleet_id: int):
    db_fleet = get_fleet(db, fleet_id=fleet_id)
    db.delete(db_fleet)
    db.commit()
    return db_fleet