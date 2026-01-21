from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.db import models
from app.schemas.marketing import (
    MarketingIntegrationCreate,
    MarketingIntegrationUpdate,
    MarketingIntegrationResponse,
    MarketingCampaignSyncResponse,
    GoogleAdsAuthRequest,
    MetaAdsAuthRequest
)
from app.api.dependencies import get_current_user
import json

router = APIRouter()

# Google Ads Integration Endpoints

@router.post("/integrations/google-ads/auth")
def connect_google_ads(
    auth_data: GoogleAdsAuthRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Connect Google Ads account
    In production, this would:
    1. Exchange authorization code for access token with Google OAuth
    2. Fetch account details
    3. Store encrypted credentials
    """
    # TODO: Implement Google OAuth flow
    # For now, return a placeholder
    return {
        "success": True,
        "message": "Google Ads integration ready. OAuth implementation pending.",
        "platform": "google_ads",
        "note": "Production requires: Google Ads API credentials, OAuth 2.0 setup"
    }

@router.post("/integrations/meta-ads/auth")
def connect_meta_ads(
    auth_data: MetaAdsAuthRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Connect Meta (Facebook/Instagram) Ads account
    In production, this would:
    1. Validate access token with Meta API
    2. Fetch ad account details
    3. Store encrypted credentials
    """
    # TODO: Implement Meta OAuth flow
    # For now, return a placeholder
    return {
        "success": True,
        "message": "Meta Ads integration ready. OAuth implementation pending.",
        "platform": "meta_ads",
        "note": "Production requires: Facebook App ID, Business Manager access"
    }

@router.get("/integrations", response_model=List[MarketingIntegrationResponse])
def get_integrations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all marketing integrations for current user's store"""
    query = db.query(models.MarketingIntegration)
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.MarketingIntegration.store_id == current_user.store_id)
    
    integrations = query.all()
    return integrations

@router.post("/integrations", response_model=MarketingIntegrationResponse)
def create_integration(
    integration: MarketingIntegrationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new marketing integration"""
    db_integration = models.MarketingIntegration(
        **integration.model_dump(),
        created_by=current_user.id
    )
    
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    
    # Create audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        action="create",
        entity_type="marketing_integration",
        entity_id=db_integration.id,
        details=json.dumps({
            "platform": db_integration.platform,
            "account_name": db_integration.account_name
        })
    )
    db.add(audit_log)
    db.commit()
    
    return db_integration

@router.delete("/integrations/{integration_id}")
def delete_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a marketing integration"""
    integration = db.query(models.MarketingIntegration).filter(
        models.MarketingIntegration.id == integration_id
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    # Check permissions
    if current_user.role != models.UserRole.SUPER_ADMIN and integration.store_id != current_user.store_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this integration"
        )
    
    db.delete(integration)
    db.commit()
    
    return {"success": True, "message": "Integration deleted"}

@router.post("/sync/google-ads/{integration_id}")
def sync_google_ads_campaigns(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Sync campaigns from Google Ads
    In production, this would:
    1. Fetch campaigns from Google Ads API
    2. Update local database with campaign performance
    3. Return summary of synced campaigns
    """
    integration = db.query(models.MarketingIntegration).filter(
        models.MarketingIntegration.id == integration_id,
        models.MarketingIntegration.platform == "google_ads"
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Google Ads integration not found"
        )
    
    # TODO: Implement Google Ads API sync
    return {
        "success": True,
        "message": "Google Ads sync initiated",
        "campaigns_synced": 0,
        "note": "Production requires: Google Ads API client library, active campaigns"
    }

@router.post("/sync/meta-ads/{integration_id}")
def sync_meta_ads_campaigns(
    integration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Sync campaigns from Meta Ads
    In production, this would:
    1. Fetch campaigns from Meta Marketing API
    2. Update local database with campaign performance
    3. Return summary of synced campaigns
    """
    integration = db.query(models.MarketingIntegration).filter(
        models.MarketingIntegration.id == integration_id,
        models.MarketingIntegration.platform == "meta_ads"
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meta Ads integration not found"
        )
    
    # TODO: Implement Meta Marketing API sync
    return {
        "success": True,
        "message": "Meta Ads sync initiated",
        "campaigns_synced": 0,
        "note": "Production requires: Facebook Marketing API, Business Manager access"
    }

@router.get("/campaigns/synced", response_model=List[MarketingCampaignSyncResponse])
def get_synced_campaigns(
    platform: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get all synced marketing campaigns"""
    query = db.query(models.MarketingCampaignSync).join(models.MarketingIntegration)
    
    if current_user.role != models.UserRole.SUPER_ADMIN:
        query = query.filter(models.MarketingIntegration.store_id == current_user.store_id)
    
    if platform:
        query = query.filter(models.MarketingCampaignSync.platform == platform)
    
    campaigns = query.order_by(models.MarketingCampaignSync.last_synced_at.desc()).all()
    return campaigns


