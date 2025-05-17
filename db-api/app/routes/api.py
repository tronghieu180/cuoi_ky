from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import Dict, List, Any
from app.database.models import Phone, TabletDevice, Accessory
from app.database.database import get_db
from app.database.schemas import PhoneSearch, TabletDeviceSearch, AccessorySearch
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()

router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
@router.get("/phones", response_model=List[PhoneSearch])
def get_phones(db: Session = Depends(get_db)):
    return db.query(Phone).all()

@router.get("/tabletdevices", response_model=List[TabletDeviceSearch])
def get_tabletdevices(db: Session = Depends(get_db)):
    return db.query(TabletDevice).all()

@router.get("/accessories", response_model=List[AccessorySearch])
def get_accessories(db: Session = Depends(get_db)):
    return db.query(Accessory).all()

@router.get("/phones/{phone_id}", response_model=PhoneSearch)
def get_phone(phone_id: int, db: Session = Depends(get_db)):
    phone = db.query(Phone).filter(Phone.id == phone_id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone

@router.get("/tabletdevices/{tabletdevice_id}", response_model=TabletDeviceSearch)
def get_tabletdevice(tabletdevice_id: int, db: Session = Depends(get_db)):
    tabletdevice = db.query(TabletDevice).filter(TabletDevice.id == tabletdevice_id).first()
    if not tabletdevice:
        raise HTTPException(status_code=404, detail="Tablet Device not found")
    return tabletdevice

@router.get("/accessories/{accessory_id}", response_model=AccessorySearch)
def get_accessory(accessory_id: int, db: Session = Depends(get_db)):
    accessory = db.query(Accessory).filter(Accessory.id == accessory_id).first()
    if not accessory:
        raise HTTPException(status_code=404, detail="Accessory not found")
    return accessory

@router.get("/search_phones", response_model=List[PhoneSearch])
def search_phones(query: str, db: Session = Depends(get_db)):
    return db.query(Phone).filter(
        Phone.title.ilike(f"%{query}%") |
        Phone.category.ilike(f"%{query}%")
    ).all()

@router.get("/search_tabletdevices", response_model=List[TabletDeviceSearch])
def search_tabletdevices(query: str, db: Session = Depends(get_db)):
    return db.query(TabletDevice).filter(
        TabletDevice.title.ilike(f"%{query}%") |
        TabletDevice.category.ilike(f"%{query}%")
    ).all()

@router.get("/search_accessories", response_model=List[AccessorySearch])
def search_accessories(query: str, db: Session = Depends(get_db)):
    return db.query(Accessory).filter(
        Accessory.title.ilike(f"%{query}%") |
        Accessory.category.ilike(f"%{query}%")
    ).all()