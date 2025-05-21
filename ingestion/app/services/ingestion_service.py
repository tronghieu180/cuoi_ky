import os
import json
import re

import requests
import bleach

LANDING_ZONE_PATH = "/landing_zone"
DB_API_URL = os.getenv("DB_API_URL")

def extract_additional_info(description: str):
    price = None
    dung_luong = None
    mau_sac = None

    price_match = re.search(r"(?:Giá|Price):\s*(\d{1,3}(?:[\.,]\d{3})*(?:\s*VND)?)", description, re.IGNORECASE)
    if price_match:
        price = price_match.group(1).replace(".", "").replace(",", "") + " VND" if "VND" not in price_match.group(1) else price_match.group(1)

    dung_luong_match = re.search(r"(\d+(?:-\d+)?GB)", description)
    if dung_luong_match:
        dung_luong = dung_luong_match.group(1)

    mau_sac_match = re.search(r"(Xanh\s*(?:Dương|Lục Bảo|Hoàng Gia)|Đen|Trắng|Vàng|Xám|Đỏ|Cam|Sa Mạc)", description, re.IGNORECASE)
    if mau_sac_match:
        mau_sac = mau_sac_match.group(1)

    return price, dung_luong, mau_sac

def extract_money(value: str):
    return int(value.split()[0])

def sanitize(value: str):
    return bleach.clean(
        value,
        strip=True
    )


class IngestionService:
    @staticmethod
    def ingest():
        return "ok"
    
    @staticmethod
    def ingest_phones(file_name):
        data = []
        path = f"{LANDING_ZONE_PATH}/{file_name}"
        if not os.path.exists(path):
            return
        
        with open(path, "r", encoding="utf-8") as f:
            feed = json.load(f)
            entries = feed.get("entries", [])
            for entry in entries:
                link = entry.get("link", "")
                if not link:
                    continue
                
                title = sanitize(entry.get("title", ""))
                summary = entry.get("summary", "")
                image_link = entry.get("image_link", "")

                category = [tag["term"] for tag in entry.get("tags", []) if "term" in tag] or ["phones"]

                price = entry.get("price", "0 VND")
                price = 0 if price == "VND" else extract_money(price)
                price_hn = extract_money(entry.get("price-hn", "0 VND"))
                price_dn = extract_money(entry.get("price-dn", "0 VND"))
                price_hcm = extract_money(entry.get("price-hcm", "0 VND"))

                dung_luong = entry.get("dung-luong", None)
                mau_sac = entry.get("mau-sac", None)
                _, fallback_dung_luong, fallback_mau_sac = extract_additional_info(summary)
                dung_luong = dung_luong or fallback_dung_luong or ""
                mau_sac = mau_sac or fallback_mau_sac or ""

                data.append({
                    "link": link,
                    "title": title,
                    "image_link": image_link,
                    "category": category,
                    "price": price,
                    "price_hn": price_hn,
                    "price_dn": price_dn,
                    "price_hcm": price_hcm,
                    "dung_luong": dung_luong,
                    "mau_sac": mau_sac
                })
        
        requests.post(
            f"{DB_API_URL}/phone",
            json=data,
            headers={"Content-Type": "application/json"},
        )

        return "ok"
    
    @staticmethod
    def ingest_tablets(file_name):
        data = IngestionService.ingest_common(file_name, "tablet_devices")

        requests.post(
            f"{DB_API_URL}/tablet",
            json=data,
            headers={"Content-Type": "application/json"},
        )

        return "ok"
    
    @staticmethod
    def ingest_accessories(file_name):
        data = IngestionService.ingest_common(file_name, "accessories")

        requests.post(
            f"{DB_API_URL}/accessory",
            json=data,
            headers={"Content-Type": "application/json"},
        )

        return "ok"

    @staticmethod
    def ingest_common(file_name, main_category):
        data = []
        path = f"{LANDING_ZONE_PATH}/{file_name}"
        if not os.path.exists(path):
            return
        
        with open(path, "r", encoding="utf-8") as f:
            feed = json.load(f)
            entries = feed.get("entries", [])
            for entry in entries:
                link = entry.get("link", "")
                if not link:
                    continue

                title = sanitize(entry.get("title", ""))
                image_link = entry.get("image_link", "")

                category = [tag["term"] for tag in entry.get("tags", []) if "term" in tag] or [main_category]

                price = entry.get("price", "0 VND")
                price = 0 if price == "VND" else extract_money(price)

                data.append({
                    "link": link,
                    "title": title,
                    "image_link": image_link,
                    "category": category,
                    "price": price,
                })
        
        return data