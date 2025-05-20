from fastapi import APIRouter

from app.services.crawler_service import CrawlerService

router = APIRouter(
    tags=["crawler"]
)

@router.get("/crawl")
async def crawl():
    results = await CrawlerService.crawl()
    return results