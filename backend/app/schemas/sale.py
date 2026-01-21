from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.db.models import PaymentMode

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    serial_number: Optional[str] = None

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemResponse(SaleItemBase):
    id: int
    gst_rate: float
    gst_amount: float
    total_price: float
    warranty_expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    customer_id: Optional[int] = None
    payment_mode: PaymentMode
    discount: float = 0.0

class SaleCreate(SaleBase):
    store_id: int
    items: List[SaleItemCreate]

class SaleResponse(SaleBase):
    id: int
    invoice_number: str
    store_id: int
    subtotal: float
    gst_amount: float
    total_amount: float
    payment_status: str
    sale_date: datetime
    items: List[SaleItemResponse]
    
    class Config:
        from_attributes = True

class DailySalesStats(BaseModel):
    date: datetime
    total_sales: float
    total_transactions: int
    cash_sales: float
    card_sales: float
    upi_sales: float
    qr_code_sales: float

class MonthlySalesStats(BaseModel):
    month: str
    year: int
    total_sales: float
    total_transactions: int
    average_transaction_value: float

