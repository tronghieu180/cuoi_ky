import json
import os
from typing import Dict, Any
import re

# Danh sách URL RSS và model tương ứng (dùng tên bảng)
rss_urls = {
    "https://mobilecity.vn/rss/dien-thoai.rss": "phones",
    "https://mobilecity.vn/rss/may-tinh-bang.rss": "tablet_devices",
    "https://mobilecity.vn/rss/phu-kien.rss": "accessories"
}

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

def ingest_data() -> Dict[str, list]:
    data_to_ingest = {}
    for url, category in rss_urls.items():
        filename = f"{url.split('/')[-1]}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                feed = json.load(f)
                entries = []
                for entry in feed.get("entries", []):
                    link = entry.get("link", "")
                    if not link:
                        continue

                    title = entry.get("title", "")
                    image_link = entry.get("image_link", "") or entry.get("image", {}).get("href", "")
                    summary = entry.get("summary", "")

                    term = next((tag["term"] for tag in entry.get("tags", []) if "term" in tag), category)
                    print(f"Tag term for {link}: {term}") 

                    if category == "phones":
                        mapped_category = "phones"
                    elif category == "tablet_devices":
                        mapped_category = "tablet_devices"
                    else:
                        mapped_category = "accessories"


                    category_value = term


                    if mapped_category == "phones":
                        dung_luong = entry.get("dung-luong", None)
                        mau_sac = entry.get("mau-sac", None)
                        _, fallback_dung_luong, fallback_mau_sac = extract_additional_info(summary)
                        dung_luong = dung_luong or fallback_dung_luong
                        mau_sac = mau_sac or fallback_mau_sac

                        price_hn = entry.get("price-hn", "0 VND")
                        price_hcm = entry.get("price-hcm", "0 VND")
                        price_dn = entry.get("price-dn", "0 VND")
                        price = next((p for p in [price_hn, price_hcm, price_dn] if p != "0 VND"), None)
                        if not price:
                            price, _, _ = extract_additional_info(summary)
                            if not price:
                                price = "0 VND"

                        entries.append({
                            "link": link,
                            "title": title,
                            "image_link": image_link,
                            "price": price,
                            "category": category_value,
                            "price_hn": price_hn,
                            "price_hcm": price_hcm,
                            "price_dn": price_dn,
                            "dung_luong": dung_luong,
                            "mau_sac": mau_sac
                        })


                    else:
                        price = entry.get("price", None)
                        if price is None or price == "":
                            price, _, _ = extract_additional_info(summary)
                        if not price:
                            price = "0 VND"

                        entries.append({
                            "link": link,
                            "title": title,
                            "image_link": image_link,
                            "price": price,
                            "category": category_value
                        })

                data_to_ingest[mapped_category] = entries
        else:
            print(f"⚠️ File {filename} không tồn tại.")
    return data_to_ingest

if __name__ == "__main__":
    data = ingest_data()
    print("Dữ liệu đã sẵn sàng để gửi đến Database API:", data)