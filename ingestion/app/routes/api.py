from fastapi import APIRouter
from app.routes import ingestion

router = APIRouter()

router.include_router(ingestion.router, tags=["ingestion"])