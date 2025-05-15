from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import Dict, List, Any
from app.database.models import Phone, TabletDevice, Accessory
from app.database.database import get_db

router = APIRouter()

@router.get("/phone")
async def get(db: Session = Depends(get_db)):
    count = db.query(Phone).count()
    samples = db.query(Phone).limit(5).all()
    return {
        "count": count,
        "data": samples
    }

@router.get("/tablet")
async def get(db: Session = Depends(get_db)):
    count = db.query(TabletDevice).count()
    samples = db.query(TabletDevice).limit(5).all()
    return {
        "count": count,
        "data": samples
    }

@router.get("/accessory")
async def get(db: Session = Depends(get_db)):
    count = db.query(Accessory).count()
    samples = db.query(Accessory).limit(5).all()
    return {
        "count": count,
        "data": samples
    }


@router.post("/phone")
async def upload_phone(data_list: List[dict], db: Session = Depends(get_db)):
    return upload(Phone, data_list, db)

@router.post("/tablet")
async def upload_tablet(data_list: List[dict], db: Session = Depends(get_db)):
    return upload(TabletDevice, data_list, db)

@router.post("/accessory")
async def upload_accessory(data_list: List[dict], db: Session = Depends(get_db)):
    return upload(Accessory, data_list, db)

def upload(model, data_list: List[dict], db: Session = Depends(get_db)):
    conflict_column = "link"

    stmt = insert(model).values(data_list)

    update_columns = {
        col: stmt.excluded[col]
        for col in data_list[0].keys()
        if col != conflict_column
    }
    
    stmt = stmt.on_conflict_do_update(
        index_elements=[conflict_column],
        set_=update_columns
    )
    db.execute(stmt)
    db.commit()
    
    return "Ok"