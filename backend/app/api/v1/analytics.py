from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, timedelta
from typing import Optional, List
from app.db.database import get_db
from app.db import models
from app.api.dependencies import get_current_user
from pydantic import BaseModel
import numpy as np
from collections import defaultdict

router = APIRouter()

# ============ SCHEMAS ============

class SalesForecast(BaseModel):
    date: str
    predicted_sales: float
    confidence_interval_low: float
    confidence_interval_high: float

class CustomerSegment(BaseModel):
    segment: str
    customer_count: int
    avg_order_value: float
    total_revenue: float
    characteristics: dict

class ProductRecommendation(BaseModel):
    product_id: int
    product_name: str
    confidence_score: float
    reason: str

# ============ AI-POWERED SALES FORECASTING ============

@router.get("/forecast/sales")
def forecast_sales(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """AI-powered sales forecasting using time series analysis"""
    
    # Get historical sales data (last 90 days)
    ninety_days_ago = datetime.now() - timedelta(days=90)
    
    query = db.query(
        func.date(models.Sale.sale_date).label('date'),
        func.sum(models.Sale.total_amount).label('total_sales')
    ).filter(
        models.Sale.sale_date >= ninety_days_ago
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    historical_data = query.group_by(func.date(models.Sale.sale_date)).all()
    
    if len(historical_data) < 7:
        raise HTTPException(status_code=400, detail="Insufficient data for forecasting")
    
    # Simple moving average forecast with trend
    sales_values = [float(row.total_sales) for row in historical_data]
    
    # Calculate trend
    x = np.arange(len(sales_values))
    z = np.polyfit(x, sales_values, 1)
    trend = z[0]
    
    # Moving average
    window = min(7, len(sales_values))
    moving_avg = np.mean(sales_values[-window:])
    
    # Generate forecast
    forecasts = []
    last_date = historical_data[-1].date
    
    for i in range(1, days + 1):
        forecast_date = last_date + timedelta(days=i)
        predicted_value = moving_avg + (trend * i)
        
        # Add confidence interval (±15%)
        confidence_range = predicted_value * 0.15
        
        forecasts.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "predicted_sales": round(predicted_value, 2),
            "confidence_interval_low": round(predicted_value - confidence_range, 2),
            "confidence_interval_high": round(predicted_value + confidence_range, 2)
        })
    
    return {
        "forecast_period": f"{days} days",
        "trend": "increasing" if trend > 0 else "decreasing",
        "trend_percentage": round(abs(trend) / moving_avg * 100, 2),
        "forecasts": forecasts
    }

# ============ CUSTOMER SEGMENTATION (RFM ANALYSIS) ============

