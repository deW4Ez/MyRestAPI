from telnetlib import SE
from typing import Union
from typing import List
from urllib import response

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/vuz/", response_model=schemas.VUZ)
def create_vuz(vuz: schemas.VUZCreate, db: Session = Depends(get_db)):
    db_user = crud.get_vuz_by_name(db, name=vuz.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_vuz(db=db, vuz=vuz)

@app.get("/vuz/budget/", response_model = List[schemas.VUZ])
def get_vuz_by_params(mark: int = None, city: str = None, db: Session = Depends(get_db)):
    return crud.get_by_params(db=db,mark=mark,city=city,budget=True)

@app.get("/vuz/paid/", response_model = List[schemas.VUZ])
def get_vuz_by_params(mark: int = None, city: str = None, db: Session = Depends(get_db)):
    return crud.get_by_params(db=db,mark=mark,city=city,budget=False)

@app.get("/all_vuz/", response_model=List[schemas.VUZ])
def read_all_vuz(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_vuz(db, skip=skip, limit=limit)
    return users

@app.get("/vuz/{vuz_id}", response_model=schemas.VUZ)
def read_vuz(vuz_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_vuz(db, vuz_id=vuz_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Vuz not found")
    return db_user

@app.delete("/vuz/{vuz_id}", response_model = dict)
def delete_vuz(vuz_id:int, db: Session = Depends(get_db)):
    db_vuz = crud.get_vuz(db, vuz_id=vuz_id)
    if db_vuz is None:
        raise HTTPException(status_code=404, detail="Vuz not found")
    crud.delete_vuz(db, db_vuz)
    return {"status": "ok"}

@app.put("/vuz/{vuz_id}", response_model = schemas.VUZ)
def update_vuz(vuz_id: int, vuz: schemas.VUZCreate ,db:Session = Depends(get_db)):
    curr_vuz = crud.get_vuz(db=db,vuz_id=vuz_id)
    if curr_vuz is None:
        raise HTTPException(status_code=404, detail="Vuz not found")
    curr_vuz = crud.update_vuz(db=db, vuz=vuz ,vuz_id=vuz_id)
    return curr_vuz


    
