import os
import json
import re
import requests

LANDING_ZONE_PATH = "/landing_zone"

def extract_additional_info(description: str):
    price = None
    dung_luong = None
    mau_sac = None

    # Extract price
    price_match = re.search(r"(?:Giá|Price):\s*(\d{1,3}(?:[\.,]\d{3})*(?:\s*VND)?)", description, re.IGNORECASE)
    if price_match:
        price = price_match.group(1).replace(".", "").replace(",", "") + " VND" if "VND" not in price_match.group(1) else price_match.group(1)

    # Extract dung_luong
    dung_luong_match = re.search(r"(\d+(?:-\d+)?GB)", description)
    if dung_luong_match:
        dung_luong = dung_luong_match.group(1)

    # Extract mau_sac
    mau_sac_match = re.search(r"(Xanh\s*(?:Dương|Lục Bảo|Hoàng Gia)|Đen|Trắng|Vàng|Xám|Đỏ|Cam|Sa Mạc)", description, re.IGNORECASE)
    if mau_sac_match:
        mau_sac = mau_sac_match.group(1)

    return price, dung_luong, mau_sac

def extract_money(value: str):
    return int(value.split()[0])


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
            items = json.load(f)
            for item in items:
                title = item["title"]
                link = item["link"]
                summary = item["summary"]
                image_link = item["image_link"]
                category = item["category"] if item["category"] else ["phones"]

                price = 0 if item["price"] == "VND" else extract_money(item["price"])
                price_hn = extract_money(item["price_hn"])
                price_dn = extract_money(item["price_dn"])
                price_hcm = extract_money(item["price_hcm"])

                _, fallback_dung_luong, fallback_mau_sac = extract_additional_info(summary)
                dung_luong = item["dung_luong"] or fallback_dung_luong or ""
                mau_sac = item["mau_sac"] or fallback_mau_sac or ""

                data.append({
                    "link": link,
                    "title": title,
                    "image_link": image_link,
                    "category": category,
                    "price": price,
                    "price_hn": price_hn,
                    "price_dn": price_dn,
                    "price_dn": price_hcm,
                    "dung_luong": dung_luong,
                    "mau_sac": mau_sac
                })
        
        requests.post(
            "http://db-api:8000/phone",
            json=data,
            headers={"Content-Type": "application/json"},
        )
        # with open(f"{LANDING_ZONE_PATH}/test_phone", "w", encoding="utf-8") as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)

        return "ok"
    
    @staticmethod
    def ingest_tablets(file_name):
        data = IngestionService.ingest_common(file_name)

        requests.post(
            "http://db-api:8000/tablet",
            json=data,
            headers={"Content-Type": "application/json"},
        )
        # with open(f"{LANDING_ZONE_PATH}/test_tablet", "w", encoding="utf-8") as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)

        return "ok"
    
    @staticmethod
    def ingest_accessories(file_name):
        data = IngestionService.ingest_common(file_name)

        requests.post(
            "http://db-api:8000/accessory",
            json=data,
            headers={"Content-Type": "application/json"},
        )
        # with open(f"{LANDING_ZONE_PATH}/test_accessory", "w", encoding="utf-8") as f:
        #     json.dump(data, f, indent=4, ensure_ascii=False)

        return "ok"

    @staticmethod
    def ingest_common(file_name):
        data = []
        path = f"{LANDING_ZONE_PATH}/{file_name}"
        if not os.path.exists(path):
            return
        
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                title = item["title"]
                link = item["link"]
                summary = item["summary"]
                image_link = item["image_link"]
                category = item["category"] if item["category"] else ["phones"]
                price = 0 if item["price"] == "VND" else extract_money(item["price"])

                data.append({
                    "link": link,
                    "title": title,
                    "image_link": image_link,
                    "category": category,
                    "price": price,
                })
        return data