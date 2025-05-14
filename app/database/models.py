from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Phone(Base):
    __tablename__ = "phones"
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(String)
    price_hn = Column(String)
    price_dn = Column(String)
    stock_hn = Column(String)
    stock_dn = Column(String)
    dung_luong = Column(String)
    mau_sac = Column(String)

class TabletDevice(Base):
    __tablename__ = "tablet_devices"
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(String)
    stock = Column(String)

class Accessory(Base):
    __tablename__ = "accessories"
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(String)
    stock = Column(String)