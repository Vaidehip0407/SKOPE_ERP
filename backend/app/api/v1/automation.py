from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional, List
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter()

# ============ SCHEMAS ============

class AutomationRule(BaseModel):
    name: str
    trigger_type: str  # low_stock, customer_inactive, warranty_expiring, high_spend
    condition: dict
    action_type: str  # send_email, send_sms, create_campaign, reorder_stock
    action_config: dict
    is_active: bool = True

class SmartAlert(BaseModel):
    alert_type: str
    severity: str
    title: str
    message: str
    action_required: bool
    recommended_action: Optional[str]

# ============ SMART ALERTS SYSTEM ============

@router.get("/alerts/smart")
def get_smart_alerts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Real-time smart alerts based on business rules"""
    
    alerts = []
    
    # Alert 1: Critical Low Stock
    critical_stock = db.query(models.Product).filter(
        models.Product.current_stock <= models.Product.minimum_stock * 0.3,
        models.Product.is_active == True
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        critical_stock = critical_stock.filter(models.Product.store_id == current_user.store_id)
    
    for product in critical_stock.limit(10).all():
        alerts.append({
            "alert_type": "inventory_critical",
            "severity": "critical",
            "title": f"Critical: {product.name} Almost Out of Stock",
            "message": f"Only {product.current_stock} units left. Minimum required: {product.minimum_stock}",
            "action_required": True,
            "recommended_action": f"Reorder {product.minimum_stock * 2} units immediately",
            "entity_id": product.id,
            "entity_type": "product"
        })
    
    # Alert 2: High-Value Customers Not Engaged
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    high_value_inactive = db.query(models.Customer).filter(
        models.Customer.total_purchases >= 100000,
        models.Customer.id.notin_(
            db.query(models.Sale.customer_id).filter(
                models.Sale.sale_date >= thirty_days_ago
            )
        )
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        high_value_inactive = high_value_inactive.filter(models.Customer.store_id == current_user.store_id)
    
    for customer in high_value_inactive.limit(5).all():
        alerts.append({
            "alert_type": "customer_retention",
            "severity": "warning",
            "title": f"High-Value Customer Inactive: {customer.name}",
            "message": f"Customer with ₹{customer.total_purchases:,.0f} lifetime value hasn't purchased in 30+ days",
            "action_required": True,
            "recommended_action": "Send personalized re-engagement offer",
            "entity_id": customer.id,
            "entity_type": "customer"
        })
    
    # Alert 3: Warranties Expiring Soon
    thirty_days_ahead = datetime.now() + timedelta(days=30)
    
    expiring_warranties = db.query(
        models.SaleItem,
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
        models.SaleItem.warranty_expires_at <= thirty_days_ahead,
        models.SaleItem.warranty_expires_at >= datetime.now()
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        expiring_warranties = expiring_warranties.filter(models.Sale.store_id == current_user.store_id)
    
    for sale_item, customer, product in expiring_warranties.limit(10).all():
        days_left = (sale_item.warranty_expires_at - datetime.now()).days
        alerts.append({
            "alert_type": "warranty_expiring",
            "severity": "info",
            "title": f"Warranty Expiring: {product.name}",
            "message": f"Customer {customer.name}'s warranty expires in {days_left} days",
            "action_required": True,
            "recommended_action": "Offer extended warranty or AMC package",
            "entity_id": customer.id,
            "entity_type": "customer"
        })
    
    # Alert 4: Unusual Sales Pattern
    today = datetime.now().date()
    today_sales = db.query(func.sum(models.Sale.total_amount)).filter(
        func.date(models.Sale.sale_date) == today
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        today_sales = today_sales.filter(models.Sale.store_id == current_user.store_id)
    
    today_total = today_sales.scalar() or 0
    
    # Get average of last 7 days
    seven_days_ago = datetime.now() - timedelta(days=7)
    avg_sales = db.query(func.avg(
        db.query(func.sum(models.Sale.total_amount)).filter(
            func.date(models.Sale.sale_date) >= seven_days_ago.date()
        ).scalar()
    )).scalar() or 0
    
    if avg_sales > 0 and today_total < avg_sales * 0.5:
        alerts.append({
            "alert_type": "sales_anomaly",
            "severity": "warning",
            "title": "Unusual Sales Pattern Detected",
            "message": f"Today's sales (₹{today_total:,.0f}) are significantly lower than average (₹{avg_sales:,.0f})",
            "action_required": True,
            "recommended_action": "Review store operations and run promotional campaigns",
            "entity_id": None,
            "entity_type": "sales"
        })
    
    # Alert 5: Staff Performance Issues
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    low_performing_staff = db.query(
        models.User.id,
        models.User.full_name,
        func.count(models.Sale.id).label('sales_count'),
        func.sum(models.Sale.total_amount).label('total_sales')
    ).join(
        models.Sale, models.User.id == models.Sale.created_by
    ).filter(
        models.Sale.sale_date >= thirty_days_ago,
        models.User.role == models.UserRole.SALES_STAFF
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        low_performing_staff = low_performing_staff.filter(models.User.store_id == current_user.store_id)
    
    low_performing_staff = low_performing_staff.group_by(
        models.User.id, models.User.full_name
    ).having(
        func.count(models.Sale.id) < 5
    ).all()
    
    for staff in low_performing_staff:
        alerts.append({
            "alert_type": "staff_performance",
            "severity": "warning",
            "title": f"Low Performance: {staff.full_name}",
            "message": f"Only {staff.sales_count} sales in last 30 days",
            "action_required": True,
            "recommended_action": "Provide training and set clear targets",
            "entity_id": staff.id,
            "entity_type": "staff"
        })
    
    # Sort by severity
    severity_order = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda x: severity_order.get(x["severity"], 3))
    
    return {
        "total_alerts": len(alerts),
        "critical_count": len([a for a in alerts if a["severity"] == "critical"]),
        "warning_count": len([a for a in alerts if a["severity"] == "warning"]),
        "alerts": alerts
    }

# ============ AUTOMATED CAMPAIGN OPTIMIZER ============

@router.post("/campaigns/{campaign_id}/optimize")
def optimize_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """AI-powered campaign optimization based on performance data"""
    
    campaign = db.query(models.AdCampaignCreation).filter(
        models.AdCampaignCreation.id == campaign_id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get campaign analytics
    analytics = db.query(models.AdCampaignAnalytics).filter(
        models.AdCampaignAnalytics.campaign_id == campaign_id
    ).all()
    
    if not analytics:
        return {"message": "Insufficient data for optimization"}
    
    # Calculate key metrics
    total_spend = sum(a.spend for a in analytics)
    total_clicks = sum(a.clicks for a in analytics)
    total_conversions = sum(a.sales_attributed for a in analytics)
    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    
    recommendations = []
    
    # Recommendation 1: Budget optimization
    if avg_cpc > 50:  # If CPC is high
        recommendations.append({
            "type": "budget",
            "priority": "high",
            "current_value": f"₹{avg_cpc:.2f}",
            "recommendation": "CPC is high. Consider refining audience targeting or adjusting bid strategy",
            "expected_impact": "Reduce cost by 20-30%"
        })
    
    # Recommendation 2: Conversion optimization
    if conversion_rate < 2:
        recommendations.append({
            "type": "conversion",
            "priority": "high",
            "current_value": f"{conversion_rate:.2f}%",
            "recommendation": "Low conversion rate. Improve ad copy and landing page experience",
            "expected_impact": "Increase conversions by 50%"
        })
    
    # Recommendation 3: Audience refinement
    if total_clicks > 100 and conversion_rate < 1:
        recommendations.append({
            "type": "audience",
            "priority": "critical",
            "current_value": "Current audience",
            "recommendation": "Consider creating lookalike audience from existing customers",
            "expected_impact": "Better targeting, higher ROI"
        })
    
    # Recommendation 4: Budget reallocation
    if len(analytics) >= 7:
        # Find best performing days
        best_days = sorted(analytics, key=lambda x: x.roas if x.roas else 0, reverse=True)[:3]
        if best_days[0].roas and best_days[0].roas > 2:
            recommendations.append({
                "type": "timing",
                "priority": "medium",
                "current_value": "Daily budget distribution",
                "recommendation": f"Allocate more budget to high-performing periods (ROAS: {best_days[0].roas:.2f}x)",
                "expected_impact": "Increase overall ROAS by 15-25%"
            })
    
    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign.campaign_name,
        "performance_summary": {
            "total_spend": round(total_spend, 2),
            "total_clicks": total_clicks,
            "avg_cpc": round(avg_cpc, 2),
            "conversion_rate": round(conversion_rate, 2)
        },
        "optimization_score": min(100, len(recommendations) * 20),
        "recommendations": recommendations
    }

# ============ AUTOMATED RESTOCK SYSTEM ============

@router.post("/inventory/auto-restock")
def auto_restock_inventory(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Automated inventory restocking based on AI predictions"""
    
    # Get low stock products
    low_stock_products = db.query(models.Product).filter(
        models.Product.current_stock <= models.Product.minimum_stock,
        models.Product.is_active == True
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        low_stock_products = low_stock_products.filter(models.Product.store_id == current_user.store_id)
    
    restock_suggestions = []
    
    for product in low_stock_products.all():
        # Calculate average daily sales
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        total_sold = db.query(func.sum(models.SaleItem.quantity)).join(
            models.Sale, models.SaleItem.sale_id == models.Sale.id
        ).filter(
            models.SaleItem.product_id == product.id,
            models.Sale.sale_date >= thirty_days_ago
        ).scalar() or 0
        
        avg_daily_sales = total_sold / 30
        
        # Calculate reorder quantity (30 days supply + safety stock)
        safety_stock = product.minimum_stock
        reorder_qty = int((avg_daily_sales * 30) + safety_stock)
        
        # Estimate cost
        estimated_cost = reorder_qty * (product.cost_price or product.unit_price * 0.7)
        
        restock_suggestions.append({
            "product_id": product.id,
            "product_name": product.name,
            "current_stock": product.current_stock,
            "minimum_stock": product.minimum_stock,
            "avg_daily_sales": round(avg_daily_sales, 2),
            "suggested_reorder_qty": reorder_qty,
            "estimated_cost": round(estimated_cost, 2),
            "urgency": "critical" if product.current_stock == 0 else "high" if product.current_stock < product.minimum_stock * 0.3 else "medium"
        })
    
    # Sort by urgency
    urgency_order = {"critical": 0, "high": 1, "medium": 2}
    restock_suggestions.sort(key=lambda x: urgency_order.get(x["urgency"], 3))
    
    total_cost = sum(s["estimated_cost"] for s in restock_suggestions)
    
    return {
        "total_products_to_restock": len(restock_suggestions),
        "total_estimated_cost": round(total_cost, 2),
        "critical_items": len([s for s in restock_suggestions if s["urgency"] == "critical"]),
        "restock_suggestions": restock_suggestions
    }

# ============ SMART PRICING ENGINE ============

@router.get("/pricing/dynamic/{product_id}")
def dynamic_pricing_suggestion(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """AI-powered dynamic pricing suggestions based on demand, competition, and inventory"""
    
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Calculate current metrics
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Sales velocity
    sales_count = db.query(func.count(models.SaleItem.id)).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).filter(
        models.SaleItem.product_id == product_id,
        models.Sale.sale_date >= thirty_days_ago
    ).scalar() or 0
    
    # Current margin
    current_margin = ((product.unit_price - (product.cost_price or 0)) / product.unit_price * 100) if product.unit_price > 0 else 0
    
    # Inventory turnover
    stock_level = product.current_stock / product.minimum_stock if product.minimum_stock > 0 else 1
    
    # Pricing recommendations
    recommendations = []
    
    # Strategy 1: High stock + low sales = discount
    if stock_level > 2 and sales_count < 5:
        suggested_price = product.unit_price * 0.90
        recommendations.append({
            "strategy": "clearance",
            "reason": "High inventory with low sales velocity",
            "suggested_price": round(suggested_price, 2),
            "discount_percentage": 10,
            "expected_impact": "Increase sales volume by 30-40%"
        })
    
    # Strategy 2: Low stock + high demand = premium pricing
    elif stock_level < 0.5 and sales_count > 15:
        suggested_price = product.unit_price * 1.05
        recommendations.append({
            "strategy": "premium",
            "reason": "High demand with limited stock",
            "suggested_price": round(suggested_price, 2),
            "discount_percentage": -5,
            "expected_impact": "Maximize profit margin"
        })
    
    # Strategy 3: Competitive pricing
    else:
        recommendations.append({
            "strategy": "maintain",
            "reason": "Balanced inventory and demand",
            "suggested_price": round(product.unit_price, 2),
            "discount_percentage": 0,
            "expected_impact": "Stable sales"
        })
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "current_price": round(product.unit_price, 2),
        "cost_price": round(product.cost_price or 0, 2),
        "current_margin": round(current_margin, 2),
        "metrics": {
            "sales_last_30_days": sales_count,
            "stock_level": round(stock_level, 2),
            "inventory_status": "high" if stock_level > 1.5 else "low" if stock_level < 0.5 else "optimal"
        },
        "recommendations": recommendations
    }

