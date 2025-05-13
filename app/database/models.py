from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from database import Base
class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    image_link = Column(String, nullable=True)
    price = Column(String, nullable=True)
    category = Column(String, nullable=True)
    price_hn = Column(String, nullable=True)
    price_dn = Column(String, nullable=True)
    stock_hn = Column(String, nullable=True)
    stock_dn = Column(String, nullable=True)
    dung_luong = Column(String, nullable=True)
    mau_sac = Column(String, nullable=True)

class TabletDevice(Base):
    __tablename__ = "tablet_device"

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)
    title = Column(String, nullable=True, index=True)
    price = Column(String, nullable=True, index=True) 
    stock = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)
    link = Column(String, nullable=True)
    image_link = Column(String, nullable=True)

class Accessory(Base):
    __tablename__ = "accessory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True, index=True)
    price = Column(String, nullable=True, index=True) 
    stock = Column(String, nullable=True)
    category = Column(String, nullable=True, index=True)
    link = Column(String, nullable=True)
    image_link = Column(String, nullable=True)