@router.get("/customers/segmentation")
def customer_segmentation(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Advanced RFM (Recency, Frequency, Monetary) customer segmentation"""
    
    # Get all customers with their purchase history
    query = db.query(models.Customer).filter(models.Customer.id.isnot(None))
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Customer.store_id == current_user.store_id)
    
    customers = query.all()
    
    segments = {
        "champions": {"customers": [], "avg_value": 0, "total_revenue": 0},
        "loyal_customers": {"customers": [], "avg_value": 0, "total_revenue": 0},
        "potential_loyalists": {"customers": [], "avg_value": 0, "total_revenue": 0},
        "at_risk": {"customers": [], "avg_value": 0, "total_revenue": 0},
        "hibernating": {"customers": [], "avg_value": 0, "total_revenue": 0},
        "lost": {"customers": [], "avg_value": 0, "total_revenue": 0}
    }
    
    for customer in customers:
        # Get customer's sales
        sales = db.query(models.Sale).filter(
            models.Sale.customer_id == customer.id
        ).all()
        
        if not sales:
            continue
        
        # Calculate RFM metrics
        last_purchase = max(sale.sale_date for sale in sales)
        recency = (datetime.now() - last_purchase).days
        frequency = len(sales)
        monetary = sum(sale.total_amount for sale in sales)
        
        # Segment based on RFM
        if recency <= 30 and frequency >= 5 and monetary >= 50000:
            segment = "champions"
        elif recency <= 60 and frequency >= 3:
            segment = "loyal_customers"
        elif recency <= 90 and frequency >= 2:
            segment = "potential_loyalists"
        elif recency > 90 and recency <= 180 and frequency >= 2:
            segment = "at_risk"
        elif recency > 180 and frequency >= 2:
            segment = "hibernating"
        else:
            segment = "lost"
        
        segments[segment]["customers"].append(customer.id)
        segments[segment]["total_revenue"] += monetary
    
    # Calculate averages
    result = []
    for segment_name, data in segments.items():
        count = len(data["customers"])
        if count > 0:
            result.append({
                "segment": segment_name,
                "customer_count": count,
                "avg_order_value": round(data["total_revenue"] / count, 2),
                "total_revenue": round(data["total_revenue"], 2),
                "characteristics": {
                    "champions": "Best customers - Recent, frequent, high value",
                    "loyal_customers": "Regular buyers - Good frequency",
                    "potential_loyalists": "Recent buyers - Can become loyal",
                    "at_risk": "Haven't purchased recently - Need attention",
                    "hibernating": "Long time since purchase - Re-engage",
                    "lost": "Inactive customers - Win-back campaigns"
                }.get(segment_name, "")
            })
    
    return {"segments": result}

# ============ PRODUCT RECOMMENDATIONS ============

@router.get("/recommendations/customer/{customer_id}")
def get_customer_recommendations(
    customer_id: int,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """AI-powered product recommendations based on purchase history"""
    
    # Get customer's purchase history
    customer_purchases = db.query(models.SaleItem.product_id).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).filter(
        models.Sale.customer_id == customer_id
    ).all()
    
    purchased_product_ids = [p.product_id for p in customer_purchases]
    
    if not purchased_product_ids:
        # New customer - recommend popular products
        popular_products = db.query(
            models.Product.id,
            models.Product.name,
            func.count(models.SaleItem.id).label('sales_count')
        ).join(
            models.SaleItem, models.Product.id == models.SaleItem.product_id
        ).group_by(
            models.Product.id, models.Product.name
        ).order_by(
            func.count(models.SaleItem.id).desc()
        ).limit(limit).all()
        
        return {
            "recommendations": [
                {
                    "product_id": p.id,
                    "product_name": p.name,
                    "confidence_score": 0.7,
                    "reason": "Popular product - trending now"
                }
                for p in popular_products
            ]
        }
    
    # Find products frequently bought together (collaborative filtering)
    # Get customers who bought similar products
    similar_customers = db.query(models.Sale.customer_id).join(
        models.SaleItem, models.Sale.id == models.SaleItem.sale_id
    ).filter(
        models.SaleItem.product_id.in_(purchased_product_ids),
        models.Sale.customer_id != customer_id
    ).distinct().limit(50).all()
    
    similar_customer_ids = [c.customer_id for c in similar_customers]
    
    # Get products these similar customers bought
    recommended_products = db.query(
        models.Product.id,
        models.Product.name,
        func.count(models.SaleItem.id).label('frequency')
    ).join(
        models.SaleItem, models.Product.id == models.SaleItem.product_id
    ).join(
        models.Sale, models.SaleItem.sale_id == models.Sale.id
    ).filter(
        models.Sale.customer_id.in_(similar_customer_ids),
        models.Product.id.notin_(purchased_product_ids)
    ).group_by(
        models.Product.id, models.Product.name
    ).order_by(
        func.count(models.SaleItem.id).desc()
    ).limit(limit).all()
    
    recommendations = []
    for product in recommended_products:
        confidence = min(0.9, product.frequency / len(similar_customer_ids))
        recommendations.append({
            "product_id": product.id,
            "product_name": product.name,
            "confidence_score": round(confidence, 2),
            "reason": "Customers like you also bought this"
        })
    
    return {"recommendations": recommendations}

# ============ COHORT ANALYSIS ============

@router.get("/cohort-analysis")
def cohort_analysis(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Cohort retention analysis - Track customer retention over time"""
    
    start_date = datetime.now() - timedelta(days=months * 30)
    
    # Get first purchase date for each customer
    first_purchases = db.query(
        models.Sale.customer_id,
        func.min(models.Sale.sale_date).label('first_purchase')
    ).filter(
        models.Sale.sale_date >= start_date
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        first_purchases = first_purchases.filter(models.Sale.store_id == current_user.store_id)
    
    first_purchases = first_purchases.group_by(models.Sale.customer_id).all()
    
    # Group customers by cohort (month of first purchase)
    cohorts = defaultdict(list)
    for fp in first_purchases:
        cohort_month = fp.first_purchase.strftime("%Y-%m")
        cohorts[cohort_month].append(fp.customer_id)
    
    # Calculate retention for each cohort
    cohort_data = []
    for cohort_month, customer_ids in sorted(cohorts.items()):
        cohort_size = len(customer_ids)
        
        # Calculate retention for each subsequent month
        retention = {}
        for i in range(6):  # 6 months retention
            month_start = datetime.strptime(cohort_month, "%Y-%m") + timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            
            # Count customers who made purchases in this month
            active_customers = db.query(func.count(func.distinct(models.Sale.customer_id))).filter(
                models.Sale.customer_id.in_(customer_ids),
                models.Sale.sale_date >= month_start,
                models.Sale.sale_date < month_end
            ).scalar()
            
            retention[f"month_{i}"] = round((active_customers / cohort_size * 100), 2)
        
        cohort_data.append({
            "cohort": cohort_month,
            "size": cohort_size,
            "retention": retention
        })
    
    return {"cohort_analysis": cohort_data}

# ============ CHURN PREDICTION ============

@router.get("/predict/churn")
def predict_customer_churn(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Predict which customers are at risk of churning"""
    
    query = db.query(models.Customer)
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Customer.store_id == current_user.store_id)
    
    customers = query.all()
    
    at_risk_customers = []
    
    for customer in customers:
        sales = db.query(models.Sale).filter(
            models.Sale.customer_id == customer.id
        ).order_by(models.Sale.sale_date.desc()).all()
        
        if not sales:
            continue
        
        last_purchase = sales[0].sale_date
        days_since_purchase = (datetime.now() - last_purchase).days
        purchase_frequency = len(sales)
        avg_order_value = sum(s.total_amount for s in sales) / len(sales)
        
        # Churn risk scoring
        churn_score = 0
        
        # Recency factor (30% weight)
        if days_since_purchase > 180:
            churn_score += 30
        elif days_since_purchase > 90:
            churn_score += 20
        elif days_since_purchase > 60:
            churn_score += 10
        
        # Frequency factor (30% weight)
        if purchase_frequency == 1:
            churn_score += 30
        elif purchase_frequency == 2:
            churn_score += 15
        
        # Declining purchase pattern (40% weight)
        if len(sales) >= 3:
            recent_3_avg = sum(s.total_amount for s in sales[:3]) / 3
            older_3_avg = sum(s.total_amount for s in sales[-3:]) / 3
            
            if recent_3_avg < older_3_avg * 0.7:
                churn_score += 40
            elif recent_3_avg < older_3_avg:
                churn_score += 20
        
        if churn_score >= 50:
            risk_level = "high" if churn_score >= 70 else "medium"
            at_risk_customers.append({
                "customer_id": customer.id,
                "customer_name": customer.name,
                "phone": customer.phone,
                "churn_score": churn_score,
                "risk_level": risk_level,
                "days_since_purchase": days_since_purchase,
                "lifetime_value": round(customer.total_purchases, 2),
                "recommended_action": "Send personalized offer" if risk_level == "high" else "Send re-engagement email"
            })
    
    # Sort by churn score
    at_risk_customers.sort(key=lambda x: x["churn_score"], reverse=True)
    
    return {
        "total_at_risk": len(at_risk_customers),
        "high_risk_count": len([c for c in at_risk_customers if c["risk_level"] == "high"]),
        "customers": at_risk_customers[:50]  # Top 50
    }

# ============ PRODUCT AFFINITY ANALYSIS ============

@router.get("/product-affinity")
def product_affinity_analysis(
    product_id: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Market basket analysis - Products frequently bought together"""
    
    if product_id:
        # Find products bought together with this product
        sales_with_product = db.query(models.Sale.id).join(
            models.SaleItem, models.Sale.id == models.SaleItem.sale_id
        ).filter(
            models.SaleItem.product_id == product_id
        ).all()
        
        sale_ids = [s.id for s in sales_with_product]
        
        # Find other products in those sales
        affinity_products = db.query(
            models.Product.id,
            models.Product.name,
            func.count(models.SaleItem.id).label('frequency')
        ).join(
            models.SaleItem, models.Product.id == models.SaleItem.product_id
        ).filter(
            models.SaleItem.sale_id.in_(sale_ids),
            models.Product.id != product_id
        ).group_by(
            models.Product.id, models.Product.name
        ).order_by(
            func.count(models.SaleItem.id).desc()
        ).limit(limit).all()
        
        total_sales = len(sale_ids)
        
        return {
            "product_id": product_id,
            "frequently_bought_with": [
                {
                    "product_id": p.id,
                    "product_name": p.name,
                    "co_occurrence_count": p.frequency,
                    "affinity_score": round(p.frequency / total_sales * 100, 2)
                }
                for p in affinity_products
            ]
        }
    else:
        # Overall product pairs analysis
        return {"message": "Provide product_id to see affinity analysis"}

# ============ AUTOMATED INSIGHTS ============

@router.get("/insights/automated")
def automated_insights(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """AI-generated business insights and recommendations"""
    
    insights = []
    
    # Insight 1: Sales trend
    last_30_days = datetime.now() - timedelta(days=30)
    previous_30_days = datetime.now() - timedelta(days=60)
    
    query = db.query(func.sum(models.Sale.total_amount)).filter(
        models.Sale.sale_date >= last_30_days
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    recent_sales = query.scalar() or 0
    
    query = db.query(func.sum(models.Sale.total_amount)).filter(
        models.Sale.sale_date >= previous_30_days,
        models.Sale.sale_date < last_30_days
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    previous_sales = query.scalar() or 0
    
    if previous_sales > 0:
        growth = ((recent_sales - previous_sales) / previous_sales) * 100
        insights.append({
            "type": "sales_trend",
            "severity": "positive" if growth > 0 else "warning",
            "title": f"Sales {'Growth' if growth > 0 else 'Decline'} Detected",
            "description": f"Sales have {'increased' if growth > 0 else 'decreased'} by {abs(growth):.1f}% compared to previous period",
            "recommendation": "Continue current strategy" if growth > 0 else "Review marketing campaigns and customer engagement"
        })
    
    # Insight 2: Low stock items
    low_stock = db.query(models.Product).filter(
        models.Product.current_stock <= models.Product.minimum_stock,
        models.Product.is_active == True
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        low_stock = low_stock.filter(models.Product.store_id == current_user.store_id)
    
    low_stock_count = low_stock.count()
    
    if low_stock_count > 0:
        insights.append({
            "type": "inventory_alert",
            "severity": "critical" if low_stock_count > 10 else "warning",
            "title": f"{low_stock_count} Products Low on Stock",
            "description": f"Immediate restocking needed for {low_stock_count} items",
            "recommendation": "Review reorder level report and place orders immediately"
        })
    
    # Insight 3: Customer engagement
    thirty_days_ago = datetime.now() - timedelta(days=30)
    inactive_customers = db.query(models.Customer).filter(
        models.Customer.id.notin_(
            db.query(models.Sale.customer_id).filter(
                models.Sale.sale_date >= thirty_days_ago
            )
        )
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        inactive_customers = inactive_customers.filter(models.Customer.store_id == current_user.store_id)
    
    inactive_count = inactive_customers.count()
    
    if inactive_count > 0:
        insights.append({
            "type": "customer_engagement",
            "severity": "warning",
            "title": f"{inactive_count} Inactive Customers",
            "description": f"{inactive_count} customers haven't purchased in last 30 days",
            "recommendation": "Launch re-engagement campaign with special offers"
        })
    
    return {"insights": insights, "total_insights": len(insights)}

# ============ PEAK HOURS ANALYSIS ============

@router.get("/analytics/peak-hours")
def peak_hours_analysis(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Analyze peak sales hours for optimal staffing"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(
        extract('hour', models.Sale.sale_date).label('hour'),
        func.count(models.Sale.id).label('transaction_count'),
        func.sum(models.Sale.total_amount).label('total_sales')
    ).filter(
        models.Sale.sale_date >= start_date
    )
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Sale.store_id == current_user.store_id)
    
    results = query.group_by(extract('hour', models.Sale.sale_date)).all()
    
    hourly_data = []
    for row in results:
        hour = int(row.hour)
        hourly_data.append({
            "hour": f"{hour:02d}:00",
            "transaction_count": int(row.transaction_count),
            "total_sales": round(float(row.total_sales), 2)
        })
    
    # Sort by hour
    hourly_data.sort(key=lambda x: x["hour"])
    
    # Identify peak hours
    if hourly_data:
        max_transactions = max(h["transaction_count"] for h in hourly_data)
        peak_hours = [h for h in hourly_data if h["transaction_count"] >= max_transactions * 0.8]
        
        return {
            "analysis_period": f"{days} days",
            "hourly_breakdown": hourly_data,
            "peak_hours": [h["hour"] for h in peak_hours],
            "recommendation": f"Ensure optimal staffing between {peak_hours[0]['hour']} and {peak_hours[-1]['hour']}"
        }
    
    return {"hourly_breakdown": [], "peak_hours": []}

