"""
Comprehensive Marketing Data Seeder
Seeds all marketing-related sample data for demo including:
- Ad account connections (Google Ads, Meta)
- Multiple campaigns with different statuses
- 30+ days of analytics data per campaign
- Custom audiences
- Creative assets references
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from decimal import Decimal
import random
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db import models

# Sample campaign templates
CAMPAIGN_DATA = [
    {
        "name": "Diwali Mega Sale 2025",
        "template": "offer_festival",
        "platform": "meta",
        "objective": "OUTCOME_SALES",
        "budget_daily": 2500,
        "headline": "Up to 50% OFF on Electronics!",
        "description": "Don't miss our biggest Diwali sale ever. Premium TVs, ACs, and mobiles at unbeatable prices.",
        "status": "active",
    },
    {
        "name": "Store Visit Campaign - Mumbai",
        "template": "store_visit",
        "platform": "meta",
        "objective": "OUTCOME_TRAFFIC",
        "budget_daily": 1500,
        "headline": "Visit Our Store Today!",
        "description": "Experience our products in person. Expert assistance and exclusive in-store deals.",
        "status": "active",
    },
    {
        "name": "WhatsApp Lead Generation",
        "template": "whatsapp_click",
        "platform": "meta",
        "objective": "OUTCOME_ENGAGEMENT",
        "budget_daily": 1000,
        "headline": "Chat with Us on WhatsApp",
        "description": "Get instant quotes and exclusive deals. Message us now!",
        "status": "active",
    },
    {
        "name": "Google Local Search Ads",
        "template": "local_search_ads",
        "platform": "google",
        "objective": "LEADS",
        "budget_daily": 2000,
        "headline": "Best Electronics Store Near You",
        "description": "Top-rated electronics store in your area. Free delivery on orders above ₹5000.",
        "status": "active",
    },
    {
        "name": "Performance Max - High Value Products",
        "template": "performance_max",
        "platform": "google",
        "objective": "SALES",
        "budget_daily": 3000,
        "headline": "Premium Electronics at Best Prices",
        "description": "Samsung, LG, Sony - All major brands at competitive prices.",
        "status": "active",
    },
    {
        "name": "New Year 2026 Promo",
        "template": "offer_festival",
        "platform": "meta",
        "objective": "OUTCOME_SALES",
        "budget_daily": 3500,
        "headline": "New Year, New Deals!",
        "description": "Start 2026 with amazing offers on smartphones and laptops.",
        "status": "draft",
    },
    {
        "name": "Remarketing - Past Visitors",
        "template": "display_remarketing",
        "platform": "google",
        "objective": "AWARENESS",
        "budget_daily": 800,
        "headline": "Still Thinking About It?",
        "description": "Come back for exclusive member-only discounts.",
        "status": "paused",
    },
    {
        "name": "Instagram Product Showcase",
        "template": "product_catalog",
        "platform": "meta",
        "objective": "OUTCOME_SALES",
        "budget_daily": 1800,
        "headline": "Shop Our Latest Collection",
        "description": "Swipe through our newest products. Tap to buy instantly!",
        "status": "completed",
    },
]


def seed_marketing_data():
    """Seed all marketing-related data"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("SEEDING MARKETING DATA")
        print("=" * 60)
        
        # Get store
        store = db.query(models.Store).first()
        if not store:
            print("❌ No store found! Run seed_reports_data.py first.")
            return
        
        print(f"✓ Using store: {store.name}")
        
        # Get admin user
        admin = db.query(models.User).filter(
            models.User.role == models.UserRole.ADMIN
        ).first()
        
        if not admin:
            admin = db.query(models.User).first()
        
        print(f"✓ Using user: {admin.username if admin else 'System'}")
        
        # Create Ad Account Connections
        print("\n--- Creating Ad Account Connections ---")
        
        connections = []
        
        # Meta connection
        meta_conn = db.query(models.AdAccountConnection).filter(
            models.AdAccountConnection.store_id == store.id,
            models.AdAccountConnection.platform == "meta"
        ).first()
        
        if not meta_conn:
            meta_conn = models.AdAccountConnection(
                store_id=store.id,
                platform="meta",
                meta_ad_account_id="act_123456789",
                meta_pixel_id="987654321",
                meta_page_id="112233445566",
                meta_business_id="998877665544",
                access_token="demo_meta_access_token_xxxxx",
                refresh_token=None,
                token_expires_at=datetime.utcnow() + timedelta(days=60),
                is_active=True,
                created_by=admin.id if admin else None
            )
            db.add(meta_conn)
            db.flush()
            print("✓ Created Meta Ads connection")
        else:
            print("✓ Meta Ads connection exists")
        connections.append(meta_conn)
        
        # Google connection
        google_conn = db.query(models.AdAccountConnection).filter(
            models.AdAccountConnection.store_id == store.id,
            models.AdAccountConnection.platform == "google"
        ).first()
        
        if not google_conn:
            google_conn = models.AdAccountConnection(
                store_id=store.id,
                platform="google",
                google_customer_id="123-456-7890",
                google_ga4_property="G-ABCDEFGHIJ",
                access_token="demo_google_access_token_xxxxx",
                refresh_token="demo_google_refresh_token_xxxxx",
                token_expires_at=datetime.utcnow() + timedelta(hours=1),
                is_active=True,
                created_by=admin.id if admin else None
            )
            db.add(google_conn)
            db.flush()
            print("✓ Created Google Ads connection")
        else:
            print("✓ Google Ads connection exists")
        connections.append(google_conn)
        
        db.commit()
        
        # Create Campaigns
        print("\n--- Creating Ad Campaigns ---")
        
        campaigns_created = []
        for cdata in CAMPAIGN_DATA:
            # Check if exists
            existing = db.query(models.AdCampaignCreation).filter(
                models.AdCampaignCreation.campaign_name == cdata["name"],
                models.AdCampaignCreation.store_id == store.id
            ).first()
            
            if existing:
                campaigns_created.append(existing)
                continue
            
            # Get correct ad account
            ad_account = meta_conn if cdata["platform"] == "meta" else google_conn
            
            # Set dates based on status
            if cdata["status"] == "completed":
                start_date = datetime.utcnow() - timedelta(days=45)
                end_date = datetime.utcnow() - timedelta(days=15)
            else:
                start_date = datetime.utcnow() - timedelta(days=15)
                end_date = datetime.utcnow() + timedelta(days=30)
            
            # Map status
            status_map = {
                "active": models.AdCampaignStatus.ACTIVE,
                "draft": models.AdCampaignStatus.DRAFT,
                "paused": models.AdCampaignStatus.PAUSED,
                "completed": models.AdCampaignStatus.COMPLETED,
            }
            
            campaign = models.AdCampaignCreation(
                store_id=store.id,
                ad_account_id=ad_account.id,
                campaign_name=cdata["name"],
                campaign_template=cdata["template"],
                platform=cdata["platform"],
                objective=cdata["objective"],
                budget_daily=Decimal(str(cdata["budget_daily"])),
                budget_total=Decimal(str(cdata["budget_daily"] * 30)),
                start_date=start_date,
                end_date=end_date,
                headline=cdata["headline"],
                description=cdata["description"],
                call_to_action="Learn More",
                location_radius=25.0,
                age_min=18,
                age_max=55,
                status=status_map.get(cdata["status"], models.AdCampaignStatus.DRAFT),
                created_by=admin.id if admin else None,
                approved_by=admin.id if cdata["status"] in ["active", "completed"] else None,
                approved_at=datetime.utcnow() - timedelta(days=20) if cdata["status"] in ["active", "completed"] else None,
                external_campaign_id=f"EXT_{cdata['platform'].upper()}_{random.randint(100000, 999999)}" if cdata["status"] == "active" else None
            )
            
            db.add(campaign)
            campaigns_created.append(campaign)
        
        db.commit()
        print(f"✓ Created/found {len(campaigns_created)} campaigns")
        
        # Refresh campaigns to get IDs
        campaigns_created = db.query(models.AdCampaignCreation).filter(
            models.AdCampaignCreation.store_id == store.id
        ).all()
        
        # Create Analytics Data
        print("\n--- Creating Campaign Analytics (30 days) ---")
        
        analytics_count = 0
        for campaign in campaigns_created:
            if campaign.status in [models.AdCampaignStatus.DRAFT, models.AdCampaignStatus.REJECTED]:
                continue
            
            # Generate 30 days of analytics
            for days_ago in range(30, -1, -1):
                date = (datetime.utcnow() - timedelta(days=days_ago)).date()
                
                # Skip if before campaign start
                if campaign.start_date and date < campaign.start_date.date():
                    continue
                
                # Skip if after campaign end
                if campaign.end_date and date > campaign.end_date.date():
                    continue
                
                # Check if exists
                existing = db.query(models.AdCampaignAnalytics).filter(
                    models.AdCampaignAnalytics.campaign_id == campaign.id,
                    models.AdCampaignAnalytics.date == date
                ).first()
                
                if existing:
                    continue
                
                # Generate realistic metrics
                daily_budget = float(campaign.budget_daily or 1500)
                spend = daily_budget * random.uniform(0.85, 1.0)
                
                # Platform-specific metrics
                if campaign.platform == "meta":
                    impressions = int(spend * random.uniform(800, 1200))
                    ctr = random.uniform(0.8, 2.5)
                else:  # google
                    impressions = int(spend * random.uniform(400, 800))
                    ctr = random.uniform(2.0, 5.0)
                
                clicks = int(impressions * ctr / 100)
                leads = int(clicks * random.uniform(0.05, 0.15))
                store_visits = int(clicks * random.uniform(0.02, 0.08))
                sales = int(leads * random.uniform(0.1, 0.3))
                revenue = sales * random.uniform(15000, 45000)
                
                analytics = models.AdCampaignAnalytics(
                    campaign_id=campaign.id,
                    date=date,
                    spend=Decimal(str(round(spend, 2))),
                    impressions=impressions,
                    clicks=clicks,
                    ctr=Decimal(str(round(ctr, 2))),
                    cpc=Decimal(str(round(spend / clicks if clicks > 0 else 0, 2))),
                    leads=leads,
                    store_visits=store_visits,
                    sales_attributed=sales,
                    revenue_attributed=Decimal(str(round(revenue, 2)))
                )
                
                db.add(analytics)
                analytics_count += 1
        
        db.commit()
        print(f"✓ Created {analytics_count} analytics records")
        
        # Create Audiences
        print("\n--- Creating Custom Audiences ---")
        
        audience_data = [
            {"name": "High Value Customers", "type": "high_value", "platform": "meta"},
            {"name": "Past 30 Day Buyers", "type": "past_buyers", "platform": "meta"},
            {"name": "Warranty Expiring Soon", "type": "warranty_expiring", "platform": "google"},
            {"name": "Mobile Phone Buyers", "type": "category_buyers", "platform": "meta"},
        ]
        
        customers = db.query(models.Customer).filter(
            models.Customer.store_id == store.id
        ).all()
        
        for aud_data in audience_data:
            existing = db.query(models.Audience).filter(
                models.Audience.name == aud_data["name"],
                models.Audience.store_id == store.id
            ).first()
            
            if existing:
                continue
            
            ad_account = meta_conn if aud_data["platform"] == "meta" else google_conn
            
            # Select random subset of customers
            selected_customers = random.sample(customers, min(len(customers), random.randint(5, 15)))
            customer_ids = [c.id for c in selected_customers]
            
            audience = models.Audience(
                store_id=store.id,
                ad_account_id=ad_account.id,
                name=aud_data["name"],
                audience_type=aud_data["type"],
                platform=aud_data["platform"],
                source_criteria={"segment": aud_data["type"]},
                customer_ids=customer_ids,
                size=len(customer_ids),
                created_by=admin.id if admin else None,
                last_synced_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            
            db.add(audience)
        
        db.commit()
        print(f"✓ Created audiences")
        
        # Create Marketing Campaigns (legacy model)
        print("\n--- Creating Marketing Campaigns ---")
        
        legacy_campaigns = [
            {"name": "Welcome Email Series", "type": "email", "trigger": "new_customer", "status": "active"},
            {"name": "Birthday Wishes", "type": "sms", "trigger": "birthday", "status": "active"},
            {"name": "Warranty Reminder", "type": "whatsapp", "trigger": "warranty_expiry", "status": "active"},
            {"name": "Re-engagement Campaign", "type": "email", "trigger": "inactive_customer", "status": "paused"},
            {"name": "Festival Promotion", "type": "sms", "trigger": "manual", "status": "completed"},
        ]
        
        for camp_data in legacy_campaigns:
            existing = db.query(models.Campaign).filter(
                models.Campaign.name == camp_data["name"],
                models.Campaign.store_id == store.id
            ).first()
            
            if existing:
                continue
            
            campaign = models.Campaign(
                store_id=store.id,
                name=camp_data["name"],
                description=f"Automated {camp_data['type']} campaign",
                campaign_type=camp_data["type"],
                trigger_type=camp_data["trigger"],
                status=camp_data["status"],
                total_sent=random.randint(100, 1000),
                total_opened=random.randint(50, 500),
                total_clicked=random.randint(20, 200),
                total_converted=random.randint(5, 50),
                created_by=admin.id if admin else None
            )
            
            db.add(campaign)
        
        db.commit()
        print("✓ Created marketing campaigns")
        
        print("\n" + "=" * 60)
        print("✓ MARKETING DATA SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  - Ad Account Connections: {len(connections)}")
        print(f"  - Ad Campaigns: {len(campaigns_created)}")
        print(f"  - Analytics Records: {analytics_count}")
        print(f"  - Custom Audiences: {len(audience_data)}")
        print(f"  - Marketing Campaigns: {len(legacy_campaigns)}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_marketing_data()
