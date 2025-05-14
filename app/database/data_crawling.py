import feedparser
import json
import os

# Danh sách URL RSS và model tương ứng
rss_urls = {
    "https://mobilecity.vn/rss/dien-thoai.rss": "phones",
    "https://mobilecity.vn/rss/may-tinh-bang.rss": "tablet_devices",
    "https://mobilecity.vn/rss/phu-kien.rss": "accessories"
}

def crawl_rss():
    for url, category in rss_urls.items():
        feed = feedparser.parse(url)
        filename = f"{url.split('/')[-1]}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(feed, f, indent=4, ensure_ascii=False)
        print(f"Đã lưu {filename}")

if __name__ == "__main__":
    crawl_rss()