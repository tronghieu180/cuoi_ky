from fastapi import APIRouter

from app.routes import crawler

router = APIRouter()

router.include_router(crawler.router)