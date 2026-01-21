from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.models import PaymentMode

class ExpenseBase(BaseModel):
    category: str
    description: str
    amount: float
    payment_mode: PaymentMode
    vendor_name: Optional[str] = None
    receipt_number: Optional[str] = None
    voucher_file: Optional[str] = None
    expense_date: Optional[datetime] = None

class ExpenseCreate(ExpenseBase):
    store_id: int

class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    payment_mode: Optional[PaymentMode] = None
    vendor_name: Optional[str] = None
    receipt_number: Optional[str] = None
    voucher_file: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    id: int
    store_id: int
    created_by: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class DailyClosingReport(BaseModel):
    date: datetime
    total_sales: float
    cash_collected: float
    card_collected: float
    upi_collected: float
    qr_code_collected: float
    total_expenses: float
    net_cash_in_hand: float
    total_transactions: int

