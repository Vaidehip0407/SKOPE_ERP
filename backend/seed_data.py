"""
Seed Script - Add Sample Data to RMS Database
This script populates the database with realistic sample data for testing
"""
from app.db.database import SessionLocal
from app.db import models
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

def seed_database():
    """Add comprehensive sample data to the database"""
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("Starting Database Seeding Process...")
        print("=" * 70)
        
        # Check if data already exists
        existing_products = db.query(models.Product).count()
        if existing_products > 10:
            print(f"\nDatabase already has {existing_products} products.")
            print("Skipping - data already seeded.")
            return
        
        # Get the store
        store = db.query(models.Store).first()
        if not store:
            print("ERROR: No store found. Please run init_db.py first!")
            return
        
        print(f"\nSeeding data for store: {store.name}")
        
        # Sample Categories
        categories = {
            'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch', 'Camera'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Dress', 'Shirt'],
            'Food & Beverages': ['Snacks', 'Coffee', 'Tea', 'Juice', 'Cookies', 'Chocolate'],
            'Books': ['Fiction', 'Non-Fiction', 'Comics', 'Magazine', 'Textbook'],
            'Home & Kitchen': ['Cookware', 'Utensils', 'Containers', 'Appliances', 'Decor'],
            'Sports': ['Cricket Bat', 'Football', 'Yoga Mat', 'Dumbbells', 'Racket'],
            'Beauty': ['Perfume', 'Skincare', 'Makeup', 'Hair Care', 'Body Care']
        }
        
        brands = {
            'Electronics': ['Samsung', 'Apple', 'Sony', 'LG', 'OnePlus', 'Xiaomi'],
            'Clothing': ['Nike', 'Adidas', 'Puma', 'Levis', 'H&M', 'Zara'],
            'Food & Beverages': ['Nestle', 'Coca-Cola', 'Pepsi', 'Britannia', 'Parle'],
            'Books': ['Penguin', 'Harper Collins', 'Scholastic', 'Random House'],
            'Home & Kitchen': ['Prestige', 'Pigeon', 'Hawkins', 'Philips', 'Milton'],
            'Sports': ['Nike', 'Adidas', 'Puma', 'Reebok', 'Decathlon'],
            'Beauty': ['Lakme', 'Maybelline', 'Loreal', 'Nivea', 'Dove']
        }
        
        print("\n[1/5] Creating Products...")
        products_created = 0
        
        for category, items in categories.items():
            for item in items:
                brand = random.choice(brands.get(category, ['Generic']))
                base_price = random.randint(100, 5000)
                
                product = models.Product(
                    sku=f"SKU{random.randint(10000, 99999)}",
                    name=f"{brand} {item}",
                    description=f"High quality {item.lower()} from {brand}",
                    category=category,
                    brand=brand,
                    unit_price=base_price,
                    cost_price=base_price * 0.7,  # 30% margin
                    gst_rate=random.choice([5.0, 12.0, 18.0, 28.0]),
                    warranty_months=random.choice([0, 6, 12, 24]) if category == 'Electronics' else 0,
                    current_stock=random.randint(5, 100),
                    minimum_stock=random.randint(5, 15),
                    store_id=store.id,
                    is_active=True
                )
                db.add(product)
                products_created += 1
        
        db.flush()
        print(f"   [OK] Created {products_created} products")
        
        # Create Customers
        print("\n[2/5] Creating Customers...")
        customer_names = [
            'Rajesh Kumar', 'Priya Sharma', 'Amit Patel', 'Sneha Reddy', 'Vikram Singh',
            'Anjali Gupta', 'Rohit Verma', 'Pooja Desai', 'Arjun Nair', 'Divya Iyer',
            'Karan Mehta', 'Neha Joshi', 'Sanjay Rao', 'Kavita Pillai', 'Rahul Chopra',
            'Sunita Agarwal', 'Manoj Kumar', 'Ritu Shah', 'Ashok Menon', 'Geeta Bose'
        ]
        
        customers_created = 0
        for i, name in enumerate(customer_names):
            customer = models.Customer(
                name=name,
                email=f"{name.lower().replace(' ', '.')}@email.com",
                phone=f"+91{random.randint(7000000000, 9999999999)}",
                address=f"{random.randint(1, 999)} Main Street, City, State - {random.randint(100000, 999999)}",
                gst_number=f"GST{random.randint(100000000, 999999999)}" if random.random() > 0.7 else None,
                store_id=store.id,
                total_purchases=0
            )
            db.add(customer)
            customers_created += 1
        
        db.flush()
        print(f"   [OK] Created {customers_created} customers")
        
        # Create Sales
        print("\n[3/5] Creating Sales Transactions...")
        products = db.query(models.Product).all()
        customers = db.query(models.Customer).all()
        
        sales_created = 0
        for day_offset in range(30):  # Last 30 days
            num_sales = random.randint(3, 10)  # 3-10 sales per day
            
            for _ in range(num_sales):
                sale_date = datetime.now() - timedelta(days=day_offset, hours=random.randint(0, 23))
                customer = random.choice(customers) if random.random() > 0.3 else None
                
                # Select 1-5 random products
                sale_products = random.sample(products, random.randint(1, 5))
                
                subtotal = 0
                gst_amount = 0
                sale_items = []
                
                for product in sale_products:
                    quantity = random.randint(1, 3)
                    item_total = product.unit_price * quantity
                    item_gst = (item_total * product.gst_rate) / 100
                    
                    subtotal += item_total
                    gst_amount += item_gst
                    
                    sale_items.append({
                        'product': product,
                        'quantity': quantity,
                        'unit_price': product.unit_price,
                        'gst_rate': product.gst_rate,
                        'gst_amount': item_gst,
                        'total_price': item_total + item_gst
                    })
                
                discount = random.choice([0, 50, 100, 200]) if random.random() > 0.7 else 0
                total_amount = subtotal + gst_amount - discount
                
                sale = models.Sale(
                    invoice_number=f"INV{store.id}{sale_date.strftime('%Y%m%d')}{random.randint(1000, 9999)}",
                    customer_id=customer.id if customer else None,
                    store_id=store.id,
                    subtotal=subtotal,
                    gst_amount=gst_amount,
                    discount=discount,
                    total_amount=total_amount,
                    payment_mode=random.choice([
                        models.PaymentMode.CASH,
                        models.PaymentMode.CARD,
                        models.PaymentMode.UPI,
                        models.PaymentMode.QR_CODE
                    ]),
                    payment_status='completed',
                    sale_date=sale_date
                )
                db.add(sale)
                db.flush()
                
                # Add sale items
                for item_data in sale_items:
                    sale_item = models.SaleItem(
                        sale_id=sale.id,
                        product_id=item_data['product'].id,
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        gst_rate=item_data['gst_rate'],
                        gst_amount=item_data['gst_amount'],
                        total_price=item_data['total_price'],
                        warranty_expires_at=sale_date + timedelta(days=item_data['product'].warranty_months * 30) if item_data['product'].warranty_months > 0 else None
                    )
                    db.add(sale_item)
                
                # Update customer total
                if customer:
                    customer.total_purchases += total_amount
                
                sales_created += 1
        
        print(f"   [OK] Created {sales_created} sales transactions")
        
        # Create Expenses
        print("\n[4/5] Creating Expenses...")
        expense_categories = [
            ('rent', 'Monthly shop rent', 15000, 25000),
            ('utilities', 'Electricity bill', 2000, 5000),
            ('utilities', 'Water bill', 500, 1500),
            ('petty_cash', 'Office supplies', 500, 2000),
            ('vendor_payout', 'Stock purchase', 10000, 50000),
            ('salary', 'Staff salary', 15000, 30000),
            ('maintenance', 'Shop maintenance', 1000, 5000),
            ('other', 'Miscellaneous expenses', 500, 3000)
        ]
        
        expenses_created = 0
        for day_offset in range(30):
            num_expenses = random.randint(1, 3)
            
            for _ in range(num_expenses):
                expense_date = datetime.now() - timedelta(days=day_offset)
                category, desc, min_amt, max_amt = random.choice(expense_categories)
                
                expense = models.Expense(
                    store_id=store.id,
                    category=category,
                    description=desc,
                    amount=random.randint(min_amt, max_amt),
                    payment_mode=random.choice([
                        models.PaymentMode.CASH,
                        models.PaymentMode.CARD,
                        models.PaymentMode.UPI
                    ]),
                    vendor_name=f"Vendor {random.randint(1, 20)}" if random.random() > 0.5 else None,
                    receipt_number=f"RCP{random.randint(10000, 99999)}" if random.random() > 0.5 else None,
                    expense_date=expense_date
                )
                db.add(expense)
                expenses_created += 1
        
        print(f"   [OK] Created {expenses_created} expense records")
        
        # Create Marketing Campaigns
        print("\n[5/6] Creating Marketing Campaigns...")
        
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
        
        print(f"   [OK] Created {campaigns_created} marketing campaigns")
        
        # Commit all changes
        print("\n[6/6] Committing changes to database...")
        db.commit()
        
        print("\n" + "=" * 70)
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\nSummary:")
        print(f"  - Products:      {products_created}")
        print(f"  - Customers:     {customers_created}")
        print(f"  - Sales:         {sales_created}")
        print(f"  - Expenses:      {expenses_created}")
        print(f"  - Campaigns:     {campaigns_created}")
        print(f"\nYour RMS is now ready with sample data including Marketing Automation!")
        print("Refresh your browser to see all the data!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nERROR: Failed to seed database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

