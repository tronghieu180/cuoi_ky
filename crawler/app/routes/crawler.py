from fastapi import APIRouter
from app.services.crawler_service import CrawlerService

router = APIRouter()

@router.get("/crawl")
async def crawl():
    return CrawlerService.crawl()