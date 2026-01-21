"""
Complete Database Setup Script - SKOPE ERP
This script creates a fully populated database with realistic business data
"""
from app.db.database import engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random
import sys

def setup_complete_database(force_reset=False):
    """Complete database initialization with comprehensive realistic data"""
    
    # Create all tables
    print("\n" + "="*80)
    print(" SKOPE ERP - Complete Database Setup".center(80))
    print("="*80)
    
    models.Base.metadata.create_all(bind=engine)
    print("\n[OK] Database tables created successfully")
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(models.User).count()
        if existing_users > 3:
            if not force_reset:
                print(f"\nWARNING: Database already populated ({existing_users} users found)")
                print("Run with --reset flag to recreate: python setup_complete_database.py --reset")
                print("Setup cancelled")
                return
            # Drop and recreate tables
            print(f"\nResetting database (had {existing_users} users)...")
            models.Base.metadata.drop_all(bind=engine)
            models.Base.metadata.create_all(bind=engine)
            print("[OK] Database reset complete")
        
        # ============ STEP 1: Create Stores ============
        print("\n[Step 1/10] Creating Stores...")
        stores_data = [
            {
                'name': 'SKPOE Delhi Store',
                'address': '123 Connaught Place, New Delhi, Delhi - 110001',
                'phone': '+91-11-4567-8900',
                'email': 'delhi@skpoe.com',
                'gst_number': 'GST07AAACS1234F1Z5'
            },
            {
                'name': 'SKPOE Mumbai Store',
                'address': '456 Marine Drive, Mumbai, Maharashtra - 400002',
                'phone': '+91-22-6789-0123',
                'email': 'mumbai@skpoe.com',
                'gst_number': 'GST27AAACS5678G2Z6'
            },
            {
                'name': 'SKPOE Bangalore Store',
                'address': '789 MG Road, Bangalore, Karnataka - 560001',
                'phone': '+91-80-7890-1234',
                'email': 'bangalore@skpoe.com',
                'gst_number': 'GST29AAACS9012H3Z7'
            }
        ]
        
        stores = []
        for store_data in stores_data:
            store = models.Store(**store_data)
            db.add(store)
            stores.append(store)
        db.flush()
        print(f"   [OK] Created {len(stores)} stores")
        
        # ============ STEP 2: Create Users ============
        print("\n[Step 2/10] Creating Users...")
        users_data = [
            # Super Admin
            {
                'email': 'admin@skpoe.com',
                'username': 'admin',
                'full_name': 'System Administrator',
                'password': 'admin123',
                'role': models.UserRole.SUPER_ADMIN,
                'store_id': stores[0].id
            },
            # Store Managers
            {
                'email': 'rajesh.kumar@skpoe.com',
                'username': 'rajesh.kumar',
                'full_name': 'Rajesh Kumar',
                'password': 'manager123',
                'role': models.UserRole.STORE_MANAGER,
                'store_id': stores[0].id
            },
            {
                'email': 'priya.sharma@skpoe.com',
                'username': 'priya.sharma',
                'full_name': 'Priya Sharma',
                'password': 'manager123',
                'role': models.UserRole.STORE_MANAGER,
                'store_id': stores[1].id
            },
            {
                'email': 'amit.patel@skpoe.com',
                'username': 'amit.patel',
                'full_name': 'Amit Patel',
                'password': 'manager123',
                'role': models.UserRole.STORE_MANAGER,
                'store_id': stores[2].id
            },
            # Marketing Users
            {
                'email': 'marketing@skpoe.com',
                'username': 'marketing',
                'full_name': 'Marketing Team',
                'password': 'marketing123',
                'role': models.UserRole.MARKETING,
                'store_id': stores[0].id
            },
            # Sales Staff
            {
                'email': 'vikram.singh@skpoe.com',
                'username': 'vikram.singh',
                'full_name': 'Vikram Singh',
                'password': 'sales123',
                'role': models.UserRole.SALES_STAFF,
                'store_id': stores[0].id
            },
            {
                'email': 'anjali.gupta@skpoe.com',
                'username': 'anjali.gupta',
                'full_name': 'Anjali Gupta',
                'password': 'sales123',
                'role': models.UserRole.SALES_STAFF,
                'store_id': stores[1].id
            },
            {
                'email': 'rohit.verma@skpoe.com',
                'username': 'rohit.verma',
                'full_name': 'Rohit Verma',
                'password': 'sales123',
                'role': models.UserRole.SALES_STAFF,
                'store_id': stores[2].id
            },
            # Accounts
            {
                'email': 'accounts@skpoe.com',
                'username': 'accounts',
                'full_name': 'Accounts Department',
                'password': 'accounts123',
                'role': models.UserRole.ACCOUNTS,
                'store_id': stores[0].id
            }
        ]
        
        users = []
        for user_data in users_data:
            password = user_data.pop('password')
            user = models.User(
                **user_data,
                hashed_password=get_password_hash(password),
                is_active=True
            )
            db.add(user)
            users.append(user)
        db.flush()
        print(f"   [OK] Created {len(users)} users")
        
        # ============ STEP 3: Create Products ============
        print("\n[Step 3/10] Creating Products...")
        
        products_data = [
            # Electronics
            ('Electronics', 'Samsung', 'Galaxy S24 Ultra', 'Premium smartphone with 200MP camera', 119999, 18.0, 12),
            ('Electronics', 'Apple', 'iPhone 15 Pro Max', 'Latest iPhone with A17 Pro chip', 159999, 18.0, 12),
            ('Electronics', 'Sony', 'WH-1000XM5 Headphones', 'Premium noise cancelling headphones', 29990, 18.0, 12),
            ('Electronics', 'OnePlus', '12 Pro', 'Flagship smartphone with Snapdragon 8 Gen 3', 64999, 18.0, 12),
            ('Electronics', 'Dell', 'XPS 15 Laptop', '15.6" 4K OLED, i9 processor, 32GB RAM', 189999, 18.0, 24),
            ('Electronics', 'LG', '65" OLED TV', '4K OLED Smart TV with AI ThinQ', 149999, 18.0, 24),
            ('Electronics', 'Canon', 'EOS R6 Camera', 'Full-frame mirrorless camera', 219999, 18.0, 24),
            ('Electronics', 'Bose', 'SoundLink Revolve+', 'Portable Bluetooth speaker', 24999, 18.0, 12),
            ('Electronics', 'Apple', 'iPad Pro 12.9"', 'M2 chip, 256GB storage', 109999, 18.0, 12),
            ('Electronics', 'Samsung', 'Galaxy Watch 6', 'Premium smartwatch with health tracking', 34999, 18.0, 12),
            
            # Clothing & Fashion
            ('Clothing', 'Nike', 'Air Jordan 1 Retro', 'Classic basketball shoes', 12995, 12.0, 0),
            ('Clothing', 'Adidas', 'Ultraboost 22', 'Premium running shoes', 16999, 12.0, 0),
            ('Clothing', 'Levis', '501 Original Jeans', 'Classic fit denim jeans', 3999, 12.0, 0),
            ('Clothing', 'Puma', 'Running T-Shirt', 'Dry-fit sports t-shirt', 1499, 12.0, 0),
            ('Clothing', 'Zara', 'Formal Blazer', 'Slim fit formal blazer', 5999, 12.0, 0),
            ('Clothing', 'H&M', 'Casual Shirt', 'Cotton casual shirt', 1999, 12.0, 0),
            ('Clothing', 'Allen Solly', 'Formal Trousers', 'Regular fit formal trousers', 2499, 12.0, 0),
            ('Clothing', 'Van Heusen', 'Business Shirt', 'Wrinkle-free formal shirt', 2299, 12.0, 0),
            
            # Home & Kitchen
            ('Home & Kitchen', 'Prestige', 'Induction Cooktop', '2000W induction cooktop', 3499, 18.0, 12),
            ('Home & Kitchen', 'Philips', 'Air Fryer', '4.1L digital air fryer', 8999, 18.0, 12),
            ('Home & Kitchen', 'Hawkins', 'Pressure Cooker', '5L stainless steel cooker', 2499, 12.0, 24),
            ('Home & Kitchen', 'Milton', 'Water Bottle Set', 'Set of 4 insulated bottles', 1299, 12.0, 6),
            ('Home & Kitchen', 'Pigeon', 'Mixer Grinder', '750W with 3 jars', 2999, 18.0, 12),
            
            # Sports & Fitness
            ('Sports', 'Nike', 'Gym Bag', 'Large sports duffel bag', 2499, 18.0, 0),
            ('Sports', 'Adidas', 'Cricket Bat', 'English willow cricket bat', 12999, 18.0, 6),
            ('Sports', 'Decathlon', 'Yoga Mat', 'Anti-slip exercise mat', 699, 12.0, 0),
            ('Sports', 'Reebok', 'Dumbbells Set', '2-20kg adjustable dumbbells', 8999, 18.0, 12),
            ('Sports', 'Yonex', 'Badminton Racket', 'Professional carbon fiber racket', 4999, 18.0, 6),
            
            # Books & Stationery
            ('Books', 'Penguin', 'The Alchemist', 'Paulo Coelho bestseller', 399, 5.0, 0),
            ('Books', 'Harper Collins', 'Rich Dad Poor Dad', 'Personal finance guide', 449, 5.0, 0),
            ('Books', 'Scholastic', 'Harry Potter Set', 'Complete 7-book collection', 3999, 5.0, 0),
            ('Stationery', 'Parker', 'Fountain Pen', 'Premium gold-plated pen', 1999, 18.0, 24),
            ('Stationery', 'Moleskine', 'Notebook', 'Classic ruled notebook', 899, 12.0, 0),
            
            # Beauty & Personal Care
            ('Beauty', 'Lakme', 'Lipstick Set', 'Set of 5 matte lipsticks', 1499, 18.0, 0),
            ('Beauty', 'Loreal', 'Hair Color', 'Ammonia-free hair color', 599, 18.0, 0),
            ('Beauty', 'Nivea', 'Body Lotion', '400ml moisturizing lotion', 399, 18.0, 0),
            ('Beauty', 'Dove', 'Soap Pack', 'Pack of 4 moisturizing soaps', 299, 18.0, 0),
            ('Beauty', 'Maybelline', 'Mascara', 'Volume express mascara', 699, 18.0, 0),
            
            # Food & Beverages
            ('Food', 'Nestle', 'Coffee Pack', '200g instant coffee', 499, 5.0, 0),
            ('Food', 'Britannia', 'Cookies Assorted', 'Pack of 6 assorted cookies', 299, 12.0, 0),
            ('Food', 'Parle', 'Biscuits Family Pack', '1kg family pack', 199, 12.0, 0),
            ('Beverages', 'Coca-Cola', '2L Bottle', 'Carbonated soft drink', 90, 12.0, 0),
            ('Beverages', 'Pepsi', 'Can Pack', 'Pack of 6 cans', 240, 12.0, 0),
        ]
        
        products = []
        for category, brand, name, description, price, gst, warranty in products_data:
            for store in stores:
                product = models.Product(
                    sku=f"SKU{store.id}{random.randint(10000, 99999)}",
                    name=f"{brand} {name}",
                    description=description,
                    category=category,
                    brand=brand,
                    unit_price=price,
                    cost_price=price * 0.65,  # 35% margin
                    gst_rate=gst,
                    warranty_months=warranty,
                    current_stock=random.randint(10, 100),
                    minimum_stock=random.randint(5, 15),
                    store_id=store.id,
                    is_active=True
                )
                db.add(product)
                products.append(product)
        db.flush()
        print(f"   [OK] Created {len(products)} products across all stores")
        
        # ============ STEP 4: Create Customers ============
        print("\n[Step 4/10] Creating Customers...")
        
        customer_names = [
            ('Aditya Sharma', 'aditya.sharma@gmail.com', '+91-9876543210'),
            ('Bharati Reddy', 'bharati.reddy@gmail.com', '+91-9876543211'),
            ('Chetan Patel', 'chetan.patel@yahoo.com', '+91-9876543212'),
            ('Deepa Iyer', 'deepa.iyer@gmail.com', '+91-9876543213'),
            ('Esha Mehta', 'esha.mehta@outlook.com', '+91-9876543214'),
            ('Faisal Khan', 'faisal.khan@gmail.com', '+91-9876543215'),
            ('Geeta Nair', 'geeta.nair@gmail.com', '+91-9876543216'),
            ('Harsh Agarwal', 'harsh.agarwal@gmail.com', '+91-9876543217'),
            ('Ishita Joshi', 'ishita.joshi@gmail.com', '+91-9876543218'),
            ('Jai Malhotra', 'jai.malhotra@gmail.com', '+91-9876543219'),
            ('Kavya Pillai', 'kavya.pillai@gmail.com', '+91-9876543220'),
            ('Lokesh Rao', 'lokesh.rao@gmail.com', '+91-9876543221'),
            ('Meera Desai', 'meera.desai@gmail.com', '+91-9876543222'),
            ('Nikhil Verma', 'nikhil.verma@gmail.com', '+91-9876543223'),
            ('Ojaswi Singh', 'ojaswi.singh@gmail.com', '+91-9876543224'),
            ('Pranav Chopra', 'pranav.chopra@gmail.com', '+91-9876543225'),
            ('Qureshi Ahmed', 'qureshi.ahmed@gmail.com', '+91-9876543226'),
            ('Riya Gupta', 'riya.gupta@gmail.com', '+91-9876543227'),
            ('Sanjay Menon', 'sanjay.menon@gmail.com', '+91-9876543228'),
            ('Tanvi Shah', 'tanvi.shah@gmail.com', '+91-9876543229'),
            ('Uday Bose', 'uday.bose@gmail.com', '+91-9876543230'),
            ('Varun Kumar', 'varun.kumar@gmail.com', '+91-9876543231'),
            ('Wendy D''Souza', 'wendy.dsouza@gmail.com', '+91-9876543232'),
            ('Xavier Fernandes', 'xavier.fernandes@gmail.com', '+91-9876543233'),
            ('Yash Kapoor', 'yash.kapoor@gmail.com', '+91-9876543234'),
            ('Zara Ali', 'zara.ali@gmail.com', '+91-9876543235'),
        ]
        
        customers = []
        for store in stores:
            for name, email, phone in customer_names:
                # Random DOB for birthday campaigns
                dob = datetime.now() - timedelta(days=random.randint(7300, 18250))  # 20-50 years old
                
                customer = models.Customer(
                    name=name,
                    email=email,
                    phone=phone,
                    address=f"{random.randint(1, 999)} {random.choice(['Main St', 'Park Ave', 'MG Road', 'Commercial St'])}, {store.name.split()[1]}",
                    gst_number=f"GST{random.randint(10, 99)}AAACS{random.randint(1000, 9999)}F1Z{random.randint(1, 9)}" if random.random() > 0.8 else None,
                    date_of_birth=dob,
                    store_id=store.id,
                    total_purchases=0,
                    loyalty_points=0
                )
                db.add(customer)
                customers.append(customer)
        db.flush()
        print(f"   [OK] Created {len(customers)} customers across all stores")
        
        # ============ STEP 5: Create Sales Transactions ============
        print("\n[Step 5/10] Creating Sales Transactions...")
        
        sales_count = 0
        for store in stores:
            store_products = [p for p in products if p.store_id == store.id]
            store_customers = [c for c in customers if c.store_id == store.id]
            store_users = [u for u in users if u.store_id == store.id and u.role == models.UserRole.SALES_STAFF]
            
            # Create 60 days of sales history
            for day_offset in range(60):
                num_sales = random.randint(5, 20)  # 5-20 sales per day
                
                for _ in range(num_sales):
                    sale_date = datetime.now() - timedelta(
                        days=day_offset,
                        hours=random.randint(10, 20),
                        minutes=random.randint(0, 59)
                    )
                    
                    # 70% sales have customer, 30% walk-ins
                    customer = random.choice(store_customers) if random.random() > 0.3 else None
                    created_by_user = random.choice(store_users) if store_users else users[0]
                    
                    # Select 1-5 products
                    sale_products = random.sample(store_products, random.randint(1, min(5, len(store_products))))
                    
                    subtotal = 0
                    gst_amount = 0
                    sale_items_data = []
                    
                    for product in sale_products:
                        quantity = random.randint(1, 3)
                        item_subtotal = product.unit_price * quantity
                        item_gst = (item_subtotal * product.gst_rate) / 100
                        item_total = item_subtotal + item_gst
                        
                        subtotal += item_subtotal
                        gst_amount += item_gst
                        
                        sale_items_data.append({
                            'product': product,
                            'quantity': quantity,
                            'unit_price': product.unit_price,
                            'gst_rate': product.gst_rate,
                            'gst_amount': item_gst,
                            'total_price': item_total
                        })
                    
                    # Random discount (30% chance)
                    discount = random.choice([0, 100, 200, 500, 1000]) if random.random() > 0.7 else 0
                    total_amount = subtotal + gst_amount - discount
                    
                    # Create sale
                    sale = models.Sale(
                        invoice_number=f"INV{store.id}{sale_date.strftime('%Y%m%d')}{random.randint(10000, 99999)}",
                        customer_id=customer.id if customer else None,
                        store_id=store.id,
                        subtotal=subtotal,
                        gst_amount=gst_amount,
                        discount=discount,
                        total_amount=total_amount,
                        payment_mode=random.choice(list(models.PaymentMode)),
                        payment_status='completed',
                        created_by=created_by_user.id,
                        sale_date=sale_date
                    )
                    db.add(sale)
                    db.flush()
                    
                    # Create sale items
                    for item_data in sale_items_data:
                        warranty_date = None
                        if item_data['product'].warranty_months > 0:
                            warranty_date = sale_date + timedelta(days=item_data['product'].warranty_months * 30)
                        
                        sale_item = models.SaleItem(
                            sale_id=sale.id,
                            product_id=item_data['product'].id,
                            quantity=item_data['quantity'],
                            unit_price=item_data['unit_price'],
                            gst_rate=item_data['gst_rate'],
                            gst_amount=item_data['gst_amount'],
                            total_price=item_data['total_price'],
                            warranty_expires_at=warranty_date
                        )
                        db.add(sale_item)
                    
                    # Update customer totals
                    if customer:
                        customer.total_purchases += total_amount
                        customer.loyalty_points += int(total_amount / 100)  # 1 point per ₹100
                    
                    sales_count += 1
        
        print(f"   [OK] Created {sales_count} sales transactions")
        
        # ============ STEP 6: Create Expenses ============
        print("\n[Step 6/10] Creating Expenses...")
        
        expense_templates = [
            ('rent', 'Monthly store rent payment', 50000, 100000),
            ('utilities', 'Electricity bill', 3000, 8000),
            ('utilities', 'Water and sewerage', 800, 2000),
            ('utilities', 'Internet and phone', 2000, 4000),
            ('salary', 'Staff salaries', 80000, 150000),
            ('vendor_payout', 'Stock purchase from vendor', 50000, 200000),
            ('maintenance', 'Store maintenance and repairs', 2000, 10000),
            ('marketing', 'Digital marketing expenses', 5000, 20000),
            ('petty_cash', 'Office supplies and stationery', 1000, 5000),
            ('transport', 'Delivery and logistics', 3000, 10000),
            ('insurance', 'Store insurance premium', 5000, 15000),
            ('other', 'Miscellaneous expenses', 500, 5000),
        ]
        
        expenses_count = 0
        for store in stores:
            for day_offset in range(60):
                # 2-4 expenses per day
                num_expenses = random.randint(2, 4)
                
                for _ in range(num_expenses):
                    expense_date = datetime.now() - timedelta(
                        days=day_offset,
                        hours=random.randint(9, 18)
                    )
                    
                    category, description, min_amt, max_amt = random.choice(expense_templates)
                    
                    expense = models.Expense(
                        store_id=store.id,
                        category=category,
                        description=description,
                        amount=random.randint(min_amt, max_amt),
                        payment_mode=random.choice(list(models.PaymentMode)),
                        vendor_name=f"{random.choice(['ABC', 'XYZ', 'Global', 'Prime', 'Super'])} {random.choice(['Traders', 'Suppliers', 'Enterprises', 'Services'])}" if random.random() > 0.3 else None,
                        receipt_number=f"RCP{random.randint(100000, 999999)}" if random.random() > 0.4 else None,
                        created_by=users[0].id,
                        expense_date=expense_date
                    )
                    db.add(expense)
                    expenses_count += 1
        
        print(f"   [OK] Created {expenses_count} expense records")
        
        # ============ STEP 7: Create Marketing Campaigns ============
        print("\n[Step 7/10] Creating Marketing Campaigns...")
        
        marketing_user = next((u for u in users if u.role == models.UserRole.MARKETING), users[0])
        
        campaigns_templates = [
            {
                'name': 'Diwali Mega Sale 2024',
                'description': 'Biggest Diwali sale with up to 60% off on all categories',
                'campaign_type': models.CampaignType.WHATSAPP,
                'trigger_type': models.CampaignTrigger.FESTIVAL,
                'message_template': '🪔 Happy Diwali {customer_name}! ✨\n\nCelebrate with FLAT {discount}% OFF on all products!\nUse code: {code}\n\nValid till {end_date}\n\n🎊 Shop at {store_name} now!',
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'DIWALI60',
                'discount_percentage': 60.0,
                'days_offset': -5
            },
            {
                'name': 'Birthday Special',
                'description': 'Automated birthday wishes with exclusive discount',
                'campaign_type': models.CampaignType.SMS,
                'trigger_type': models.CampaignTrigger.BIRTHDAY,
                'message_template': '🎉 Happy Birthday {customer_name}! 🎂\n\nEnjoy {discount}% OFF on your birthday!\nCode: {code}\n\nValid for 7 days at {store_name}! 🎁',
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'BDAY25',
                'discount_percentage': 25.0,
                'days_offset': 0
            },
            {
                'name': 'Weekend Flash Sale',
                'description': 'Special weekend offers every Friday to Sunday',
                'campaign_type': models.CampaignType.NOTIFICATION,
                'trigger_type': models.CampaignTrigger.MANUAL,
                'message_template': '⚡ Weekend Flash Sale!\n\nHi {customer_name}!\n\nGet {discount}% OFF this weekend only!\nCode: {code}\n\n⏰ Hurry! Limited time offer!',
                'status': models.CampaignStatus.COMPLETED,
                'discount_code': 'WEEKEND35',
                'discount_percentage': 35.0,
                'days_offset': -15
            },
            {
                'name': 'Warranty Expiry Reminder',
                'description': 'Alert customers about expiring warranties 30 days in advance',
                'campaign_type': models.CampaignType.WHATSAPP,
                'trigger_type': models.CampaignTrigger.WARRANTY_EXPIRY,
                'message_template': '⚠️ Warranty Expiring Soon!\n\nDear {customer_name},\n\nYour product warranty expires in {days} days.\n\n🔧 Get free service check-up at {store_name}\nCall: {store_phone}',
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': None,
                'discount_percentage': 0.0,
                'days_offset': 0
            },
            {
                'name': 'Win-Back Campaign',
                'description': 'Re-engage inactive customers who haven\'t purchased in 30+ days',
                'campaign_type': models.CampaignType.EMAIL,
                'trigger_type': models.CampaignTrigger.NO_PURCHASE_30_DAYS,
                'message_template': '💜 We Miss You {customer_name}!\n\nIt\'s been a while since we saw you.\n\nCome back and enjoy {discount}% OFF!\nCode: {code}\n\n🛍️ Valid for 7 days at {store_name}',
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'COMEBACK20',
                'discount_percentage': 20.0,
                'days_offset': 0
            },
            {
                'name': 'New Year Grand Sale',
                'description': 'New year special offers on all products',
                'campaign_type': models.CampaignType.WHATSAPP,
                'trigger_type': models.CampaignTrigger.FESTIVAL,
                'message_template': '🎆 Happy New Year {customer_name}! 🎊\n\nStart 2025 with {discount}% OFF!\nCode: {code}\n\nValid till Jan 15th\n\n🎉 Shop at {store_name}!',
                'status': models.CampaignStatus.SCHEDULED,
                'discount_code': 'NEWYEAR2025',
                'discount_percentage': 45.0,
                'days_offset': 10
            },
            {
                'name': 'Referral Program',
                'description': 'Refer friends and earn rewards for both',
                'campaign_type': models.CampaignType.SMS,
                'trigger_type': models.CampaignTrigger.MANUAL,
                'message_template': '👥 Refer & Earn!\n\nHi {customer_name},\n\nRefer friends and both get {discount}% OFF!\n\nYour code: {code}\n\n💰 Start earning at {store_name}!',
                'status': models.CampaignStatus.DRAFT,
                'discount_code': 'REFER30',
                'discount_percentage': 30.0,
                'days_offset': 20
            },
            {
                'name': 'Purchase Anniversary',
                'description': 'Celebrate customer purchase anniversary with special offers',
                'campaign_type': models.CampaignType.EMAIL,
                'trigger_type': models.CampaignTrigger.PURCHASE_ANNIVERSARY,
                'message_template': '🎊 It\'s been a year!\n\nDear {customer_name},\n\nThanks for being with us!\nEnjoy {discount}% OFF as anniversary gift!\n\nCode: {code}\n\n❤️ {store_name}',
                'status': models.CampaignStatus.ACTIVE,
                'discount_code': 'ANNIVERSARY15',
                'discount_percentage': 15.0,
                'days_offset': 0
            }
        ]
        
        campaigns_count = 0
        for store in stores:
            for template in campaigns_templates:
                days_offset = template.get('days_offset', 0)
                start_date = datetime.now() + timedelta(days=days_offset) if days_offset > 0 else datetime.now() - timedelta(days=abs(days_offset))
                end_date = start_date + timedelta(days=15)
                
                campaign = models.Campaign(
                    **{k: v for k, v in template.items() if k != 'days_offset'},
                    store_id=store.id,
                    start_date=start_date,
                    end_date=end_date,
                    send_time=f"{random.randint(9, 18)}:00",
                    total_sent=random.randint(100, 500) if template['status'] in [models.CampaignStatus.ACTIVE, models.CampaignStatus.COMPLETED] else 0,
                    total_opened=random.randint(70, 400) if template['status'] in [models.CampaignStatus.ACTIVE, models.CampaignStatus.COMPLETED] else 0,
                    total_clicked=random.randint(30, 200) if template['status'] in [models.CampaignStatus.ACTIVE, models.CampaignStatus.COMPLETED] else 0,
                    total_converted=random.randint(10, 100) if template['status'] in [models.CampaignStatus.ACTIVE, models.CampaignStatus.COMPLETED] else 0,
                    created_by=marketing_user.id
                )
                db.add(campaign)
                campaigns_count += 1
        
        db.flush()
        print(f"   [OK] Created {campaigns_count} marketing campaigns")
        
        # ============ STEP 8: Create Ad Account Connections ============
        print("\n[Step 8/10] Creating Ad Platform Connections...")
        
        ad_connections_count = 0
        for i, store in enumerate(stores):
            # Meta (Facebook/Instagram/WhatsApp) Connection
            meta_connection = models.AdAccountConnection(
                store_id=store.id,
                platform=models.AdPlatform.META,
                meta_ad_account_id=f"act_123456789{i}",
                meta_pixel_id=f"123456789012345{i}",
                meta_page_id=f"10987654321{i}",
                meta_business_id=f"98765432{i}",
                access_token="dummy_meta_access_token_" + str(i),
                refresh_token="dummy_meta_refresh_token_" + str(i),
                token_expires_at=datetime.now() + timedelta(days=60),
                is_active=True,
                is_verified=True,
                last_token_refresh=datetime.now() - timedelta(days=5),
                last_sync_at=datetime.now() - timedelta(hours=2),
                created_by=marketing_user.id
            )
            db.add(meta_connection)
            ad_connections_count += 1
            
            # Google Ads Connection
            google_connection = models.AdAccountConnection(
                store_id=store.id,
                platform=models.AdPlatform.GOOGLE,
                google_customer_id=f"123-456-789{i}",
                google_conversion_actions=["store_visit", "purchase", "lead_form"],
                google_ga4_property=f"G-12345678{i}",
                access_token="dummy_google_access_token_" + str(i),
                refresh_token="dummy_google_refresh_token_" + str(i),
                token_expires_at=datetime.now() + timedelta(days=60),
                is_active=True,
                is_verified=True,
                last_token_refresh=datetime.now() - timedelta(days=5),
                last_sync_at=datetime.now() - timedelta(hours=1),
                created_by=marketing_user.id
            )
            db.add(google_connection)
            ad_connections_count += 1
        
        db.flush()
        print(f"   [OK] Created {ad_connections_count} ad platform connections")
        
        # ============ STEP 9: Create Ad Campaigns ============
        print("\n[Step 9/10] Creating Ad Campaigns (Meta & Google)...")
        
        ad_campaigns_count = 0
        for store in stores:
            # Get connections for this store
            meta_conn = db.query(models.AdAccountConnection).filter(
                models.AdAccountConnection.store_id == store.id,
                models.AdAccountConnection.platform == models.AdPlatform.META
            ).first()
            
            google_conn = db.query(models.AdAccountConnection).filter(
                models.AdAccountConnection.store_id == store.id,
                models.AdAccountConnection.platform == models.AdPlatform.GOOGLE
            ).first()
            
            # Meta Ad Campaigns
            meta_campaigns = [
                {
                    'name': f'{store.name} - Store Visit Campaign',
                    'template': models.AdCampaignTemplate.STORE_VISIT,
                    'platform': models.AdPlatform.META,
                    'objective': 'STORE_VISITS',
                    'headline': 'Visit Our Store Today!',
                    'description': f'Special offers available at {store.name}. Get directions and visit us now!',
                    'budget_daily': 500.0,
                    'cta': 'Get Directions'
                },
                {
                    'name': f'{store.name} - WhatsApp Lead Campaign',
                    'template': models.AdCampaignTemplate.WHATSAPP_CLICK,
                    'platform': models.AdPlatform.META,
                    'objective': 'MESSAGES',
                    'headline': 'Chat with Us on WhatsApp!',
                    'description': 'Get instant assistance and exclusive deals via WhatsApp.',
                    'budget_daily': 300.0,
                    'cta': 'Send Message'
                },
                {
                    'name': f'{store.name} - Diwali Festival Offer',
                    'template': models.AdCampaignTemplate.OFFER_FESTIVAL,
                    'platform': models.AdPlatform.META,
                    'objective': 'CONVERSIONS',
                    'headline': '🪔 Diwali Mega Sale - Up to 60% OFF!',
                    'description': 'Celebrate Diwali with amazing discounts on all products!',
                    'budget_daily': 1000.0,
                    'cta': 'Shop Now'
                }
            ]
            
            # Google Ad Campaigns
            google_campaigns = [
                {
                    'name': f'{store.name} - Local Search Ads',
                    'template': models.AdCampaignTemplate.LOCAL_SEARCH_ADS,
                    'platform': models.AdPlatform.GOOGLE,
                    'objective': 'LOCAL_AWARENESS',
                    'headline': f'Best Deals at {store.name}',
                    'description': 'Visit our store for exclusive offers and premium products.',
                    'budget_daily': 700.0,
                    'cta': 'Visit Store'
                },
                {
                    'name': f'{store.name} - Performance Max',
                    'template': models.AdCampaignTemplate.PERFORMANCE_MAX,
                    'platform': models.AdPlatform.GOOGLE,
                    'objective': 'SALES',
                    'headline': 'Shop Premium Products',
                    'description': 'Discover our wide range of quality products at great prices.',
                    'budget_daily': 800.0,
                    'cta': 'Learn More'
                }
            ]
            
            # Create Meta campaigns
            for campaign_data in meta_campaigns:
                cta = campaign_data.get('cta', 'Learn More')
                campaign = models.AdCampaignCreation(
                    store_id=store.id,
                    ad_account_id=meta_conn.id,
                    campaign_name=campaign_data['name'],
                    campaign_template=campaign_data['template'],
                    platform=campaign_data['platform'],
                    status=random.choice([models.AdCampaignStatus.ACTIVE, models.AdCampaignStatus.ACTIVE, models.AdCampaignStatus.PAUSED]),
                    objective=campaign_data['objective'],
                    budget_daily=campaign_data['budget_daily'],
                    budget_total=campaign_data['budget_daily'] * 30,
                    start_date=datetime.now() - timedelta(days=random.randint(5, 30)),
                    end_date=datetime.now() + timedelta(days=random.randint(15, 60)),
                    headline=campaign_data['headline'],
                    description=campaign_data['description'],
                    call_to_action=cta,
                    target_audience={'age_range': '18-65', 'gender': 'all', 'interests': ['shopping', 'retail']},
                    location_radius=10.0,
                    age_min=18,
                    age_max=65,
                    gender='all',
                    interests=['shopping', 'electronics', 'fashion'],
                    store_name_dynamic=True,
                    location_dynamic=True,
                    offer_text=f'Up to {random.choice([30, 40, 50, 60])}% OFF',
                    external_campaign_id=f"meta_camp_{random.randint(100000, 999999)}",
                    created_by=marketing_user.id,
                    approved_by=users[0].id,
                    approved_at=datetime.now() - timedelta(days=random.randint(1, 10))
                )
                db.add(campaign)
                ad_campaigns_count += 1
            
            # Create Google campaigns
            for campaign_data in google_campaigns:
                cta = campaign_data.get('cta', 'Learn More')
                campaign = models.AdCampaignCreation(
                    store_id=store.id,
                    ad_account_id=google_conn.id,
                    campaign_name=campaign_data['name'],
                    campaign_template=campaign_data['template'],
                    platform=campaign_data['platform'],
                    status=random.choice([models.AdCampaignStatus.ACTIVE, models.AdCampaignStatus.ACTIVE, models.AdCampaignStatus.PAUSED]),
                    objective=campaign_data['objective'],
                    budget_daily=campaign_data['budget_daily'],
                    budget_total=campaign_data['budget_daily'] * 30,
                    start_date=datetime.now() - timedelta(days=random.randint(5, 30)),
                    end_date=datetime.now() + timedelta(days=random.randint(15, 60)),
                    headline=campaign_data['headline'],
                    description=campaign_data['description'],
                    call_to_action=cta,
                    target_audience={'location': 'local', 'radius': '10km'},
                    location_radius=10.0,
                    store_name_dynamic=True,
                    location_dynamic=True,
                    offer_text=f'{random.choice(["Best Prices", "Premium Quality", "Fast Delivery"])}',
                    external_campaign_id=f"google_camp_{random.randint(100000, 999999)}",
                    created_by=marketing_user.id,
                    approved_by=users[0].id,
                    approved_at=datetime.now() - timedelta(days=random.randint(1, 10))
                )
                db.add(campaign)
                ad_campaigns_count += 1
        
        db.flush()
        print(f"   [OK] Created {ad_campaigns_count} ad campaigns")
        
        # ============ STEP 10: Create Analytics Data ============
        print("\n[Step 10/10] Creating Analytics Data...")
        
        # Get all ad campaigns
        all_ad_campaigns = db.query(models.AdCampaignCreation).all()
        analytics_count = 0
        
        for campaign in all_ad_campaigns:
            if campaign.status == models.AdCampaignStatus.ACTIVE:
                # Create 30 days of analytics
                for day in range(30):
                    analytics_date = datetime.now() - timedelta(days=day)
                    
                    impressions = random.randint(1000, 10000)
                    clicks = random.randint(50, 500)
                    spend = campaign.budget_daily * random.uniform(0.8, 1.0)
                    leads = random.randint(5, 50)
                    store_visits = random.randint(10, 100)
                    sales = random.randint(2, 30)
                    revenue = sales * random.uniform(2000, 10000)
                    
                    ctr = (clicks / impressions) * 100 if impressions > 0 else 0
                    cpc = spend / clicks if clicks > 0 else 0
                    cpl = spend / leads if leads > 0 else 0
                    roas = revenue / spend if spend > 0 else 0
                    
                    analytics = models.AdCampaignAnalytics(
                        campaign_id=campaign.id,
                        date=analytics_date,
                        impressions=impressions,
                        clicks=clicks,
                        spend=spend,
                        reach=int(impressions * 0.7),
                        leads=leads,
                        store_visits=store_visits,
                        sales_attributed=sales,
                        revenue_attributed=revenue,
                        ctr=round(ctr, 2),
                        cpc=round(cpc, 2),
                        cpl=round(cpl, 2),
                        roas=round(roas, 2)
                    )
                    db.add(analytics)
                    analytics_count += 1
        
        print(f"   [OK] Created {analytics_count} analytics records")
        
        # ============ COMMIT ALL CHANGES ============
        print("\n[Finalizing] Committing all changes to database...")
        db.commit()
        
        # ============ SUCCESS SUMMARY ============
        print("\n" + "="*80)
        print(" DATABASE SETUP COMPLETED SUCCESSFULLY! ".center(80))
        print("="*80)
        
        print("\nDATA SUMMARY:")
        print(f"   • Stores:              {len(stores)}")
        print(f"   • Users:               {len(users)}")
        print(f"   • Products:            {len(products)}")
        print(f"   • Customers:           {len(customers)}")
        print(f"   • Sales Transactions:  {sales_count}")
        print(f"   • Expenses:            {expenses_count}")
        print(f"   • Marketing Campaigns: {campaigns_count}")
        print(f"   • Ad Connections:      {ad_connections_count}")
        print(f"   • Ad Campaigns:        {ad_campaigns_count}")
        print(f"   • Analytics Records:   {analytics_count}")
        
        print("\nDEFAULT LOGIN CREDENTIALS:")
        print("="*80)
        print("\n1. Super Admin (Full Access):")
        print("   Username: admin")
        print("   Password: admin123")
        
        print("\n2. Store Manager (Delhi):")
        print("   Username: rajesh.kumar")
        print("   Password: manager123")
        
        print("\n3. Marketing Team:")
        print("   Username: marketing")
        print("   Password: marketing123")
        
        print("\n4. Sales Staff:")
        print("   Username: vikram.singh")
        print("   Password: sales123")
        
        print("\n5. Accounts:")
        print("   Username: accounts")
        print("   Password: accounts123")
        
        print("\n" + "="*80)
        print(" YOUR SKOPE ERP IS NOW READY WITH COMPLETE DATA! ".center(80))
        print("="*80)
        print("\nNEXT STEPS:")
        print("   1. Start the backend server: cd backend && python -m uvicorn app.main:app --reload")
        print("   2. Start the frontend: cd frontend && npm run dev")
        print("   3. Open browser at: http://localhost:5173")
        print("   4. Login with any of the credentials above")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    force_reset = "--reset" in sys.argv or "--force" in sys.argv
    setup_complete_database(force_reset=force_reset)

