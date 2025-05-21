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

    def add_if_match(item, item_type):
        title_norm = normalize(item.title)
        if is_fuzzy_match(keyword_normalized, title_norm):
            relevance = fuzz.partial_ratio(keyword_normalized, title_norm)
            results.append({
                "type": item_type,
                "title": item.title,
                "link": item.link,
                "image_link": item.image_link,
                "price": str(item.price) if item.price else None,
                "category": ", ".join(item.category) if isinstance(item.category, list) else (item.category if item.category else None),
                "relevance": relevance
            })

    for p in db.query(Phone).all():
        add_if_match(p, "phone")

    for t in db.query(TabletDevice).all():
        add_if_match(t, "tablet")

    for a in db.query(Accessory).all():
        add_if_match(a, "accessory")

    
    results.sort(key=lambda x: x["relevance"], reverse=True)


    for r in results:
        r.pop("relevance", None)

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