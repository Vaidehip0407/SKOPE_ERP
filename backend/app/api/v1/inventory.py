from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, BatchCreate, BatchResponse
from app.api.dependencies import get_current_user, get_store_manager_or_admin
import json

router = APIRouter()

# Products endpoints
@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    # Check if SKU already exists
    existing_product = db.query(models.Product).filter(
        models.Product.sku == product.sku
    ).first()
    
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )
    
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="product",
        entity_id=db_product.id,
        details=json.dumps({"sku": db_product.sku, "name": db_product.name})
    )
    db.add(audit_log)
    db.commit()
    
    return db_product

@router.get("/products", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    store_id: int = None,
    low_stock: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Product)
    
    # Filter by store
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    elif store_id:
        query = query.filter(models.Product.store_id == store_id)
    
    # Filter for low stock
    if low_stock:
        query = query.filter(models.Product.current_stock <= models.Product.minimum_stock)
    
    products = query.filter(models.Product.is_active == True).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if product.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if product.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="update",
        entity_type="product",
        entity_id=product.id,
        details=json.dumps(update_data, default=str)
    )
    db.add(audit_log)
    db.commit()
    
    return product

# Batch tracking endpoints
@router.post("/batches", response_model=BatchResponse)
def create_batch(
    batch: BatchCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == batch.product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if batch ID already exists
    existing_batch = db.query(models.Batch).filter(
        models.Batch.batch_id == batch.batch_id
    ).first()
    
    if existing_batch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch with this ID already exists"
        )
    
    db_batch = models.Batch(
        **batch.model_dump(),
        remaining_quantity=batch.quantity
    )
    db.add(db_batch)
    
    # Update product stock
    product.current_stock += batch.quantity
    
    db.commit()
    db.refresh(db_batch)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="batch",
        entity_id=db_batch.id,
        details=json.dumps({"batch_id": db_batch.batch_id, "product_id": batch.product_id, "quantity": batch.quantity})
    )
    db.add(audit_log)
    db.commit()
    
    return db_batch

@router.get("/batches", response_model=List[BatchResponse])
def get_batches(
    product_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Batch)
    
    if product_id:
        query = query.filter(models.Batch.product_id == product_id)
    
    batches = query.offset(skip).limit(limit).all()
    return batches

@router.get("/dashboard")
def get_inventory_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Get total products
    query = db.query(models.Product)
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Product.store_id == current_user.store_id)
    
    total_products = query.filter(models.Product.is_active == True).count()
    low_stock_products = query.filter(
        models.Product.current_stock <= models.Product.minimum_stock,
        models.Product.is_active == True
    ).count()
    out_of_stock_products = query.filter(
        models.Product.current_stock == 0,
        models.Product.is_active == True
    ).count()
    
    total_stock_value = db.query(
        models.Product
    ).filter(
        models.Product.store_id == current_user.store_id if current_user.role != models.UserRole.SUPER_ADMIN else True
    ).with_entities(
        models.Product.current_stock * models.Product.cost_price
    ).all()
    
    stock_value = sum([val[0] if val[0] else 0 for val in total_stock_value])
    
    return {
        "total_products": total_products,
        "low_stock_products": low_stock_products,
        "out_of_stock_products": out_of_stock_products,
        "total_stock_value": round(stock_value, 2)
    }

