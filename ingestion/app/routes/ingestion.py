from fastapi import APIRouter
from app.services.ingestion_service import IngestionService

router = APIRouter()

@router.get("/ingest")
async def ingest():
    return IngestionService.ingest()