from fastapi import FastAPI, APIRouter, Query ,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from typing import Dict, List, Any
from app.database.models import Phone, TabletDevice, Accessory
from app.database.database import get_db
from app.database.schemas import SearchResult
from unidecode import unidecode
from rapidfuzz import fuzz
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


router = APIRouter()


def normalize(text: str) -> str:
    return unidecode(text).lower() if text else ""

def is_fuzzy_match(query: str, text: str, threshold: int = 70) -> bool:
    return fuzz.partial_ratio(query, text) >= threshold


@router.get("/phone")
async def get(db: Session = Depends(get_db)):
    count = db.query(Phone).count()
    samples = db.query(Phone).all()
    return {
        "count": count,
        "data": samples
    }

@router.get("/tablet")
async def get(db: Session = Depends(get_db)):
    count = db.query(TabletDevice).count()
    samples = db.query(TabletDevice).all()
    return {
        "count": count,
        "data": samples
    }

@router.get("/accessory")
async def get(db: Session = Depends(get_db)):
    count = db.query(Accessory).count()
    samples = db.query(Accessory).all()
    return {
        "count": count,
        "data": samples
    }



@router.get("/search", response_model=List[SearchResult])
def search_all(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    keyword_normalized = normalize(keyword)
    results = []

    phones = db.query(Phone).all()
    for p in phones:
        title_norm = normalize(p.title)
        if is_fuzzy_match(keyword_normalized, title_norm):
            results.append({
                "type": "phone",
                "title": p.title,
                "link": p.link,
                "image_link": p.image_link,
                "price": str(p.price) if p.price else None,
                 "category": ", ".join(p.category) if isinstance(p.category, list) else (p.category if p.category else None),
            })

    tablets = db.query(TabletDevice).all()
    for t in tablets:
        title_norm = normalize(t.title)
        if is_fuzzy_match(keyword_normalized, title_norm):
            results.append({
                "type": "tablet",
                "title": t.title,
                "link": t.link,
                "image_link": t.image_link,
                "price": str(t.price) if t.price else None,
                "category": ", ".join(t.category) if isinstance(t.category, list) else (t.category if t.category else None),
            })

    accessories = db.query(Accessory).all()
    for a in accessories:
        title_norm = normalize(a.title)
        if is_fuzzy_match(keyword_normalized, title_norm):
            results.append({
                "type": "accessory",
                "title": a.title,
                "link": a.link,
                "image_link": a.image_link,
                "price": str(a.price) if a.price else None,
                "category": ", ".join(a.category) if isinstance(a.category, list) else (a.category if a.category else None),
            })

    return results


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