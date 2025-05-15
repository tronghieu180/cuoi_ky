from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from app.database.database import Base

class Phone(Base):
    __tablename__ = "phones"

    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(String)
    category = Column(ARRAY(String))
    price_hn = Column(Integer)
    price_dn = Column(Integer)
    price_hcm = Column(Integer)
    dung_luong = Column(String)
    mau_sac = Column(String)

class TabletDevice(Base):
    __tablename__ = "tablet_devices"

    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(Integer)
    category = Column(ARRAY(String))

class Accessory(Base):
    __tablename__ = "accessories"
    
    link = Column(String, primary_key=True)
    title = Column(String)
    image_link = Column(String)
    price = Column(Integer)
    category = Column(ARRAY(String))