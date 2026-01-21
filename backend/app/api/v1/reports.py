from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, case, distinct
from datetime import datetime, timedelta
from typing import Optional, List
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
import io
import pandas as pd
from pydantic import BaseModel

router = APIRouter()

# ============ SCHEMAS ============

class DateRangeFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# ============ A. SALES REPORTS ============

@router.get("/sales/daily-summary")
def get_daily_sales_summary(
    date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Daily Sales Summary Report with comparisons"""
    if not date:
        date = datetime.now()
    
    # Set date range for today
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Yesterday
    yesterday = date - timedelta(days=1)
    start_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Same day last week
    last_week = date - timedelta(days=7)
    start_last_week = last_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_last_week = last_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # Query for today
    query = db.query(models.Sale).filter(models.Sale.sale_date >= start_of_day, models.Sale.sale_date <= end_of_day)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    today_sales = query.all()
    
    # Calculate today's metrics
    total_sales_today = sum(sale.total_amount for sale in today_sales)
    num_bills_today = len(today_sales)
    avg_bill_value_today = total_sales_today / num_bills_today if num_bills_today > 0 else 0
    
    # Payment mode breakdown
    payment_breakdown = {}
    for sale in today_sales:
        mode = sale.payment_mode.value
        payment_breakdown[mode] = payment_breakdown.get(mode, 0) + sale.total_amount
    
    # Yesterday comparison
    query_yesterday = db.query(models.Sale).filter(
        models.Sale.sale_date >= start_yesterday,
        models.Sale.sale_date <= end_yesterday
    )
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query_yesterday = query_yesterday.filter(models.Sale.store_id == current_user.store_id)
    
    yesterday_sales = query_yesterday.all()
    total_sales_yesterday = sum(sale.total_amount for sale in yesterday_sales)
    
    # Last week same day comparison
    query_last_week = db.query(models.Sale).filter(
        models.Sale.sale_date >= start_last_week,
        models.Sale.sale_date <= end_last_week
    )
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query_last_week = query_last_week.filter(models.Sale.store_id == current_user.store_id)
    
    last_week_sales = query_last_week.all()
    total_sales_last_week = sum(sale.total_amount for sale in last_week_sales)
    
    # Calculate percentage changes
    vs_yesterday = ((total_sales_today - total_sales_yesterday) / total_sales_yesterday * 100) if total_sales_yesterday > 0 else 0
    vs_last_week = ((total_sales_today - total_sales_last_week) / total_sales_last_week * 100) if total_sales_last_week > 0 else 0
    
    return {
        "date": date.strftime("%Y-%m-%d"),
        "total_sales": round(total_sales_today, 2),
        "num_bills": num_bills_today,
        "average_bill_value": round(avg_bill_value_today, 2),
        "payment_breakdown": {k: round(v, 2) for k, v in payment_breakdown.items()},
        "comparisons": {
            "vs_yesterday": {
                "amount": round(total_sales_yesterday, 2),
                "change_percentage": round(vs_yesterday, 2)
            },
            "vs_last_week_same_day": {
                "amount": round(total_sales_last_week, 2),
                "change_percentage": round(vs_last_week, 2)
            }
        }
    }

@router.get("/sales/product-wise")
def get_product_wise_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Product-wise Sales Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query sale items
    query = db.query(
        models.Product.name,
        models.Product.sku,
        func.sum(models.SaleItem.quantity).label('quantity_sold'),
        func.sum(models.SaleItem.total_price).label('sales_value'),
        func.sum(models.Sale.discount * models.SaleItem.total_price / models.Sale.total_amount).label('discount_given'),
        func.sum(models.SaleItem.total_price - (models.Product.cost_price * models.SaleItem.quantity)).label('margin_earned')
    ).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    results = query.group_by(models.Product.id, models.Product.name, models.Product.sku).all()
    
    products = []
    for row in results:
        products.append({
            "product_name": row.name,
            "sku": row.sku,
            "quantity_sold": int(row.quantity_sold or 0),
            "sales_value": round(float(row.sales_value or 0), 2),
            "discount_given": round(float(row.discount_given or 0), 2),
            "margin_earned": round(float(row.margin_earned or 0), 2)
        })
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "products": products
    }

@router.get("/sales/category-wise")
def get_category_wise_sales(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Category-wise Sales Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query by category
    query = db.query(
        models.Product.category,
        func.sum(models.SaleItem.total_price).label('revenue'),
        func.sum(models.SaleItem.total_price - (models.Product.cost_price * models.SaleItem.quantity)).label('profit')
    ).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    results = query.group_by(models.Product.category).all()
    
    # Calculate total for percentages
    total_revenue = sum(float(row.revenue or 0) for row in results)
    total_profit = sum(float(row.profit or 0) for row in results)
    
    categories = []
    for row in results:
        revenue = float(row.revenue or 0)
        profit = float(row.profit or 0)
        categories.append({
            "category": row.category or "Uncategorized",
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
            "revenue_contribution_percent": round((revenue / total_revenue * 100) if total_revenue > 0 else 0, 2),
            "profit_contribution_percent": round((profit / total_profit * 100) if total_profit > 0 else 0, 2)
        })
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "categories": categories,
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2)
    }

# ============ B. STAFF REPORTS ============

@router.get("/staff/sales-report")
def get_staff_sales_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Staff-wise Sales Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query sales by staff
    query = db.query(
        models.User.id,
        models.User.full_name,
        func.count(models.Sale.id).label('bills_generated'),
        func.sum(models.Sale.total_amount).label('sales_value'),
        func.sum(
            func.coalesce(
                db.query(func.sum(models.SaleItem.quantity))
                .filter(models.SaleItem.sale_id == models.Sale.id)
                .correlate(models.Sale)
                .scalar_subquery(),
                0
            )
        ).label('units_sold')
    ).join(
        models.Sale, models.User.id == models.Sale.created_by
    ).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.User.store_id == current_user.store_id)
    
    results = query.group_by(models.User.id, models.User.full_name).all()
    
    staff_report = []
    for row in results:
        staff_report.append({
            "staff_id": row.id,
            "staff_name": row.full_name,
            "bills_generated": int(row.bills_generated or 0),
            "sales_value": round(float(row.sales_value or 0), 2),
            "units_sold": int(row.units_sold or 0),
            "conversion_rate": 0  # TODO: Implement walk-in tracking
        })
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "staff": staff_report
    }

@router.get("/staff/incentive-report")
def get_staff_incentive_report(
    month: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Staff Incentive Report"""
    if not month:
        month = datetime.now().strftime("%Y-%m")
    
    # Query staff targets
    query = db.query(
        models.StaffTarget,
        models.User.full_name
    ).join(
        models.User, models.StaffTarget.user_id == models.User.id
    ).filter(
        models.StaffTarget.month == month
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.StaffTarget.store_id == current_user.store_id)
    
    results = query.all()
    
    staff_incentives = []
    for target, staff_name in results:
        achievement_percent = (target.achieved_amount / target.target_amount * 100) if target.target_amount > 0 else 0
        
        staff_incentives.append({
            "staff_name": staff_name,
            "target_amount": round(target.target_amount, 2),
            "achieved_amount": round(target.achieved_amount, 2),
            "achievement_percent": round(achievement_percent, 2),
            "incentive_earned": round(target.incentive_earned, 2),
            "incentive_paid": round(target.incentive_paid, 2),
            "incentive_pending": round(target.incentive_pending, 2)
        })
    
    return {
        "month": month,
        "staff_incentives": staff_incentives
    }

@router.get("/staff/attendance-sales-correlation")
def get_staff_attendance_sales_correlation(
    month: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Staff Attendance + Sales Correlation Report"""
    if not month:
        month = datetime.now().strftime("%Y-%m")
    
    # Parse month
    year, month_num = map(int, month.split("-"))
    start_date = datetime(year, month_num, 1)
    if month_num == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(year, month_num + 1, 1) - timedelta(seconds=1)
    
    # Get all staff
    query = db.query(models.User).filter(
        models.User.role.in_([models.UserRole.SALES_STAFF, models.UserRole.STORE_MANAGER])
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.User.store_id == current_user.store_id)
    
    staff_members = query.all()
    
    staff_report = []
    for staff in staff_members:
        # Get attendance
        attendance = db.query(models.StaffAttendance).filter(
            models.StaffAttendance.user_id == staff.id,
            models.StaffAttendance.date >= start_date,
            models.StaffAttendance.date <= end_date,
            models.StaffAttendance.status == "present"
        ).count()
        
        # Get sales
        sales = db.query(models.Sale).filter(
            models.Sale.created_by == staff.id,
            models.Sale.sale_date >= start_date,
            models.Sale.sale_date <= end_date
        ).all()
        
        total_sales = sum(sale.total_amount for sale in sales)
        
        # Get total hours worked
        hours_query = db.query(func.sum(models.StaffAttendance.hours_worked)).filter(
            models.StaffAttendance.user_id == staff.id,
            models.StaffAttendance.date >= start_date,
            models.StaffAttendance.date <= end_date
        ).scalar()
        
        total_hours = float(hours_query or 0)
        
        staff_report.append({
            "staff_name": staff.full_name,
            "present_days": attendance,
            "total_hours_worked": round(total_hours, 2),
            "total_sales": round(total_sales, 2),
            "sales_per_day": round(total_sales / attendance if attendance > 0 else 0, 2),
            "sales_per_hour": round(total_sales / total_hours if total_hours > 0 else 0, 2)
        })
    
    return {
        "month": month,
        "staff_report": staff_report
    }

# ============ C. INVENTORY & STOCK ANALYTICS ============

@router.get("/inventory/live-stock")
def get_live_stock_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Live Stock Report"""
    query = db.query(models.Product)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    products = query.filter(models.Product.is_active == True).all()
    
    stock_report = []
    for product in products:
        # Get last sold date
        last_sale = db.query(models.Sale.sale_date).join(
            models.SaleItem, models.Sale.id == models.SaleItem.sale_id
        ).filter(
            models.SaleItem.product_id == product.id
        ).order_by(models.Sale.sale_date.desc()).first()
        
        # Get store name
        store = db.query(models.Store).filter(models.Store.id == product.store_id).first()
        
        stock_report.append({
            "item_name": product.name,
            "sku": product.sku,
            "available_quantity": product.current_stock,
            "store_location": store.name if store else "Unknown",
            "last_sold_date": last_sale[0].strftime("%Y-%m-%d") if last_sale else "Never"
        })
    
    return {"stock_report": stock_report}

@router.get("/inventory/movement-analysis")
def get_stock_movement_analysis(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Fast Moving vs Slow Moving Items"""
    query = db.query(models.Product)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    products = query.filter(models.Product.is_active == True).all()
    
    stock_analysis = []
    for product in products:
        # Get last sold date
        last_sale = db.query(models.Sale.sale_date).join(
            models.SaleItem, models.Sale.id == models.SaleItem.sale_id
        ).filter(
            models.SaleItem.product_id == product.id
        ).order_by(models.Sale.sale_date.desc()).first()
        
        if last_sale:
            days_since_last_sale = (datetime.now() - last_sale[0]).days
        else:
            days_since_last_sale = 999
        
        # Determine ageing category
        if days_since_last_sale <= 30:
            ageing = "0-30 days"
        elif days_since_last_sale <= 60:
            ageing = "31-60 days"
        else:
            ageing = "60+ days"
        
        stock_analysis.append({
            "item_name": product.name,
            "sku": product.sku,
            "current_stock": product.current_stock,
            "days_since_last_sale": days_since_last_sale if days_since_last_sale < 999 else "Never",
            "stock_ageing": ageing,
            "movement_status": "Fast Moving" if days_since_last_sale <= 30 else "Slow Moving"
        })
    
    return {"stock_analysis": stock_analysis}

@router.get("/inventory/reorder-level")
def get_reorder_level_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Reorder Level Report"""
    query = db.query(models.Product)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    products = query.filter(
        models.Product.is_active == True,
        models.Product.current_stock <= models.Product.minimum_stock
    ).all()
    
    reorder_report = []
    for product in products:
        suggested_quantity = max(product.minimum_stock * 2 - product.current_stock, 0)
        
        reorder_report.append({
            "item_name": product.name,
            "sku": product.sku,
            "current_stock": product.current_stock,
            "minimum_stock": product.minimum_stock,
            "suggested_reorder_quantity": suggested_quantity,
            "estimated_cost": round(suggested_quantity * (product.cost_price or 0), 2)
        })
    
    return {"reorder_report": reorder_report}

@router.get("/inventory/high-value-stock")
def get_high_value_stock_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """High-Value Stock Report - items with high stock value"""
    query = db.query(models.Product)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    products = query.filter(models.Product.is_active == True).all()
    
    high_value_report = []
    for product in products:
        stock_value = product.current_stock * (product.cost_price or 0)
        
        # Include items with stock value > 10000 (lowered from 50000)
        if stock_value < 10000:
            continue
        
        # Get sales in last 60 days
        sixty_days_ago = datetime.now() - timedelta(days=60)
        sales_count = db.query(func.sum(models.SaleItem.quantity)).join(
            models.Sale, models.SaleItem.sale_id == models.Sale.id
        ).filter(
            models.SaleItem.product_id == product.id,
            models.Sale.sale_date >= sixty_days_ago
        ).scalar() or 0
        
        # Determine movement status
        if sales_count < 5:
            movement_status = "Low Movement"
        elif sales_count < 20:
            movement_status = "Medium Movement"
        else:
            movement_status = "High Movement"
        
        high_value_report.append({
            "item_name": product.name,
            "sku": product.sku,
            "current_stock": product.current_stock,
            "cost_per_unit": round(product.cost_price or 0, 2),
            "stock_value": round(stock_value, 2),
            "sales_last_60_days": int(sales_count),
            "movement_status": movement_status,
            "capital_blocked": round(stock_value, 2)
        })
    
    # Sort by stock value descending
    high_value_report.sort(key=lambda x: x['stock_value'], reverse=True)
    
    return {"high_value_stock": high_value_report}

# ============ D. PROFITABILITY & FINANCE REPORTS ============

@router.get("/profitability/item-wise-margin")
def get_item_wise_margin_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Item-wise Margin Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query sales with margin calculation
    query = db.query(
        models.Product.name,
        models.Product.sku,
        models.Product.cost_price,
        func.avg(models.SaleItem.unit_price).label('avg_selling_price'),
        func.sum(models.SaleItem.quantity).label('quantity_sold'),
        func.sum(models.Sale.discount * models.SaleItem.total_price / func.nullif(models.Sale.total_amount, 0)).label('total_discount'),
        func.sum(models.SaleItem.total_price - (models.Product.cost_price * models.SaleItem.quantity)).label('total_margin')
    ).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    results = query.group_by(models.Product.id, models.Product.name, models.Product.sku, models.Product.cost_price).all()
    
    margin_report = []
    for row in results:
        cost_price = float(row.cost_price or 0)
        selling_price = float(row.avg_selling_price or 0)
        quantity_sold = int(row.quantity_sold or 0)
        total_discount = float(row.total_discount or 0)
        total_margin = float(row.total_margin or 0)
        
        # Calculate per-unit net margin (selling price - cost price)
        per_unit_margin = selling_price - cost_price
        
        # Calculate margin percent
        margin_percent = ((selling_price - cost_price) / selling_price * 100) if selling_price > 0 else 0
        
        margin_report.append({
            "item_name": row.name,
            "sku": row.sku,
            "purchase_price": round(cost_price, 2),
            "selling_price": round(selling_price, 2),
            "discount": round(total_discount, 2),
            "net_margin": round(per_unit_margin, 2),  # Per-unit margin
            "margin_percent": round(margin_percent, 2)
        })
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "margin_report": margin_report
    }

@router.get("/profitability/brand-wise")
def get_brand_wise_profitability(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Brand-wise Profitability Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query by brand
    query = db.query(
        models.Product.brand,
        func.sum(models.SaleItem.total_price).label('revenue'),
        func.sum(models.SaleItem.total_price - (models.Product.cost_price * models.SaleItem.quantity)).label('gross_profit')
    ).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    results = query.group_by(models.Product.brand).all()
    
    brand_report = []
    for row in results:
        revenue = float(row.revenue or 0)
        gross_profit = float(row.gross_profit or 0)
        margin_percent = (gross_profit / revenue * 100) if revenue > 0 else 0
        
        brand_report.append({
            "brand": row.brand or "Unknown",
            "revenue": round(revenue, 2),
            "gross_profit": round(gross_profit, 2),
            "margin_percent": round(margin_percent, 2)
        })
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "brand_report": brand_report
    }

@router.get("/profitability/discount-impact")
def get_discount_impact_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Invoice Discount Impact Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query sales with discount
    query = db.query(models.Sale).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    sales = query.all()
    
    total_discount = sum(sale.discount for sale in sales)
    total_sales_value = sum(sale.total_amount + sale.discount for sale in sales)
    total_actual_sales = sum(sale.total_amount for sale in sales)
    
    # Calculate profit erosion (simplified)
    profit_erosion = total_discount * 0.7  # Assuming 70% of discount eats into profit
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_sales_before_discount": round(total_sales_value, 2),
        "total_discount_given": round(total_discount, 2),
        "total_sales_after_discount": round(total_actual_sales, 2),
        "discount_percentage": round((total_discount / total_sales_value * 100) if total_sales_value > 0 else 0, 2),
        "estimated_profit_erosion": round(profit_erosion, 2)
    }

@router.get("/finance/payment-mode-report")
def get_payment_mode_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Payment Mode Report"""
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    # Query sales by payment mode
    query = db.query(
        models.Sale.payment_mode,
        func.count(models.Sale.id).label('transaction_count'),
        func.sum(models.Sale.total_amount).label('total_amount')
    ).filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    results = query.group_by(models.Sale.payment_mode).all()
    
    payment_report = []
    for row in results:
        payment_report.append({
            "payment_mode": row.payment_mode.value,
            "transaction_count": int(row.transaction_count or 0),
            "total_amount": round(float(row.total_amount or 0), 2)
        })
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "payment_breakdown": payment_report
    }

@router.get("/finance/outstanding-receivables")
def get_outstanding_receivables(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Outstanding Receivables Report"""
    # Query pending finance sales
    query = db.query(models.Sale).filter(
        models.Sale.payment_status != "completed"
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    pending_sales = query.all()
    
    receivables = []
    total_pending = 0
    
    for sale in pending_sales:
        days_pending = (datetime.now() - sale.sale_date).days
        
        receivables.append({
            "invoice_number": sale.invoice_number,
            "customer_name": sale.customer.name if sale.customer else "Walk-in",
            "amount": round(sale.total_amount, 2),
            "sale_date": sale.sale_date.strftime("%Y-%m-%d"),
            "days_pending": days_pending,
            "payment_mode": sale.payment_mode.value
        })
        
        total_pending += sale.total_amount
    
    return {
        "total_outstanding": round(total_pending, 2),
        "receivables": receivables
    }

# ============ E. CUSTOMER ANALYTICS ============

@router.get("/customers/repeat-customers")
def get_repeat_customer_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Repeat Customer Report"""
    # Query customers with multiple purchases
    query = db.query(
        models.Customer,
        func.count(models.Sale.id).label('visit_count'),
        func.sum(models.Sale.total_amount).label('lifetime_value')
    ).join(
        models.Sale, models.Customer.id == models.Sale.customer_id
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Customer.store_id == current_user.store_id)
    
    results = query.group_by(models.Customer.id).having(func.count(models.Sale.id) > 1).all()
    
    repeat_customers = []
    for customer, visit_count, lifetime_value in results:
        # Get preferred products (most purchased category)
        preferred = db.query(models.Product.category).join(
            models.SaleItem, models.Product.id == models.SaleItem.product_id
        ).join(
            models.Sale, models.SaleItem.sale_id == models.Sale.id
        ).filter(
            models.Sale.customer_id == customer.id
        ).group_by(models.Product.category).order_by(func.count(models.Product.id).desc()).first()
        
        repeat_customers.append({
            "customer_name": customer.name,
            "phone": customer.phone,
            "email": customer.email or "",
            "repeat_visits": int(visit_count),
            "lifetime_value": round(float(lifetime_value or 0), 2),
            "preferred_products": preferred[0] if preferred else "N/A"
        })
    
    return {"repeat_customers": repeat_customers}

@router.get("/customers/warranty-due")
def get_warranty_due_report(
    days_ahead: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Warranty / AMC Due Report"""
    # Calculate date range
    today = datetime.now()
    future_date = today + timedelta(days=days_ahead)
    
    # Query sale items with warranty expiring soon
    query = db.query(
        models.SaleItem,
        models.Sale,
        models.Customer,
        models.Product
    ).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).join(
        models.Customer, models.Sale.customer_id == models.Customer.id
    ).join(
        models.Product, models.SaleItem.product_id == models.Product.id
    ).filter(
        models.SaleItem.warranty_expires_at.isnot(None),
        models.SaleItem.warranty_expires_at >= today,
        models.SaleItem.warranty_expires_at <= future_date
    )
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    results = query.all()
    
    warranty_due = []
    for sale_item, sale, customer, product in results:
        days_remaining = (sale_item.warranty_expires_at - today).days
        
        warranty_due.append({
            "customer_name": customer.name,
            "phone": customer.phone,
            "product_name": product.name,
            "serial_number": sale_item.serial_number or "N/A",
            "purchase_date": sale.sale_date.strftime("%Y-%m-%d"),
            "warranty_expiry": sale_item.warranty_expires_at.strftime("%Y-%m-%d"),
            "days_remaining": days_remaining
        })
    
    return {"warranty_due_list": warranty_due}

@router.get("/customers/{customer_id}/purchase-history")
def get_customer_purchase_history(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Customer Purchase History"""
    # Get customer
    customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check store access
    if current_user.role != models.UserRole.SUPER_ADMIN and customer.store_id != current_user.store_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get all sales
    sales = db.query(models.Sale).filter(
        models.Sale.customer_id == customer_id
    ).order_by(models.Sale.sale_date.desc()).all()
    
    purchase_history = []
    for sale in sales:
        items = []
        for item in sale.sale_items:
            items.append({
                "product_name": item.product.name,
                "quantity": item.quantity,
                "price": round(item.total_price, 2)
            })
        
        purchase_history.append({
            "invoice_number": sale.invoice_number,
            "date": sale.sale_date.strftime("%Y-%m-%d"),
            "total_amount": round(sale.total_amount, 2),
            "items": items
        })
    
    # Get last purchase date
    last_purchase = sales[0].sale_date if sales else None
    
    # Suggest accessories based on past purchases
    categories_purchased = set()
    for sale in sales:
        for item in sale.sale_items:
            if item.product.category:
                categories_purchased.add(item.product.category)
    
    # Simple accessory suggestions
    accessory_suggestions = []
    if "Mobile" in categories_purchased or "Mobiles" in categories_purchased:
        accessory_suggestions.extend(["Mobile Cases", "Screen Protectors", "Power Banks"])
    if "TV" in categories_purchased:
        accessory_suggestions.extend(["HDMI Cables", "Wall Mounts", "Soundbars"])
    if "AC" in categories_purchased:
        accessory_suggestions.extend(["AC Covers", "Stabilizers"])
    
    return {
        "customer": {
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email or "",
            "total_purchases": round(customer.total_purchases, 2),
            "last_purchase": last_purchase.strftime("%Y-%m-%d") if last_purchase else "Never"
        },
        "purchase_history": purchase_history,
        "accessory_suggestions": list(set(accessory_suggestions))[:5]
    }

@router.get("/sales/excel")
def download_sales_report_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Sale)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Sale.store_id == store_id)
    
    # Filter by date range
    if not start_date:
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if not end_date:
        end_date = datetime.now()
    
    query = query.filter(
        models.Sale.sale_date >= start_date,
        models.Sale.sale_date <= end_date
    )
    
    sales = query.all()
    
    # Prepare data for Excel
    data = []
    for sale in sales:
        data.append({
            "Invoice Number": sale.invoice_number,
            "Date": sale.sale_date.strftime("%Y-%m-%d %H:%M:%S"),
            "Customer": sale.customer.name if sale.customer else "Walk-in",
            "Subtotal": sale.subtotal,
            "GST Amount": sale.gst_amount,
            "Discount": sale.discount,
            "Total Amount": sale.total_amount,
            "Payment Mode": sale.payment_mode.value
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales Report')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=sales_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"}
    )

@router.get("/inventory/excel")
def download_inventory_report_excel(
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Product)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Product.store_id == store_id)
    
    products = query.filter(models.Product.is_active == True).all()
    
    # Prepare data for Excel
    data = []
    for product in products:
        stock_value = (product.cost_price or 0) * product.current_stock
        data.append({
            "SKU": product.sku,
            "Name": product.name,
            "Category": product.category or "",
            "Brand": product.brand or "",
            "Unit Price": product.unit_price,
            "Cost Price": product.cost_price or 0,
            "Current Stock": product.current_stock,
            "Minimum Stock": product.minimum_stock,
            "Stock Value": stock_value,
            "GST Rate": product.gst_rate,
            "Warranty (Months)": product.warranty_months
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventory Report')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=inventory_report_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )

@router.get("/expenses/excel")
def download_expenses_report_excel(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Expense)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Expense.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Expense.store_id == store_id)
    
    # Filter by date range
    try:
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_dt = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_dt = datetime.now()
    except (ValueError, AttributeError):
        # If date parsing fails, use current month
        start_dt = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = datetime.now()
    
    query = query.filter(
        models.Expense.expense_date >= start_dt,
        models.Expense.expense_date <= end_dt
    )
    
    expenses = query.all()
    
    # Prepare data for Excel
    data = []
    for expense in expenses:
        data.append({
            "Date": expense.expense_date.strftime("%Y-%m-%d %H:%M:%S"),
            "Category": expense.category,
            "Description": expense.description,
            "Amount": expense.amount,
            "Payment Mode": expense.payment_mode.value,
            "Vendor": expense.vendor_name or "",
            "Receipt Number": expense.receipt_number or ""
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Expenses Report')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=expenses_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"}
    )

@router.get("/customers/excel")
def download_customers_report_excel(
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Customer)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Customer.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Customer.store_id == store_id)
    
    customers = query.all()
    
    # Prepare data for Excel
    data = []
    for customer in customers:
        # Get purchase count
        purchase_count = db.query(models.Sale).filter(
            models.Sale.customer_id == customer.id
        ).count()
        
        data.append({
            "Name": customer.name,
            "Phone": customer.phone,
            "Email": customer.email or "",
            "Address": customer.address or "",
            "GST Number": customer.gst_number or "",
            "Total Purchases": customer.total_purchases,
            "Purchase Count": purchase_count,
            "Joined Date": customer.created_at.strftime("%Y-%m-%d")
        })
    
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Customers Report')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=customers_report_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )

@router.get("/profit-loss/excel")
def download_profit_loss_report_excel(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Profit & Loss Statement Excel Report"""
    try:
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_dt = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_dt = datetime.now()
    except (ValueError, AttributeError):
        start_dt = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = datetime.now()
    
    # Get sales data
    sales_query = db.query(models.Sale).filter(
        models.Sale.sale_date >= start_dt,
        models.Sale.sale_date <= end_dt
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        sales_query = sales_query.filter(models.Sale.store_id == current_user.store_id)
    elif store_id:
        sales_query = sales_query.filter(models.Sale.store_id == store_id)
    
    sales = sales_query.all()
    
    # Calculate revenue
    total_revenue = sum(sale.total_amount for sale in sales)
    total_gst_collected = sum(sale.gst_amount for sale in sales)
    total_discounts = sum(sale.discount for sale in sales)
    
    # Calculate COGS (Cost of Goods Sold)
    cogs = 0
    for sale in sales:
        for item in sale.sale_items:
            cogs += (item.product.cost_price or 0) * item.quantity
    
    # Get expenses
    expenses_query = db.query(models.Expense).filter(
        models.Expense.expense_date >= start_dt,
        models.Expense.expense_date <= end_dt
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        expenses_query = expenses_query.filter(models.Expense.store_id == current_user.store_id)
    elif store_id:
        expenses_query = expenses_query.filter(models.Expense.store_id == store_id)
    
    expenses = expenses_query.all()
    
    # Group expenses by category
    expense_by_category = {}
    for expense in expenses:
        cat = expense.category
        expense_by_category[cat] = expense_by_category.get(cat, 0) + expense.amount
    
    total_expenses = sum(expense.amount for expense in expenses)
    
    # Calculate profitability
    gross_profit = total_revenue - cogs
    net_profit = gross_profit - total_expenses
    
    # Prepare Excel data
    data = []
    
    # Revenue Section
    data.append({"Item": "=== REVENUE ===", "Amount": ""})
    data.append({"Item": "Total Sales", "Amount": total_revenue})
    data.append({"Item": "GST Collected", "Amount": total_gst_collected})
    data.append({"Item": "Discounts Given", "Amount": -total_discounts})
    data.append({"Item": "", "Amount": ""})
    
    # COGS Section
    data.append({"Item": "=== COST OF GOODS SOLD ===", "Amount": ""})
    data.append({"Item": "Cost of Goods Sold (COGS)", "Amount": -cogs})
    data.append({"Item": "GROSS PROFIT", "Amount": gross_profit})
    data.append({"Item": "", "Amount": ""})
    
    # Operating Expenses
    data.append({"Item": "=== OPERATING EXPENSES ===", "Amount": ""})
    for category, amount in expense_by_category.items():
        data.append({"Item": f"{category.title()}", "Amount": -amount})
    data.append({"Item": "Total Operating Expenses", "Amount": -total_expenses})
    data.append({"Item": "", "Amount": ""})
    
    # Net Profit
    data.append({"Item": "=== NET PROFIT/LOSS ===", "Amount": ""})
    data.append({"Item": "NET PROFIT", "Amount": net_profit})
    data.append({"Item": "Profit Margin %", "Amount": f"{(net_profit / total_revenue * 100) if total_revenue > 0 else 0:.2f}%"})
    
    df = pd.DataFrame(data)
    
    # Create Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Profit & Loss')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=profit_loss_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )

@router.get("/tax/excel")
def download_tax_report_excel(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    store_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """GST/Tax Report Excel"""
    try:
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_dt = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_dt = datetime.now()
    except (ValueError, AttributeError):
        start_dt = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_dt = datetime.now()
    
    # Get sales with GST breakdown
    sales_query = db.query(models.Sale).filter(
        models.Sale.sale_date >= start_dt,
        models.Sale.sale_date <= end_dt
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        sales_query = sales_query.filter(models.Sale.store_id == current_user.store_id)
    elif store_id:
        sales_query = sales_query.filter(models.Sale.store_id == store_id)
    
    sales = sales_query.all()
    
    # Group by GST rate
    gst_breakdown = {}
    for sale in sales:
        for item in sale.sale_items:
            gst_rate = item.gst_rate
            if gst_rate not in gst_breakdown:
                gst_breakdown[gst_rate] = {
                    'taxable_value': 0,
                    'gst_amount': 0,
                    'total': 0
                }
            taxable = item.unit_price * item.quantity
            gst_breakdown[gst_rate]['taxable_value'] += taxable
            gst_breakdown[gst_rate]['gst_amount'] += item.gst_amount
            gst_breakdown[gst_rate]['total'] += item.total_price
    
    # Prepare Excel data
    data = []
    total_taxable = 0
    total_gst = 0
    
    for rate in sorted(gst_breakdown.keys()):
        values = gst_breakdown[rate]
        data.append({
            "GST Rate": f"{rate}%",
            "Taxable Value": round(values['taxable_value'], 2),
            "GST Amount": round(values['gst_amount'], 2),
            "Total Value": round(values['total'], 2)
        })
        total_taxable += values['taxable_value']
        total_gst += values['gst_amount']
    
    # Add totals
    data.append({
        "GST Rate": "TOTAL",
        "Taxable Value": round(total_taxable, 2),
        "GST Amount": round(total_gst, 2),
        "Total Value": round(total_taxable + total_gst, 2)
    })
    
    df = pd.DataFrame(data)
    
    # Create Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='GST Report')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=gst_tax_report_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


# ============ ADVANCED REPORTS EXCEL EXPORTS ============

@router.get("/sales/product-wise/excel")
def download_product_wise_sales_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Product-wise Sales Report - Excel Export"""
    # Get data from the main endpoint logic
    data_response = get_product_wise_sales(start_date, end_date, db, current_user)
    
    # Convert to DataFrame
    df = pd.DataFrame(data_response['products'])
    
    if len(df) > 0:
        df.columns = ['Product Name', 'SKU', 'Quantity Sold', 'Sales Value (₹)', 'Discount Given (₹)', 'Margin Earned (₹)']
    
    # Create Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Product-wise Sales')
        
        # Add summary
        summary_data = {
            'Metric': ['Total Products', 'Total Quantity Sold', 'Total Sales Value', 'Total Discount', 'Total Margin'],
            'Value': [
                len(df),
                df['Quantity Sold'].sum() if len(df) > 0 else 0,
                f"₹{df['Sales Value (₹)'].sum():.2f}" if len(df) > 0 else '₹0.00',
                f"₹{df['Discount Given (₹)'].sum():.2f}" if len(df) > 0 else '₹0.00',
                f"₹{df['Margin Earned (₹)'].sum():.2f}" if len(df) > 0 else '₹0.00'
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, index=False, sheet_name='Summary', startrow=0)
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=product_wise_sales_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/sales/category-wise/excel")
def download_category_wise_sales_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Category-wise Sales Report - Excel Export"""
    data_response = get_category_wise_sales(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response['categories'])
    if len(df) > 0:
        df.columns = ['Category', 'Revenue (₹)', 'Profit (₹)', 'Contribution %']
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Category-wise Sales')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=category_wise_sales_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/sales/daily-summary/excel")
def download_daily_summary_excel(
    date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Daily Sales Summary - Excel Export"""
    data_response = get_daily_sales_summary(date, db, current_user)
    
    # Create summary data
    summary_data = {
        'Metric': [
            'Date',
            'Total Sales',
            'Number of Bills',
            'Average Bill Value',
            'vs Yesterday',
            'vs Last Week'
        ],
        'Value': [
            data_response['date'],
            f"₹{data_response['total_sales']:.2f}",
            data_response['num_bills'],
            f"₹{data_response['average_bill_value']:.2f}",
            f"{data_response['comparisons']['vs_yesterday']['percentage']:.2f}%",
            f"{data_response['comparisons']['vs_last_week']['percentage']:.2f}%"
        ]
    }
    
    # Payment breakdown
    payment_data = []
    for mode, amount in data_response['payment_breakdown'].items():
        payment_data.append({'Payment Mode': mode, 'Amount (₹)': amount})
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(summary_data).to_excel(writer, index=False, sheet_name='Summary')
        pd.DataFrame(payment_data).to_excel(writer, index=False, sheet_name='Payment Breakdown')
    
    output.seek(0)
    dt = date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=daily_sales_summary_{dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/inventory/live-stock/excel")
def download_live_stock_excel(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Live Stock Report - Excel Export"""
    data_response = get_live_stock_report(db, current_user)
    
    df = pd.DataFrame(data_response['products'])
    if len(df) > 0:
        df.columns = ['SKU', 'Product Name', 'Category', 'Current Stock', 'Min Stock', 'Status', 'Value (₹)']
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Live Stock')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=live_stock_report_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )


# ============ REMAINING EXCEL EXPORTS FOR ALL 17 REPORTS ============

@router.get("/staff/sales-report/excel")
def download_staff_sales_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Staff Sales Performance - Excel Export"""
    data_response = get_staff_sales_report(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response['staff'])
    if len(df) > 0:
        df.columns = ['Staff Name', 'Email', 'Bills Generated', 'Total Sales (₹)', 'Units Sold', 'Avg Bill Value (₹)']
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Staff Sales')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=staff_sales_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/staff/incentive-report/excel")
def download_staff_incentive_excel(
    month: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Staff Incentive Report - Excel Export"""
    data_response = get_staff_incentive_report(month, db, current_user)
    
    # Create DataFrame
    staff_data = []
    for staff_member in data_response.get('staff', []):
        staff_data.append({
            'Staff Name': staff_member.get('staff_name', ''),
            'Month': data_response.get('month', ''),
            'Sales Target (₹)': staff_member.get('target', 0),
            'Sales Achieved (₹)': staff_member.get('achieved', 0),
            'Achievement %': staff_member.get('achievement_percentage', 0),
            'Incentive Earned (₹)': staff_member.get('incentive_earned', 0),
            'Status': staff_member.get('status', '')
        })
    
    df = pd.DataFrame(staff_data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Incentive Report')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=staff_incentive_{data_response.get('month', 'current')}.xlsx"}
    )


@router.get("/staff/attendance-sales-correlation/excel")
def download_attendance_correlation_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Attendance & Sales Correlation - Excel Export"""
    data_response = get_attendance_sales_correlation(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response.get('staff', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance-Sales')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=attendance_sales_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/inventory/movement-analysis/excel")
def download_movement_analysis_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Stock Movement Analysis - Excel Export"""
    data_response = get_stock_movement_analysis(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response.get('products', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Movement Analysis')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=movement_analysis_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/inventory/reorder-level/excel")
def download_reorder_level_excel(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Reorder Level Alert - Excel Export"""
    data_response = get_reorder_level_alert(db, current_user)
    
    df = pd.DataFrame(data_response.get('products', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Reorder Alert')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=reorder_level_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/inventory/high-value-stock/excel")
def download_high_value_stock_excel(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """High Value Stock Report - Excel Export"""
    data_response = get_high_value_stock_report(db, current_user)
    
    df = pd.DataFrame(data_response.get('products', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='High Value Stock')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=high_value_stock_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/profitability/item-wise-margin/excel")
def download_item_margin_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Item-wise Margin Report - Excel Export"""
    data_response = get_item_wise_margin_report(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response.get('products', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Item Margins')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=item_margin_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/profitability/brand-wise/excel")
def download_brand_profitability_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Brand-wise Profitability - Excel Export"""
    data_response = get_brand_wise_profitability(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response.get('brands', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Brand Profitability')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=brand_profitability_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/profitability/discount-impact/excel")
def download_discount_impact_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Discount Impact Analysis - Excel Export"""
    data_response = get_discount_impact_analysis(start_date, end_date, db, current_user)
    
    # Create DataFrame from the response
    discount_data = [{
        'Total Discount Given (₹)': data_response.get('total_discount', 0),
        'Total Sales (₹)': data_response.get('total_sales', 0),
        'Discount %': data_response.get('discount_percentage', 0),
        'Profit Impact (₹)': data_response.get('profit_impact', 0)
    }]
    
    df = pd.DataFrame(discount_data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Discount Impact')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=discount_impact_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/customers/repeat-customers/excel")
def download_repeat_customers_excel(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Repeat Customer Analysis - Excel Export"""
    data_response = get_repeat_customers(db, current_user)
    
    df = pd.DataFrame(data_response.get('customers', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Repeat Customers')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=repeat_customers_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/customers/warranty-due/excel")
def download_warranty_due_excel(
    days_ahead: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Warranty Expiry Alert - Excel Export"""
    data_response = get_warranty_due_products(days_ahead, db, current_user)
    
    df = pd.DataFrame(data_response.get('products', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Warranty Expiring')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=warranty_expiring_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/finance/payment-mode-report/excel")
def download_payment_mode_excel(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Payment Mode Breakdown - Excel Export"""
    data_response = get_payment_mode_report(start_date, end_date, db, current_user)
    
    df = pd.DataFrame(data_response.get('payment_modes', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Payment Modes')
    
    output.seek(0)
    start_dt = start_date or datetime.now().replace(day=1)
    end_dt = end_date or datetime.now()
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=payment_modes_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.xlsx"}
    )


@router.get("/finance/outstanding-receivables/excel")
def download_outstanding_receivables_excel(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Outstanding Receivables - Excel Export"""
    data_response = get_outstanding_receivables(db, current_user)
    
    df = pd.DataFrame(data_response.get('receivables', []))
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Outstanding')
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=outstanding_receivables_{datetime.now().strftime('%Y%m%d')}.xlsx"}
    )

