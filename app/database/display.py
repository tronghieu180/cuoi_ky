from database import SessionLocal
from models import Phone, TabletDevice, Accessory

def display_data():
    db = SessionLocal()
    try:
        print("Dữ liệu trong bảng Phones (10 dòng đầu):")
        phones = db.query(Phone).limit(10).all()
        for phone in phones:
            print(f"Link (ID): {phone.link}")
            print(f"Title: {phone.title}")
            print(f"Image Link: {phone.image_link}")
            print(f"Price: {phone.price}")
            print(f"Category: {phone.category}")
            print(f"Price HN: {phone.price_hn}")
            print(f"Price HCM: {phone.price_hcm}")
            print(f"Price DN: {phone.price_dn}")
            print(f"Dung lượng: {phone.dung_luong}")
            print(f"Màu sắc: {phone.mau_sac}")
            print("-" * 50)


        print("\nDữ liệu trong bảng Tablet Devices (10 dòng đầu):")
        tablets = db.query(TabletDevice).limit(10).all()
        for tablet in tablets:
            print(f"Link (ID): {tablet.link}")
            print(f"Title: {tablet.title}")
            print(f"Image Link: {tablet.image_link}")
            print(f"Price: {tablet.price}")
            print(f"Category: {tablet.category}")
            print("-" * 50)

        print("\nDữ liệu trong bảng Accessories (10 dòng đầu):")
        accessories = db.query(Accessory).limit(10).all()
        for accessory in accessories:
            print(f"Link (ID): {accessory.link}")
            print(f"Title: {accessory.title}")
            print(f"Image Link: {accessory.image_link}")
            print(f"Price: {accessory.price}")
            print(f"Category: {accessory.category}")
            print("-" * 50)

    finally:
        db.close()

if __name__ == "__main__":
    display_data()