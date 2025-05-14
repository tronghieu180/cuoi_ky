import feedparser
import json
import os
import re
from database import SessionLocal, engine, Base
from models import Phone, TabletDevice, Accessory
from sqlalchemy.orm import load_only
import time

# Danh sách URL RSS và model tương ứng
rss_urls = {
    "https://mobilecity.vn/rss/dien-thoai.rss": Phone,
    "https://mobilecity.vn/rss/may-tinh-bang.rss": TabletDevice,
    "https://mobilecity.vn/rss/phu-kien.rss": Accessory
}

# 📌 BƯỚC 1: Tải RSS và lưu thành JSON
def rss_to_json():
    for url in rss_urls.keys():
        feed = feedparser.parse(url)
        filename = f"{url.split('/')[-1]}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(feed, f, indent=4, ensure_ascii=False)
        print(f"Đã lưu {filename}")

# 📌 BƯỚC 2: Hàm trích xuất thông tin phụ (giá, dung lượng, màu sắc) từ summary
def extract_additional_info(description):
    price = None
    dung_luong = None
    mau_sac = None

    # Extract price (specific context to avoid unrelated numbers)
    price_match = re.search(r"(?:Giá|Price):\s*(\d{1,3}(?:[\.,]\d{3})*(?:\s*VND)?)", description, re.IGNORECASE)
    if price_match:
        price = price_match.group(1).replace(".", "").replace(",", "") + " VND" if "VND" not in price_match.group(1) else price_match.group(1)

    # Extract dung_luong (e.g., 16-256GB, 12GB)
    dung_luong_match = re.search(r"(\d+(?:-\d+)?GB)", description)
    if dung_luong_match:
        dung_luong = dung_luong_match.group(1)

    # Extract mau_sac (expanded list of colors)
    mau_sac_match = re.search(r"(Xanh\s*(?:Dương|Lục Bảo|Hoàng Gia)|Đen|Trắng|Vàng|Xám|Đỏ|Cam|Sa Mạc)", description, re.IGNORECASE)
    if mau_sac_match:
        mau_sac = mau_sac_match.group(1)

    return price, dung_luong, mau_sac

# 📌 BƯỚC 3: Đọc file JSON và đồng bộ với DB
def sync_rss_feed(json_filename, model, db):
    with open(json_filename, "r", encoding="utf-8") as f:
        feed = json.load(f)

    # Use the actual ORM attribute (model.link) instead of a string
    existing_links = {item.link for item in db.query(model).options(load_only(model.link))}

    for entry in feed.get("entries", []):
        link = entry.get("link", "")
        if not link:
            continue

        title = entry.get("title", "")
        image_link = entry.get("image_link", "") or entry.get("image", {}).get("href", "")
        summary = entry.get("summary", "")

        # Extract category from tags, fallback to model name
        category = next((tag["term"] for tag in entry.get("tags", []) if "term" in tag), model.__tablename__)

        # Handle Phone-specific fields
        if model == Phone:
            dung_luong = entry.get("dung-luong", None)
            mau_sac = entry.get("mau-sac", None)
            _, fallback_dung_luong, fallback_mau_sac = extract_additional_info(summary)
            dung_luong = dung_luong or fallback_dung_luong
            mau_sac = mau_sac or fallback_mau_sac

            price_hn = entry.get("price-hn", "0 VND")
            price_dn = entry.get("price-dn", "0 VND")
            price = next((p for p in [price_hn, price_dn] if p != "0 VND"), None)
            if not price:
                price, _, _ = extract_additional_info(summary)
                if not price:
                    price = "0 VND"

            stock_hn = entry.get("stock-hn", "0")
            stock_dn = entry.get("stock-dn", "0")

            device = db.query(Phone).filter_by(link=link).first()
            if device:
                # Update existing entry
                device.title = title
                device.image_link = image_link
                device.price = price
                device.category = category
                device.price_hn = price_hn
                device.price_dn = price_dn
                device.stock_hn = stock_hn
                device.stock_dn = stock_dn
                device.dung_luong = dung_luong
                device.mau_sac = mau_sac
            else:
                # Insert new entry
                device = Phone(
                    link=link,
                    title=title,
                    image_link=image_link,
                    price=price,
                    category=category,
                    price_hn=price_hn,
                    price_dn=price_dn,
                    stock_hn=stock_hn,
                    stock_dn=stock_dn,
                    dung_luong=dung_luong,
                    mau_sac=mau_sac
                )
                db.add(device)

        # Handle TabletDevice and Accessory
        else:
            price = entry.get("price", None)
            if price is None or price == "":
                price, _, _ = extract_additional_info(summary)
            if not price:
                price = "0 VND"

            stock = entry.get("stock", "0")

            device = db.query(model).filter_by(link=link).first()
            if device:
                # Update existing entry
                device.title = title
                device.image_link = image_link
                device.price = price
                device.category = category
                device.stock = str(stock)
            else:
                # Insert new entry
                if model == TabletDevice:
                    device = TabletDevice(
                        link=link,
                        title=title,
                        image_link=image_link,
                        price=price,
                        category=category,
                        stock=str(stock)
                    )
                elif model == Accessory:
                    device = Accessory(
                        link=link,
                        title=title,
                        image_link=image_link,
                        price=price,
                        category=category,
                        stock=str(stock)
                    )
                db.add(device)

# 📌 CHẠY CHƯƠNG TRÌNH LIÊN TỤC
def main():
    # Tạo bảng nếu chưa có (with link as primary key)
    Base.metadata.create_all(bind=engine)

    while True:
        # Bước 1: Lưu RSS thành JSON
        rss_to_json()

        # Bước 2 & 3: Đọc JSON và đồng bộ CSDL
        db = SessionLocal()
        try:
            for url, model in rss_urls.items():
                filename = f"{url.split('/')[-1]}.json"
                if os.path.exists(filename):
                    sync_rss_feed(filename, model, db)
                else:
                    print(f"⚠️ File {filename} không tồn tại.")
            db.commit()
            print("✅ Dữ liệu đã được đồng bộ vào PostgreSQL!")
        except Exception as e:
            print(f"❌ Lỗi khi đồng bộ dữ liệu: {e}")
            db.rollback()
        finally:
            db.close()

        # Chờ 5 phút trước khi kiểm tra lại (tùy chỉnh thời gian)
        time.sleep(300)

if __name__ == "__main__":
    main()