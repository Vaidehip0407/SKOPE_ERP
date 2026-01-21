from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.db import models
from app.schemas.user import UserLogin, Token, UserResponse, PasswordChange
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.api.dependencies import get_current_user
import json

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Check if logging in with username or email
    user = db.query(models.User).filter(
        (models.User.username == user_credentials.username) |
        (models.User.email == user_credentials.username)
    ).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=user.id,
        action="login",
        entity_type="user",
        entity_id=user.id,
        details=json.dumps({"username": user.username})
    )
    db.add(audit_log)
    db.commit()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="password_change",
        entity_type="user",
        entity_id=current_user.id
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user

