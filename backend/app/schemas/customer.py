from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    address: Optional[str] = None
    gst_number: Optional[str] = None

class CustomerCreate(CustomerBase):
    store_id: int

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int
    store_id: int
    total_purchases: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class CustomerWithPurchaseHistory(CustomerResponse):
    purchase_count: int
    last_purchase_date: Optional[datetime] = None

