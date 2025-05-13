from database import SessionLocal
from models import Phone, TabletDevice, Accessory

def display_data():
    db = SessionLocal()
    try:
        # Truy vấn 10 dòng đầu từ bảng phones
        phones = db.query(Phone).limit(10).all()
        tablets = db.query(TabletDevice).limit(10).all()
        accessories = db.query(Accessory).limit(10).all()

        # Hiển thị dữ liệu từ bảng phones
        if phones:
            print("Dữ liệu trong bảng Phones (10 dòng đầu):")
            for phone in phones:
                print(f"ID: {phone.id}")
                print(f"Title: {phone.title}")
                print(f"Link: {phone.link}")
                print(f"Image Link: {phone.image_link}")
                print(f"Price: {phone.price}")
                print(f"Category: {phone.category}")
                print(f"Price HN: {phone.price_hn}")
                print(f"Price DN: {phone.price_dn}")
                print(f"Stock HN: {phone.stock_hn}")
                print(f"Stock DN: {phone.stock_dn}")
                print(f"Dung lượng: {phone.dung_luong}")
                print(f"Màu sắc: {phone.mau_sac}")
                print("-" * 50)

        # Hiển thị dữ liệu từ bảng tablet_device
        if tablets:
            print("Dữ liệu trong bảng TabletDevice (10 dòng đầu):")
            for tablet in tablets:
                print(f"ID: {tablet.id}")
                print(f"Title: {tablet.title}")
                print(f"Link: {tablet.link}")
                print(f"Image Link: {tablet.image_link}")
                print(f"Price: {tablet.price}")
                print(f"Category: {tablet.category}")
                print(f"Stock: {tablet.stock}")
                print("-" * 50)

        # Hiển thị dữ liệu từ bảng accessory
        if accessories:
            print("Dữ liệu trong bảng Accessory (10 dòng đầu):")
            for accessory in accessories:
                print(f"ID: {accessory.id}")
                print(f"Title: {accessory.title}")
                print(f"Link: {accessory.link}")
                print(f"Image Link: {accessory.image_link}")
                print(f"Price: {accessory.price}")
                print(f"Category: {accessory.category}")
                print(f"Stock: {accessory.stock}")
                print("-" * 50)

        if not phones and not tablets and not accessories:
            print("Không có dữ liệu trong các bảng.")
    finally:
        db.close()

if __name__ == "__main__":
    display_data()