import feedparser
import json
import os
import re
from database import SessionLocal, engine, Base
from models import Phone, TabletDevice, Accessory

# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

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

    price_match = re.search(r"(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2})?)\s*VND", description)
    if price_match:
        price = price_match.group(1).replace(".", "").replace(",", "") + " VND"

    dung_luong_match = re.search(r"(\d+(?:-\d+)?GB)", description)
    if dung_luong_match:
        dung_luong = dung_luong_match.group(1)

    mau_sac_match = re.search(r"(Xanh\s*(?:Dương|Lục Bảo|Hoàng Gia)|Đen|Trắng|Vàng|Xám|Đỏ)", description)
    if mau_sac_match:
        mau_sac = mau_sac_match.group(1)

    return price, dung_luong, mau_sac

# 📌 BƯỚC 3: Đọc file JSON và lưu vào DB
def process_rss_feed(json_filename, model, db):
    with open(json_filename, "r", encoding="utf-8") as f:
        feed = json.load(f)

    for entry in feed.get("entries", []):
        title = entry.get("title", "")
        link = entry.get("link", "")
        image_link = entry.get("image_link", "") or entry.get("image", {}).get("href", "")
        summary = entry.get("summary", "")

        price_hn = entry.get("price-hn", "0 VND")
        price_hcm = entry.get("price-hcm", "0 VND")
        price_dn = entry.get("price-dn", "0 VND")

        # Ưu tiên lấy giá theo thứ tự
        price = next((p for p in [price_hn, price_hcm, price_dn] if p != "0 VND"), None)

        # Trích xuất từ summary nếu chưa có
        fallback_price, fallback_dung_luong, fallback_mau_sac = extract_additional_info(summary)
        price = price or fallback_price

        stock_hn = entry.get("stock-hn", "0")
        stock_dn = entry.get("stock-dn", "0")

        category = next((tag["term"] for tag in entry.get("tags", []) if "term" in tag), model.__tablename__)

        # Xử lý Phone
        if model == Phone:
            dung_luong = entry.get("dung_luong") or fallback_dung_luong
            mau_sac = entry.get("mau_sac") or fallback_mau_sac

            device = Phone(
                title=title,
                link=link,
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

        # Xử lý TabletDevice
        elif model == TabletDevice:
            stock = entry.get("stock") or stock_hn or "0"
            device = TabletDevice(
                title=title,
                link=link,
                image_link=image_link,
                price=price,
                category=category,
                stock=str(stock)
            )

        # Xử lý Accessory
        elif model == Accessory:
            stock = entry.get("stock") or stock_hn or "0"
            device = Accessory(
                title=title,
                link=link,
                image_link=image_link,
                price=price,
                category=category,
                stock=str(stock)
            )

        db.add(device)

# 📌 CHẠY CHƯƠNG TRÌNH
def main():
    # Bước 1: Lưu RSS thành JSON
    rss_to_json()

    # Bước 2 & 3: Đọc JSON và lưu CSDL
    db = SessionLocal()
    try:
        for url, model in rss_urls.items():
            filename = f"{url.split('/')[-1]}.json"
            if os.path.exists(filename):
                process_rss_feed(filename, model, db)
            else:
                print(f"⚠️ File {filename} không tồn tại.")
        db.commit()
        print("✅ Dữ liệu đã được lưu vào PostgreSQL!")
    except Exception as e:
        print(f"❌ Lỗi khi lưu dữ liệu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
