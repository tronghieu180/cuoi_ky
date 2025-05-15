from sqlalchemy import Column, String
from database import Base

class Phone(Base):
    __tablename__ = "phones"
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(String)
    price_hn = Column(String)
    price_hcm = Column(String)  # Đảm bảo có price_hcm
    price_dn = Column(String)   # Giữ price_dn
    dung_luong = Column(String)
    mau_sac = Column(String)

class TabletDevice(Base):
    __tablename__ = "tablet_devices"
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(String)

class Accessory(Base):
    __tablename__ = "accessories"
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(String)