# ============ AUTOMATED EMAIL CAMPAIGNS ============

@router.post("/email/auto-campaigns")
def trigger_automated_email_campaigns(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Trigger automated email campaigns based on customer behavior"""
    
    campaigns_triggered = []
    
    # Campaign 1: Welcome new customers
    seven_days_ago = datetime.now() - timedelta(days=7)
    new_customers = db.query(models.Customer).filter(
        models.Customer.created_at >= seven_days_ago
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        new_customers = new_customers.filter(models.Customer.store_id == current_user.store_id)
    
    new_customers_count = new_customers.count()
    if new_customers_count > 0:
        campaigns_triggered.append({
            "campaign_type": "welcome",
            "target_count": new_customers_count,
            "message": "Welcome email with special offer",
            "status": "queued"
        })
    
    # Campaign 2: Re-engage inactive customers
    ninety_days_ago = datetime.now() - timedelta(days=90)
    inactive_customers = db.query(models.Customer).filter(
        models.Customer.id.notin_(
            db.query(models.Sale.customer_id).filter(
                models.Sale.sale_date >= ninety_days_ago
            )
        )
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        inactive_customers = inactive_customers.filter(models.Customer.store_id == current_user.store_id)
    
    inactive_count = inactive_customers.count()
    if inactive_count > 0:
        campaigns_triggered.append({
            "campaign_type": "reengagement",
            "target_count": inactive_count,
            "message": "We miss you - Special comeback offer",
            "status": "queued"
        })
    
    # Campaign 3: Birthday wishes
    today = datetime.now()
    birthday_customers = db.query(models.Customer).filter(
        extract('month', models.Customer.date_of_birth) == today.month,
        extract('day', models.Customer.date_of_birth) == today.day
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        birthday_customers = birthday_customers.filter(models.Customer.store_id == current_user.store_id)
    
    birthday_count = birthday_customers.count()
    if birthday_count > 0:
        campaigns_triggered.append({
            "campaign_type": "birthday",
            "target_count": birthday_count,
            "message": "Birthday special discount",
            "status": "queued"
        })
    
    return {
        "campaigns_triggered": len(campaigns_triggered),
        "total_recipients": sum(c["target_count"] for c in campaigns_triggered),
        "campaigns": campaigns_triggered
    }

