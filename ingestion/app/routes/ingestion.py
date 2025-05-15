from fastapi import APIRouter
from app.services.ingestion_service import IngestionService

router = APIRouter()

@router.post("/phone")
async def ingest(payload: dict):
    file_name = payload["filename"]
    return IngestionService.ingest_phones(file_name)

@router.post("/tablet")
async def ingest(payload: dict):
    file_name = payload["filename"]
    return IngestionService.ingest_tablets(file_name)

@router.post("/accessory")
async def ingest(payload: dict):
    file_name = payload["filename"]
    return IngestionService.ingest_accessories(file_name)