from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarketingIntegrationBase(BaseModel):
    platform: str  # google_ads, meta_ads
    account_id: Optional[str] = None
    account_name: Optional[str] = None

class MarketingIntegrationCreate(MarketingIntegrationBase):
    store_id: int
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None

class MarketingIntegrationUpdate(BaseModel):
    account_name: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class MarketingIntegrationResponse(MarketingIntegrationBase):
    id: int
    store_id: int
    is_active: bool
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class MarketingCampaignSyncResponse(BaseModel):
    id: int
    integration_id: int
    external_campaign_id: str
    campaign_name: str
    platform: str
    status: Optional[str] = None
    impressions: int
    clicks: int
    conversions: int
    spend: float
    ctr: float
    cpc: float
    roas: float
    last_synced_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class GoogleAdsAuthRequest(BaseModel):
    authorization_code: str
    redirect_uri: str

class MetaAdsAuthRequest(BaseModel):
    access_token: str
    ad_account_id: str


