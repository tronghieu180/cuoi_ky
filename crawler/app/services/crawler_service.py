import os
import json
import asyncio
import logging
from datetime import datetime

import feedparser
import requests


LANDING_ZONE_PATH = "/landing_zone"

SMARTPHONE_RSS_URL = "https://mobilecity.vn/rss/dien-thoai.rss"
TABLET_URL = "https://mobilecity.vn/rss/may-tinh-bang.rss"
ACCESSORIES_URL = "https://mobilecity.vn/rss/phu-kien.rss"

INGESTION_SERVICE_URL = os.getenv("INGESTION_SERVICE_URL")


class CrawlerService:
    @staticmethod
    async def crawl_phones():
        feed = feedparser.parse(SMARTPHONE_RSS_URL)
        file_name = f"smartphone_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(f"{LANDING_ZONE_PATH}/{file_name}", "w", encoding="utf-8") as f:
            json.dump(feed, f, indent=4, ensure_ascii=False)

        requests.post(f"{INGESTION_SERVICE_URL}/phone", json={"filename": file_name})

        return file_name
    
    @staticmethod
    async def crawl_tablets():
        feed = feedparser.parse(TABLET_URL)
        file_name = f"tablet_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(f"{LANDING_ZONE_PATH}/{file_name}", "w", encoding="utf-8") as f:
            json.dump(feed, f, indent=4, ensure_ascii=False)

        requests.post(f"{INGESTION_SERVICE_URL}/tablet", json={"filename": file_name})

        return file_name

    @staticmethod
    async def crawl_accessories():
        feed = feedparser.parse(ACCESSORIES_URL)
        file_name = f"accessories_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(f"{LANDING_ZONE_PATH}/{file_name}", "w", encoding="utf-8") as f:
            json.dump(feed, f, indent=4, ensure_ascii=False)

        requests.post(f"{INGESTION_SERVICE_URL}/accessory", json={"filename": file_name})

        return file_name
    
    @staticmethod
    async def crawl():
        logging.basicConfig(level=logging.INFO)
        logging.info("Start crawling")
        
        results = await asyncio.gather(
            CrawlerService.crawl_phones(),
            CrawlerService.crawl_tablets(),
            CrawlerService.crawl_accessories()
        )

        logging.info("Finished")

        requests.post(f"{INGESTION_SERVICE_URL}/clean")

        return results