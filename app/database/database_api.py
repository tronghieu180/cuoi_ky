import json
from database import SessionLocal, engine, Base
from models import Phone, TabletDevice, Accessory
from sqlalchemy.orm import load_only
from typing import Dict, Any

Base.metadata.create_all(bind=engine)

def sync_to_database(data: Dict[str, list]):
    db = SessionLocal()
    try:
        for category, entries in data.items():
            print(f"Đồng bộ dữ liệu cho danh mục: {category}")  
            model = {
                "phones": Phone,
                "tablet_devices": TabletDevice,
                "accessories": Accessory
            }[category]

            existing_links = {item.link for item in db.query(model).options(load_only(model.link))}
            print(f"Số lượng link hiện có trong {category}: {len(existing_links)}")  

            for entry in entries:
                link = entry.get("link", "")
                if not link:
                    continue

                if category == "phones":
                    device = db.query(Phone).filter_by(link=link).first()
                    if device:
                        device.title = entry["title"]
                        device.image_link = entry["image_link"]
                        device.price = entry["price"]
                        device.category = entry["category"]
                        device.price_hn = entry["price_hn"]
                        device.price_hcm = entry["price_hcm"]
                        device.price_dn = entry["price_dn"]
                        device.dung_luong = entry["dung_luong"]
                        device.mau_sac = entry["mau_sac"]
                    else:
                        device = Phone(
                            link=link,
                            title=entry["title"],
                            image_link=entry["image_link"],
                            price=entry["price"],
                            category=entry["category"],
                            price_hn=entry["price_hn"],
                            price_hcm=entry["price_hcm"],
                            price_dn=entry["price_dn"],
                            dung_luong=entry["dung_luong"],
                            mau_sac=entry["mau_sac"]
                        )
                        db.add(device)

                else:
                    device = db.query(model).filter_by(link=link).first()
                    if device:
                        device.title = entry["title"]
                        device.image_link = entry["image_link"]
                        device.price = entry["price"]
                        device.category = entry["category"]
                    else:
                        device = model(
                            link=link,
                            title=entry["title"],
                            image_link=entry["image_link"],
                            price=entry["price"],
                            category=entry["category"]
                        )
                        db.add(device)

        db.commit()
        print("✅ Dữ liệu đã được đồng bộ vào cơ sở dữ liệu!")
    except Exception as e:
        print(f"❌ Lỗi khi đồng bộ dữ liệu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    from data_ingestion import ingest_data
    data = ingest_data()
    sync_to_database(data)