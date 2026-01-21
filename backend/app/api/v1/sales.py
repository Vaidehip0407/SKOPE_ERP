from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db import models
from app.schemas.sale import SaleCreate, SaleResponse, DailySalesStats, MonthlySalesStats
from app.api.dependencies import get_current_user
import json
import random

router = APIRouter()

def generate_invoice_number(db: Session, store_id: int) -> str:
    """Generate unique invoice number"""
    today = datetime.now()
    prefix = f"INV{store_id}{today.strftime('%Y%m%d')}"
    
    # Get count of invoices today
    count = db.query(models.Sale).filter(
        models.Sale.invoice_number.like(f"{prefix}%")
    ).count()
    
    return f"{prefix}{count + 1:04d}"

@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verify all products exist and have sufficient stock
    for item in sale.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )
        
        if product.current_stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
    
    # Calculate totals
    subtotal = 0
    gst_amount = 0
    
    for item in sale.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        item_total = item.unit_price * item.quantity
        item_gst = (item_total * product.gst_rate) / 100
        subtotal += item_total
        gst_amount += item_gst
    
    total_amount = subtotal + gst_amount - sale.discount
    
    # Create sale
    db_sale = models.Sale(
        invoice_number=generate_invoice_number(db, sale.store_id),
        customer_id=sale.customer_id,
        store_id=sale.store_id,
        subtotal=subtotal,
        gst_amount=gst_amount,
        discount=sale.discount,
        total_amount=total_amount,
        payment_mode=sale.payment_mode,
        created_by=current_user.id
    )
    
    db.add(db_sale)
    db.flush()
    
    # Create sale items and update stock
    for item in sale.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        
        item_total = item.unit_price * item.quantity
        item_gst = (item_total * product.gst_rate) / 100
        
        warranty_expires_at = None
        if product.warranty_months > 0:
            warranty_expires_at = datetime.now() + timedelta(days=product.warranty_months * 30)
        
        db_sale_item = models.SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            gst_rate=product.gst_rate,
            gst_amount=item_gst,
            total_price=item_total + item_gst,
            serial_number=item.serial_number,
            warranty_expires_at=warranty_expires_at
        )
        
        db.add(db_sale_item)
        
        # Update product stock
        product.current_stock -= item.quantity
    
    # Update customer total purchases
    if sale.customer_id:
        customer = db.query(models.Customer).filter(models.Customer.id == sale.customer_id).first()
        if customer:
            customer.total_purchases += total_amount
    
    db.commit()
    db.refresh(db_sale)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="sale",
        entity_id=db_sale.id,
        details=json.dumps({
            "invoice_number": db_sale.invoice_number,
            "total_amount": total_amount,
            "items_count": len(sale.items)
        })
    )
    db.add(audit_log)
    db.commit()
    
    return db_sale

@router.get("/", response_model=List[SaleResponse])
def get_sales(
    skip: int = 0,
    limit: int = 100,
    store_id: int = None,
    customer_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Eagerly load sale_items to avoid lazy loading issues
    query = db.query(models.Sale).options(joinedload(models.Sale.sale_items))
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Sale.store_id == store_id)
    
    # Filter by customer
    if customer_id:
        query = query.filter(models.Sale.customer_id == customer_id)
    
    # Filter by date range
    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    
    sales = query.order_by(models.Sale.sale_date.desc()).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Eagerly load sale_items
    sale = db.query(models.Sale).options(joinedload(models.Sale.sale_items)).filter(models.Sale.id == sale_id).first()
    
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if sale.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return sale

@router.get("/stats/daily", response_model=DailySalesStats)
def get_daily_sales_stats(
    date: datetime = None,
    store_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not date:
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    end_date = date + timedelta(days=1)
    
    query = db.query(models.Sale).filter(
        models.Sale.sale_date >= date,
        models.Sale.sale_date < end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Sale.store_id == store_id)
    
    sales = query.all()
    
    total_sales = sum(sale.total_amount for sale in sales)
    total_transactions = len(sales)
    cash_sales = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.CASH)
    card_sales = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.CARD)
    upi_sales = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.UPI)
    qr_code_sales = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.QR_CODE)
    
    return {
        "date": date,
        "total_sales": total_sales,
        "total_transactions": total_transactions,
        "cash_sales": cash_sales,
        "card_sales": card_sales,
        "upi_sales": upi_sales,
        "qr_code_sales": qr_code_sales
    }

@router.get("/stats/monthly", response_model=MonthlySalesStats)
def get_monthly_sales_stats(
    month: int = None,
    year: int = None,
    store_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not month:
        month = datetime.now().month
    if not year:
        year = datetime.now().year
    
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    query = db.query(models.Sale).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date < end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Sale.store_id == store_id)
    
    sales = query.all()
    
    total_sales = sum(sale.total_amount for sale in sales)
    total_transactions = len(sales)
    average_transaction_value = total_sales / total_transactions if total_transactions > 0 else 0
    
    return {
        "month": f"{year}-{month:02d}",
        "year": year,
        "total_sales": total_sales,
        "total_transactions": total_transactions,
        "average_transaction_value": average_transaction_value
    }

@router.get("/dashboard/stats")
def get_sales_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get today's stats
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_today = today + timedelta(days=1)
    
    query = db.query(models.Sale)
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    today_sales = query.filter(
        models.Sale.sale_date >= today,
        models.Sale.sale_date < end_today
    ).all()
    
    # Get this month's stats
    start_month = datetime(today.year, today.month, 1)
    if today.month == 12:
        end_month = datetime(today.year + 1, 1, 1)
    else:
        end_month = datetime(today.year, today.month + 1, 1)
    
    month_sales = query.filter(
        models.Sale.sale_date >= start_month,
        models.Sale.sale_date < end_month
    ).all()
    
    return {
        "today_sales": sum(sale.total_amount for sale in today_sales),
        "today_transactions": len(today_sales),
        "month_sales": sum(sale.total_amount for sale in month_sales),
        "month_transactions": len(month_sales),
        "average_transaction_value": sum(sale.total_amount for sale in month_sales) / len(month_sales) if month_sales else 0
    }

