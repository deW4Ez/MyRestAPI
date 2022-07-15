from operator import mod
from sqlalchemy.orm import Session

import models, schemas


def get_vuz(db: Session, vuz_id: int):
    return db.query(models.University).filter(models.University.id == vuz_id).first()

def get_vuz_by_name(db: Session, name: str):
    return db.query(models.University).filter(models.University.name == name).first()

def get_all_vuz(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.University).offset(skip).limit(limit).all()


def create_vuz(db: Session, vuz: schemas.VUZ):
    
    db_user = models.University(        
        name=vuz.name, 
        avg_rate_free = vuz.avg_rate_free, 
        avg_rate_paid = vuz.avg_rate_paid,
        count_free_place = vuz.count_free_place,
        count_paid_place = vuz.count_paid_place,
        city = vuz.city
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_vuz(db:Session, vuz: schemas.VUZ):
    db.delete(vuz)
    db.commit()
    return db

def get_by_params(db: Session, mark:int, city: str, budget: bool):
    responce = db.query(models.University)    
    if city != None:
        responce = responce.filter(models.University.city == city)
    if mark != None:
        if budget:
            responce = responce.filter(models.University.avg_rate_free != 0, models.University.avg_rate_free <= mark)
        else:
            responce = responce.filter(models.University.avg_rate_paid <= mark)
    return responce.all()

def update_vuz(db:Session, vuz: schemas.VUZCreate ,vuz_id: int):
    curr_vuz = db.query(models.University).filter(models.University.id == vuz_id).first()
    curr_vuz.name = vuz.name
    curr_vuz.avg_rate_free = vuz.avg_rate_free
    curr_vuz.avg_rate_paid = vuz.avg_rate_paid 
    curr_vuz.count_free_place = vuz.count_free_place
    curr_vuz.count_paid_place = vuz.count_paid_place
    db.add(curr_vuz)
    db.commit()
    db.refresh(curr_vuz)
    return curr_vuz