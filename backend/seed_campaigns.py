"""
Seed Marketing Campaigns
"""
from app.db.database import SessionLocal
from app.db import models
from datetime import datetime, timedelta
import random
import sys

def seed_campaigns():
    """Add sample marketing campaigns to the database"""
    db = SessionLocal()
    
    try:
        sys.stdout.buffer.write(b"=" * 70 + b"\n")
        sys.stdout.buffer.write(b"Adding Marketing Campaigns...\n")
        sys.stdout.buffer.write(b"=" * 70 + b"\n")
        sys.stdout.flush()
        
        # Get the store
        store = db.query(models.Store).first()
        if not store:
            sys.stdout.buffer.write(b"ERROR: No store found. Please run init_db.py first!\n")
            sys.stdout.flush()
            return
        
        # Get marketing user or use first admin
        marketing_user = db.query(models.User).filter(
            models.User.role.in_([models.UserRole.MARKETING, models.UserRole.SUPER_ADMIN])
        ).first()
        
        if not marketing_user:
            marketing_user = db.query(models.User).first()
        
        campaigns_data = [
            {
                'name': 'Diwali Mega Sale 2024',
                'description': 'Special Diwali offers with up to 50% discount',
                'campaign_type': models.CampaignType.WHATSAPP,
                'trigger_type': models.CampaignTrigger.FESTIVAL,
                'message_template': "🪔 Happy Diwali {customer_name}! ✨\n\nCelebrate with {discount}% OFF on all products!\nUse code: {code}\n\nOffer valid till {end_date}\n\n🎊 Shop Now!",
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'DIWALI50',
                'discount_percentage': 50.0,
                'start_date': datetime.now() - timedelta(days=5),
                'end_date': datetime.now() + timedelta(days=10),
                'send_time': '10:00',
                'total_sent': random.randint(150, 200),
                'total_opened': random.randint(100, 150),
                'total_clicked': random.randint(50, 80),
                'total_converted': random.randint(20, 40)
            },
            {
                'name': 'Birthday Special Wishes',
                'description': 'Automated birthday wishes with special discount',
                'campaign_type': models.CampaignType.SMS,
                'trigger_type': models.CampaignTrigger.BIRTHDAY,
                'message_template': "🎉 Happy Birthday {customer_name}! 🎂\n\nWe're celebrating YOU today! Get {discount}% OFF on your next purchase.\nUse code: {code}\n\nValid for 7 days. Visit us now! 🎁",
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'BDAY20',
                'discount_percentage': 20.0,
                'days_before_trigger': 0,
                'send_time': '09:00',
                'total_sent': random.randint(30, 50),
                'total_opened': random.randint(25, 45),
                'total_clicked': random.randint(15, 30),
                'total_converted': random.randint(8, 15)
            },
            {
                'name': 'Warranty Expiry Alert',
                'description': 'Remind customers about expiring warranties',
                'campaign_type': models.CampaignType.WHATSAPP,
                'trigger_type': models.CampaignTrigger.WARRANTY_EXPIRY,
                'message_template': "⚠️ Important: Warranty Expiring Soon!\n\nDear {customer_name},\n\nYour product warranty expires in {days} days. Get it serviced or upgrade now!\n\nCall: {store_phone}\n\n🔧 We're here to help!",
                'status': models.CampaignStatus.ACTIVE,
                'days_before_trigger': 30,
                'send_time': '11:00',
                'total_sent': random.randint(20, 40),
                'total_opened': random.randint(15, 35),
                'total_clicked': random.randint(10, 25),
                'total_converted': random.randint(5, 12)
            },
            {
                'name': 'Win Back Campaign',
                'description': 'Re-engage customers who haven\'t purchased in 30 days',
                'campaign_type': models.CampaignType.EMAIL,
                'trigger_type': models.CampaignTrigger.NO_PURCHASE_30_DAYS,
                'message_template': "💜 We Miss You!\n\nHi {customer_name},\n\nIt's been a while! Come back and get {discount}% OFF your next purchase.\n\nCode: {code}\nValid for 7 days!\n\n🛍️ See you soon!",
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'COMEBACK15',
                'discount_percentage': 15.0,
                'send_time': '14:00',
                'total_sent': random.randint(50, 80),
                'total_opened': random.randint(30, 60),
                'total_clicked': random.randint(15, 35),
                'total_converted': random.randint(8, 18)
            },
            {
                'name': 'Cart Abandonment Recovery',
                'description': 'Recover abandoned carts with special offers',
                'campaign_type': models.CampaignType.WHATSAPP,
                'trigger_type': models.CampaignTrigger.CART_ABANDONED,
                'message_template': "🛒 You left something behind!\n\nHi {customer_name},\n\nComplete your purchase now and get {discount}% OFF!\n\nCode: {code}\nValid for 24 hours only!\n\n💳 Checkout now!",
                'status': models.CampaignStatus.DRAFT,
                'discount_code': 'CART10',
                'discount_percentage': 10.0,
                'send_time': '16:00',
                'total_sent': 0,
                'total_opened': 0,
                'total_clicked': 0,
                'total_converted': 0
            },
            {
                'name': 'Referral Program',
                'description': 'Encourage customers to refer friends',
                'campaign_type': models.CampaignType.SMS,
                'trigger_type': models.CampaignTrigger.MANUAL,
                'message_template': "👥 Refer & Earn!\n\nDear {customer_name},\n\nRefer a friend and both get {discount}% OFF!\n\nYour referral code: {code}\n\n💰 Start earning rewards today!",
                'status': models.CampaignStatus.SCHEDULED,
                'discount_code': 'REFER25',
                'discount_percentage': 25.0,
                'start_date': datetime.now() + timedelta(days=2),
                'end_date': datetime.now() + timedelta(days=30),
                'send_time': '10:30',
                'total_sent': 0,
                'total_opened': 0,
                'total_clicked': 0,
                'total_converted': 0
            },
            {
                'name': 'Weekend Flash Sale',
                'description': 'Weekend special offers',
                'campaign_type': models.CampaignType.NOTIFICATION,
                'trigger_type': models.CampaignTrigger.MANUAL,
                'message_template': "⚡ Weekend Flash Sale!\n\nHello {customer_name}!\n\nGet {discount}% OFF this weekend only!\nCode: {code}\n\n⏰ Hurry! Offer ends Sunday midnight!",
                'status': models.CampaignStatus.COMPLETED,
                'discount_code': 'WEEKEND30',
                'discount_percentage': 30.0,
                'start_date': datetime.now() - timedelta(days=10),
                'end_date': datetime.now() - timedelta(days=8),
                'send_time': '09:00',
                'total_sent': random.randint(200, 250),
                'total_opened': random.randint(150, 200),
                'total_clicked': random.randint(80, 120),
                'total_converted': random.randint(35, 55)
            },
            {
                'name': 'New Year Celebration',
                'description': 'New Year special offers',
                'campaign_type': models.CampaignType.EMAIL,
                'trigger_type': models.CampaignTrigger.FESTIVAL,
                'message_template': "🎆 Happy New Year {customer_name}! 🎊\n\nStart the year with {discount}% OFF!\nUse code: {code}\n\nValid till January 15th\n\n🎉 Shop Now!",
                'status': models.CampaignStatus.PAUSED,
                'discount_code': 'NEWYEAR40',
                'discount_percentage': 40.0,
                'send_time': '08:00',
                'total_sent': random.randint(100, 150),
                'total_opened': random.randint(70, 120),
                'total_clicked': random.randint(40, 70),
                'total_converted': random.randint(18, 35)
            }
        ]
        
        campaigns_created = 0
        for campaign_data in campaigns_data:
            campaign = models.Campaign(
                **campaign_data,
                store_id=store.id,
                created_by=marketing_user.id if marketing_user else 1
            )
            db.add(campaign)
            campaigns_created += 1
        
        db.commit()
        
        sys.stdout.buffer.write(f"\nSuccessfully created {campaigns_created} marketing campaigns!\n".encode('utf-8'))
        sys.stdout.buffer.write(b"\nCampaigns include:\n")
        sys.stdout.buffer.write(b"  - Festival campaigns (Diwali, New Year)\n")
        sys.stdout.buffer.write(b"  - Birthday automation\n")
        sys.stdout.buffer.write(b"  - Warranty expiry alerts\n")
        sys.stdout.buffer.write(b"  - Cart abandonment recovery\n")
        sys.stdout.buffer.write(b"  - Win-back campaigns\n")
        sys.stdout.buffer.write(b"  - Referral programs\n\n")
        sys.stdout.buffer.write(b"Go to Marketing page to see all campaigns!\n")
        sys.stdout.buffer.write(b"=" * 70 + b"\n")
        sys.stdout.flush()
        
    except Exception as e:
        sys.stdout.buffer.write(f"\nERROR: Failed to seed campaigns: {e}\n".encode('utf-8'))
        sys.stdout.flush()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_campaigns()

