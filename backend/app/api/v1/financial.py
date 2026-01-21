from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db import models
from app.schemas.financial import ExpenseCreate, ExpenseUpdate, ExpenseResponse, DailyClosingReport
from app.api.dependencies import get_current_user, get_store_manager_or_admin
import json
import os
import shutil
from pathlib import Path

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/vouchers")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/expenses", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_expense = models.Expense(
        **expense.model_dump(),
        created_by=current_user.id
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="expense",
        entity_id=db_expense.id,
        details=json.dumps({
            "category": db_expense.category,
            "amount": db_expense.amount,
            "description": db_expense.description
        })
    )
    db.add(audit_log)
    db.commit()
    
    return db_expense

@router.post("/expenses/upload-voucher")
async def upload_voucher(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    """Upload expense voucher/bill (PDF or Image)"""
    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/jpg", "image/png", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and image files are allowed"
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"voucher_{current_user.id}_{timestamp}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return relative path for database storage
        return {
            "success": True,
            "file_path": f"uploads/vouchers/{unique_filename}",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )

@router.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(
    skip: int = 0,
    limit: int = 100,
    store_id: int = None,
    category: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Expense)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Expense.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Expense.store_id == store_id)
    
    # Filter by category
    if category:
        query = query.filter(models.Expense.category == category)
    
    # Filter by date range
    if start_date:
        query = query.filter(models.Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(models.Expense.expense_date <= end_date)
    
    expenses = query.order_by(models.Expense.expense_date.desc()).offset(skip).limit(limit).all()
    return expenses

@router.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if expense.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return expense

@router.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if expense.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="update",
        entity_type="expense",
        entity_id=expense.id,
        details=json.dumps(update_data, default=str)
    )
    db.add(audit_log)
    db.commit()
    
    return expense

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if expense.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    db.delete(expense)
    db.commit()
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="delete",
        entity_type="expense",
        entity_id=expense_id,
        details=json.dumps({"category": expense.category, "amount": expense.amount})
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Expense deleted successfully"}

@router.get("/daily-closing", response_model=DailyClosingReport)
def get_daily_closing_report(
    date: datetime = None,
    store_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not date:
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    end_date = date + timedelta(days=1)
    
    # Get sales
    sales_query = db.query(models.Sale).filter(
        models.Sale.sale_date >= date,
        models.Sale.sale_date < end_date
    )
    
    # Get expenses
    expenses_query = db.query(models.Expense).filter(
        models.Expense.expense_date >= date,
        models.Expense.expense_date < end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        sales_query = sales_query.filter(models.Sale.store_id == current_user.store_id)
        expenses_query = expenses_query.filter(models.Expense.store_id == current_user.store_id)
    elif store_id:
        sales_query = sales_query.filter(models.Sale.store_id == store_id)
        expenses_query = expenses_query.filter(models.Expense.store_id == store_id)
    
    sales = sales_query.all()
    expenses = expenses_query.all()
    
    total_sales = sum(sale.total_amount for sale in sales)
    cash_collected = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.CASH)
    card_collected = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.CARD)
    upi_collected = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.UPI)
    qr_code_collected = sum(sale.total_amount for sale in sales if sale.payment_mode == models.PaymentMode.QR_CODE)
    
    total_expenses = sum(expense.amount for expense in expenses)
    cash_expenses = sum(expense.amount for expense in expenses if expense.payment_mode == models.PaymentMode.CASH)
    
    net_cash_in_hand = cash_collected - cash_expenses
    
    return {
        "date": date,
        "total_sales": total_sales,
        "cash_collected": cash_collected,
        "card_collected": card_collected,
        "upi_collected": upi_collected,
        "qr_code_collected": qr_code_collected,
        "total_expenses": total_expenses,
        "net_cash_in_hand": net_cash_in_hand,
        "total_transactions": len(sales)
    }

@router.get("/dashboard/stats")
def get_financial_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get today's data
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_today = today + timedelta(days=1)
    
    # Get this month's data
    start_month = datetime(today.year, today.month, 1)
    if today.month == 12:
        end_month = datetime(today.year + 1, 1, 1)
    else:
        end_month = datetime(today.year, today.month + 1, 1)
    
    sales_query = db.query(models.Sale).options(
        joinedload(models.Sale.sale_items).joinedload(models.SaleItem.product)
    )
    expenses_query = db.query(models.Expense)
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        sales_query = sales_query.filter(models.Sale.store_id == current_user.store_id)
        expenses_query = expenses_query.filter(models.Expense.store_id == current_user.store_id)
    
    # Today's stats
    today_sales = sales_query.filter(
        models.Sale.sale_date >= today,
        models.Sale.sale_date < end_today
    ).all()
    
    today_expenses = expenses_query.filter(
        models.Expense.expense_date >= today,
        models.Expense.expense_date < end_today
    ).all()
    
    # Monthly stats
    month_sales = sales_query.filter(
        models.Sale.sale_date >= start_month,
        models.Sale.sale_date < end_month
    ).all()
    
    month_expenses = expenses_query.filter(
        models.Expense.expense_date >= start_month,
        models.Expense.expense_date < end_month
    ).all()
    
    # Calculate totals with safe handling of None values
    today_revenue = sum(float(sale.total_amount or 0) for sale in today_sales)
    today_expenses_total = sum(float(expense.amount or 0) for expense in today_expenses)
    month_revenue = sum(float(sale.total_amount or 0) for sale in month_sales)
    month_expenses_total = sum(float(expense.amount or 0) for expense in month_expenses)
    
    # Calculate Cost of Goods Sold (COGS) for proper profit calculation
    # Profit = Revenue - COGS - Expenses
    # COGS is calculated from sale items using product cost_price
    today_cogs = 0
    for sale in today_sales:
        for item in sale.sale_items:
            if item.product and item.product.cost_price:
                today_cogs += float(item.product.cost_price) * float(item.quantity)
    
    month_cogs = 0
    for sale in month_sales:
        for item in sale.sale_items:
            if item.product and item.product.cost_price:
                month_cogs += float(item.product.cost_price) * float(item.quantity)
    
    # Gross Profit = Revenue - COGS
    # Net Profit = Gross Profit - Expenses
    today_gross_profit = today_revenue - today_cogs
    today_net_profit = today_gross_profit - today_expenses_total
    
    month_gross_profit = month_revenue - month_cogs
    month_net_profit = month_gross_profit - month_expenses_total
    
    return {
        "today_revenue": round(today_revenue, 2),
        "today_expenses": round(today_expenses_total, 2),
        "today_profit": round(today_net_profit, 2),
        "month_revenue": round(month_revenue, 2),
        "month_expenses": round(month_expenses_total, 2),
        "month_profit": round(month_net_profit, 2)
    }

