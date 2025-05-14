import feedparser
import json
from datetime import datetime

LANDING_ZONE_PATH = "/landing_zone"
SMARTPHONE_RSS_URL = "https://mobilecity.vn/rss/dien-thoai.rss"
TABLET_URL = "https://mobilecity.vn/rss/may-tinh-bang.rss"
ACCESSORIES_URL = "https://mobilecity.vn/rss/phu-kien.rss"

class CrawlerService:
    @staticmethod
    def crawl_smartphone():
        rss = feedparser.parse(SMARTPHONE_RSS_URL)
        items = rss["items"]
        data = []

        for item in items:
            data.append({
                "title": item["title"],
                "link": item["link"],
                "summary": item["summary"],
                "category": [tag["term"] for tag in item["tags"]],
                "price": item["price"],
                "price_hn": item["price-hn"],
                "price_dn": item["price-dn"],
                "price_hcm": item["price-hcm"],
            })

        file_name = f"{LANDING_ZONE_PATH}/smartphone_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return file_name
    
    @staticmethod
    def crawl_tablet():
        rss = feedparser.parse(TABLET_URL)
        items = rss["items"]
        data = []

        for item in items:
            data.append({
                "title": item["title"],
                "link": item["link"],
                "summary": item["summary"],
                "category": [tag["term"] for tag in item["tags"]],
                "price": item["price"],
            })

        file_name = f"{LANDING_ZONE_PATH}/tablet_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return file_name

    @staticmethod
    def crawl_accessories():
        rss = feedparser.parse(ACCESSORIES_URL)
        items = rss["items"]
        data = []

        for item in items:
            data.append({
                "title": item["title"],
                "link": item["link"],
                "summary": item["summary"],
                "category": [tag["term"] for tag in item["tags"]],
                "price": item["price"],
            })

        file_name = f"{LANDING_ZONE_PATH}/accessories_data_{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return file_name
    
    @staticmethod
    def crawl():
        smarphone_file = CrawlerService.crawl_smartphone()
        tablet_file = CrawlerService.crawl_tablet()
        accessories_file = CrawlerService.crawl_accessories()

        return [smarphone_file, tablet_file, accessories_file]