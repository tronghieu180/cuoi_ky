from pydantic import BaseModel
from typing import Optional

# Schema cho bảng phones
class PhoneBase(BaseModel):
    title: Optional[str] = None
    link: str
    image_link: Optional[str] = None
    price: Optional[str] = None
    category: Optional[str] = None
    price_hn: Optional[str] = None
    price_hcm: Optional[str] = None  # Thêm price_hcm
    price_dn: Optional[str] = None   # Đảm bảo giữ price_dn
    dung_luong: Optional[str] = None
    mau_sac: Optional[str] = None

class PhoneSearch(PhoneBase):
    class Config:
        orm_mode = True

# Schema cho bảng tablet_device
class TabletDeviceBase(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    category: Optional[str] = None
    link: str  
    image_link: Optional[str] = None

class TabletDeviceSearch(TabletDeviceBase):
    class Config:
        orm_mode = True

# Schema cho bảng accessory
class AccessoryBase(BaseModel):
    title: Optional[str] = None
    price: Optional[str] = None
    category: Optional[str] = None
    link: str  
    image_link: Optional[str] = None

class AccessorySearch(AccessoryBase):
    class Config:
        orm_mode = True