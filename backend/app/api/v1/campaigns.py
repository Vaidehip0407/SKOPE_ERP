from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.db import models
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignStats
from app.api.dependencies import get_current_user, require_role
from app.db.models import UserRole
import json
import traceback

router = APIRouter()

@router.post("/", response_model=CampaignResponse)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new marketing campaign"""
    try:
        print(f"\n=== Creating Campaign ===")
        print(f"User: {current_user.username} (ID: {current_user.id})")
        print(f"Campaign Name: {campaign.name}")
        print(f"Store ID: {campaign.store_id}")
        print(f"Campaign Type: {campaign.campaign_type}")
        print(f"Trigger Type: {campaign.trigger_type}")
        
        # Validate store exists
        store = db.query(models.Store).filter(models.Store.id == campaign.store_id).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Store with ID {campaign.store_id} not found"
            )
        
        # Create campaign with explicit field mapping
        db_campaign = models.Campaign(
            name=campaign.name,
            description=campaign.description,
            campaign_type=campaign.campaign_type,
            trigger_type=campaign.trigger_type,
            message_template=campaign.message_template,
            subject=campaign.subject,
            store_id=campaign.store_id,
            target_customers=campaign.target_customers,
            geo_location=campaign.geo_location,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            send_time=campaign.send_time,
            days_before_trigger=campaign.days_before_trigger,
            discount_code=campaign.discount_code,
            discount_percentage=campaign.discount_percentage,
            status=models.CampaignStatus.DRAFT,
            total_sent=0,
            total_opened=0,
            total_clicked=0,
            total_converted=0,
            created_by=current_user.id
        )
        
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        
        print(f"Campaign created with ID: {db_campaign.id}")
        
        # Create audit log
        try:
            audit_log = models.AuditLog(
                user_id=current_user.id,
                action="create",
                entity_type="campaign",
                entity_id=db_campaign.id,
                details=json.dumps({"name": db_campaign.name, "type": db_campaign.campaign_type.value})
            )
            db.add(audit_log)
            db.commit()
        except Exception as audit_error:
            print(f"Warning: Could not create audit log: {audit_error}")
        
        return db_campaign
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        error_detail = f"Failed to create campaign: {str(e)}"
        print(f"ERROR: {error_detail}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )

@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    campaign_type: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all campaigns"""
    query = db.query(models.Campaign)
    
    # Filter by store
    if current_user.role != UserRole.SUPER_ADMIN:
        query = query.filter(models.Campaign.store_id == current_user.store_id)
    
    # Filter by status
    if status:
        query = query.filter(models.Campaign.status == status)
    
    # Filter by type
    if campaign_type:
        query = query.filter(models.Campaign.campaign_type == campaign_type)
    
    campaigns = query.order_by(models.Campaign.created_at.desc()).offset(skip).limit(limit).all()
    return campaigns

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get campaign by ID"""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if campaign.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    return campaign

@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    campaign_update: CampaignUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update campaign"""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if campaign.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    update_data = campaign_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="update",
        entity_type="campaign",
        entity_id=campaign.id,
        details=json.dumps(update_data, default=str)
    )
    db.add(audit_log)
    db.commit()
    
    return campaign

@router.post("/{campaign_id}/activate")
def activate_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Activate a campaign"""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign.status = models.CampaignStatus.ACTIVE
    db.commit()
    
    return {"message": "Campaign activated successfully", "campaign_id": campaign_id}

@router.post("/{campaign_id}/pause")
def pause_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Pause a campaign"""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign.status = models.CampaignStatus.PAUSED
    db.commit()
    
    return {"message": "Campaign paused successfully", "campaign_id": campaign_id}

@router.get("/{campaign_id}/stats", response_model=CampaignStats)
def get_campaign_stats(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get campaign statistics"""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Calculate rates
    open_rate = (campaign.total_opened / campaign.total_sent * 100) if campaign.total_sent > 0 else 0
    click_rate = (campaign.total_clicked / campaign.total_sent * 100) if campaign.total_sent > 0 else 0
    conversion_rate = (campaign.total_converted / campaign.total_sent * 100) if campaign.total_sent > 0 else 0
    
    return {
        "campaign_id": campaign.id,
        "campaign_name": campaign.name,
        "total_sent": campaign.total_sent,
        "total_opened": campaign.total_opened,
        "total_clicked": campaign.total_clicked,
        "total_converted": campaign.total_converted,
        "open_rate": round(open_rate, 2),
        "click_rate": round(click_rate, 2),
        "conversion_rate": round(conversion_rate, 2)
    }

@router.get("/dashboard/stats")
def get_marketing_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get marketing dashboard stats"""
    query = db.query(models.Campaign)
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.Campaign.store_id == current_user.store_id)
    
    campaigns = query.all()
    
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.status == models.CampaignStatus.ACTIVE])
    total_sent = sum(int(c.total_sent or 0) for c in campaigns)
    total_converted = sum(int(c.total_converted or 0) for c in campaigns)
    
    avg_conversion_rate = (total_converted / total_sent * 100) if total_sent > 0 else 0
    
    return {
        "total_campaigns": total_campaigns,
        "active_campaigns": active_campaigns,
        "total_messages_sent": total_sent,
        "total_conversions": total_converted,
        "average_conversion_rate": round(avg_conversion_rate, 2)
    }

@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a campaign"""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Check permissions
    if current_user.role != UserRole.SUPER_ADMIN:
        if campaign.store_id != current_user.store_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    db.delete(campaign)
    db.commit()
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="delete",
        entity_type="campaign",
        entity_id=campaign_id,
        details=json.dumps({"name": campaign.name})
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Campaign deleted successfully"}

