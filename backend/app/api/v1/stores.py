from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas.store import StoreCreate, StoreUpdate, StoreResponse, StoreStats
from app.api.dependencies import get_super_admin, get_current_user
import json

router = APIRouter()

@router.post("/", response_model=StoreResponse)
def create_store(
    store: StoreCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_super_admin)
):
    """Create a new store (Super Admin only)"""
    # Check if store with same name exists
    existing_store = db.query(models.Store).filter(
        models.Store.name == store.name
    ).first()
    
    if existing_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Store with this name already exists"
        )
    
    db_store = models.Store(**store.model_dump())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="store",
        entity_id=db_store.id,
        details=json.dumps({"name": db_store.name})
    )
    db.add(audit_log)
    db.commit()
    
    return db_store

@router.get("/", response_model=List[StoreResponse])
def get_stores(
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_super_admin)
):
    """Get all stores (Super Admin only)"""
    query = db.query(models.Store)
    
    if not include_inactive:
        query = query.filter(models.Store.is_active == True)
    
    stores = query.offset(skip).limit(limit).all()
    return stores

@router.get("/stats", response_model=List[StoreStats])
def get_stores_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get statistics for all stores"""
    # Super admin sees all stores, others see their store only
    if current_user.role == models.UserRole.SUPER_ADMIN:
        stores = db.query(models.Store).filter(models.Store.is_active == True).all()
    else:
        stores = db.query(models.Store).filter(
            models.Store.id == current_user.store_id,
            models.Store.is_active == True
        ).all()
    
    stats = []
    for store in stores:
        # Count products
        total_products = db.query(models.Product).filter(
            models.Product.store_id == store.id,
            models.Product.is_active == True
        ).count()
        
        # Sum sales
        total_sales = db.query(func.sum(models.Sale.total_amount)).filter(
            models.Sale.store_id == store.id
        ).scalar() or 0
        
        # Count customers (Customer model doesn't have is_active)
        total_customers = db.query(models.Customer).filter(
            models.Customer.store_id == store.id
        ).count()
        
        # Count users
        total_users = db.query(models.User).filter(
            models.User.store_id == store.id,
            models.User.is_active == True
        ).count()
        
        stats.append(StoreStats(
            store_id=store.id,
            store_name=store.name,
            total_products=total_products,
            total_sales=float(total_sales),
            total_customers=total_customers,
            total_users=total_users
        ))
    
    return stats

@router.get("/{store_id}", response_model=StoreResponse)
def get_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_super_admin)
):
    """Get a specific store (Super Admin only)"""
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    return store

@router.put("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: int,
    store_update: StoreUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_super_admin)
):
    """Update a store (Super Admin only)"""
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    # Check if updating to a name that already exists
    if store_update.name and store_update.name != store.name:
        existing = db.query(models.Store).filter(
            models.Store.name == store_update.name,
            models.Store.id != store_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Store with this name already exists"
            )
    
    update_data = store_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(store, field, value)
    
    db.commit()
    db.refresh(store)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="update",
        entity_type="store",
        entity_id=store.id,
        details=json.dumps(update_data, default=str)
    )
    db.add(audit_log)
    db.commit()
    
    return store

@router.delete("/{store_id}")
def delete_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_super_admin)
):
    """Delete/deactivate a store (Super Admin only)"""
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    
    # Check if store has active users
    active_users = db.query(models.User).filter(
        models.User.store_id == store_id,
        models.User.is_active == True
    ).count()
    
    if active_users > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete store with {active_users} active users. Deactivate users first."
        )
    
    # Soft delete - just deactivate
    store.is_active = False
    db.commit()
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="delete",
        entity_type="store",
        entity_id=store_id,
        details=json.dumps({"name": store.name})
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Store deactivated successfully"}

