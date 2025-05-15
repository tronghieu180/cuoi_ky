import feedparser
import json
import requests
import asyncio
from datetime import datetime

LANDING_ZONE_PATH = "/landing_zone"
SMARTPHONE_RSS_URL = "https://mobilecity.vn/rss/dien-thoai.rss"
TABLET_URL = "https://mobilecity.vn/rss/may-tinh-bang.rss"
ACCESSORIES_URL = "https://mobilecity.vn/rss/phu-kien.rss"

class CrawlerService:
    @staticmethod
    async def crawl_phones():
        rss = feedparser.parse(SMARTPHONE_RSS_URL)
        items = rss.entries
        data = []

        for item in items:
            data.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "summary": item.get("summary", ""),
                "image_link": item.get("image_link", ""),
                "category": [tag.get("term", "") for tag in item.get("tags", [])],
                "price": item.get("price", ""),
                "price_hn": item.get("price-hn", ""),
                "price_dn": item.get("price-dn", ""),
                "price_hcm": item.get("price-hcm", ""),
                "dung_luong": item.get("dung-luong", ""),
                "mau_sac": item.get("mau-sac", "")
            })

        file_name = f"smartphone_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(f"{LANDING_ZONE_PATH}/{file_name}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        requests.post("http://ingestion:8000/phone", json={"filename": file_name})

        return file_name
    
    @staticmethod
    async def crawl_tablets():
        rss = feedparser.parse(TABLET_URL)
        items = rss.entries
        data = []

        for item in items:
            data.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "image_link": item.get("image_link", ""),
                "summary": item.get("summary", ""),
                "category": [tag.get("term", "") for tag in item.get("tags", "")],
                "price": item.get("price", ""),
            })

        file_name = f"tablet_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(f"{LANDING_ZONE_PATH}/{file_name}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        requests.post("http://ingestion:8000/tablet", json={"filename": file_name})

        return file_name

    @staticmethod
    async def crawl_accessories():
        rss = feedparser.parse(ACCESSORIES_URL)
        items = rss.entries
        data = []

        for item in items:
            data.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "image_link": item.get("image_link", ""),
                "summary": item.get("summary", ""),
                "category": [tag.get("term", "") for tag in item.get("tags", "")],
                "price": item.get("price", ""),
            })

        file_name = f"accessories_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(f"{LANDING_ZONE_PATH}/{file_name}", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        requests.post("http://ingestion:8000/accessory", json={"filename": file_name})

        return file_name
    
    @staticmethod
    async def crawl():
        result = await asyncio.gather(
            CrawlerService.crawl_phones(),
            CrawlerService.crawl_tablets(),
            CrawlerService.crawl_accessories()
        )

        return result