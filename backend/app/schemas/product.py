from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    unit_price: float
    cost_price: Optional[float] = None
    gst_rate: float = 18.0
    image_url: Optional[str] = None
    warranty_months: int = 0
    minimum_stock: int = 10

class ProductCreate(ProductBase):
    store_id: int
    current_stock: int = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    gst_rate: Optional[float] = None
    image_url: Optional[str] = None
    warranty_months: Optional[int] = None
    minimum_stock: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    current_stock: int
    store_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class BatchBase(BaseModel):
    batch_id: str
    product_id: int
    quantity: int
    serial_numbers: Optional[str] = None
    manufacturing_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

class BatchCreate(BatchBase):
    pass

class BatchResponse(BatchBase):
    id: int
    remaining_quantity: int
    received_date: datetime
    
    class Config:
        from_attributes = True

