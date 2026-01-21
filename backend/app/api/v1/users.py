from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash
from app.api.dependencies import get_current_user, get_super_admin, get_store_manager_or_admin
import json

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    # Check if user already exists
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Store Managers can only create staff roles for their store
    if current_user.role == models.UserRole.STORE_MANAGER:
        # Restrict to staff roles only
        if user.role in [models.UserRole.SUPER_ADMIN, models.UserRole.STORE_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Store Managers can only create staff users (Sales, Marketing, Accounts)"
            )
        # Must be for their store
        if user.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create users for your store"
            )
    
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        store_id=user.store_id if current_user.role == models.UserRole.SUPER_ADMIN else current_user.store_id,
        hashed_password=get_password_hash(user.password)
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="user",
        entity_id=db_user.id,
        details=json.dumps({"username": db_user.username, "role": db_user.role.value})
    )
    db.add(audit_log)
    db.commit()
    
    return db_user

@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.UserRole.SUPER_ADMIN:
        users = db.query(models.User).offset(skip).limit(limit).all()
    else:
        users = db.query(models.User).filter(
            models.User.store_id == current_user.store_id
        ).offset(skip).limit(limit).all()
    
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN:
        if user.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Store Managers can only edit users in their store and cannot change roles to admin/manager
    if current_user.role == models.UserRole.STORE_MANAGER:
        if user.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit users from your store"
            )
        # Cannot edit Super Admin or other Store Managers
        if user.role in [models.UserRole.SUPER_ADMIN, models.UserRole.STORE_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot edit Super Admin or Store Manager users"
            )
        # Cannot change role to admin/manager
        if user_update.role and user_update.role in [models.UserRole.SUPER_ADMIN, models.UserRole.STORE_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot promote users to Super Admin or Store Manager"
            )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "password":
            setattr(user, "hashed_password", get_password_hash(value))
        else:
            setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="update",
        entity_type="user",
        entity_id=user.id,
        details=json.dumps({k: str(v) for k, v in update_data.items() if k != "password"}, default=str)
    )
    db.add(audit_log)
    db.commit()
    
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_store_manager_or_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Store Managers can only delete staff from their store
    if current_user.role == models.UserRole.STORE_MANAGER:
        if user.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete users from your store"
            )
        # Cannot delete Super Admin or other Store Managers
        if user.role in [models.UserRole.SUPER_ADMIN, models.UserRole.STORE_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot delete Super Admin or Store Manager users"
            )
    
    db.delete(user)
    db.commit()
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="delete",
        entity_type="user",
        entity_id=user_id,
        details=json.dumps({"username": user.username})
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "User deleted successfully"}

