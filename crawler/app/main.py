import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from app.routes import api
from app.services.crawler_service import CrawlerService

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()

    hour = os.getenv("CRAWL_HOUR")
    minute = os.getenv("CRAWL_MINUTE")

    scheduler.add_job(CrawlerService.crawl, "cron", hour=hour, minute=minute, id="crawl")
    scheduler.start()
    yield
    scheduler.shutdown()


def get_application():
    app = FastAPI(
        lifespan=lifespan,
        root_path="/crawler",
        docs_url="/docs",
        openapi_url="/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(api.router)
    return app

app = get_application()