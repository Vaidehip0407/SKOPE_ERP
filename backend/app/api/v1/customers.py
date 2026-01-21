from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerWithPurchaseHistory
from app.api.dependencies import get_current_user
import json

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Check if customer with same phone exists in the store
    existing_customer = db.query(models.Customer).filter(
        models.Customer.phone == customer.phone,
        models.Customer.store_id == customer.store_id
    ).first()
    
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this phone number already exists in this store"
        )
    
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="customer",
        entity_id=db_customer.id,
        details=json.dumps({"name": db_customer.name, "phone": db_customer.phone})
    )
    db.add(audit_log)
    db.commit()
    
    return db_customer

@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    skip: int = 0,
    limit: int = 100,
    store_id: int = None,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Customer)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Customer.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Customer.store_id == store_id)
    
    # Search by name or phone
    if search:
        query = query.filter(
            (models.Customer.name.ilike(f"%{search}%")) |
            (models.Customer.phone.ilike(f"%{search}%"))
        )
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if customer.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return customer

@router.get("/{customer_id}/purchase-history")
def get_customer_purchase_history(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if customer.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Get sales
    sales = db.query(models.Sale).filter(
        models.Sale.customer_id == customer_id
    ).order_by(models.Sale.sale_date.desc()).all()
    
    # Get warranty information
    warranties = []
    for sale in sales:
        for item in sale.sale_items:
            if item.warranty_expires_at:
                warranties.append({
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "serial_number": item.serial_number,
                    "purchase_date": sale.sale_date,
                    "warranty_expires_at": item.warranty_expires_at,
                    "invoice_number": sale.invoice_number
                })
    
    return {
        "customer": customer,
        "total_purchases": customer.total_purchases,
        "purchase_count": len(sales),
        "recent_purchases": sales[:10],
        "active_warranties": [w for w in warranties if w["warranty_expires_at"] > func.now()]
    }

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if customer.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    update_data = customer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="update",
        entity_type="customer",
        entity_id=customer.id,
        details=json.dumps(update_data, default=str)
    )
    db.add(audit_log)
    db.commit()
    
    return customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if customer.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Check if customer has sales
    has_sales = db.query(models.Sale).filter(models.Sale.customer_id == customer_id).first()
    if has_sales:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete customer with existing sales records"
        )
    
    db.delete(customer)
    db.commit()
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="delete",
        entity_type="customer",
        entity_id=customer_id,
        details=json.dumps({"name": customer.name, "phone": customer.phone})
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Customer deleted successfully"}

