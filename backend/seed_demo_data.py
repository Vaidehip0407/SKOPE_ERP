"""
Comprehensive Seed Script - 5000+ Records with ALL Fields
Includes: Products, Batches, Customers, Users/Sellers, Sales, Expenses, Campaigns
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import random
import string
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models

# Staff/Sellers
STAFF = [
    ("Rohit Mehta", "rohit@skope.com", models.UserRole.SALES_STAFF),
    ("Priya Sharma", "priya@skope.com", models.UserRole.SALES_STAFF),
    ("Amit Patel", "amit@skope.com", models.UserRole.SALES_STAFF),
    ("Sneha Gupta", "sneha@skope.com", models.UserRole.SALES_STAFF),
    ("Vikram Singh", "vikram@skope.com", models.UserRole.SALES_STAFF),
    ("Anita Reddy", "anita@skope.com", models.UserRole.STORE_MANAGER),
    ("Rajesh Kumar", "rajesh@skope.com", models.UserRole.ACCOUNTS),
    ("Neha Joshi", "neha@skope.com", models.UserRole.MARKETING),
]

# Products with full details
PRODUCTS = [
    ("iPhone 15 Pro Max", "Electronics", "Apple", 134999, 149999, 12, "Premium flagship smartphone with A17 Pro chip"),
    ("iPhone 15 Pro", "Electronics", "Apple", 119999, 134999, 12, "Pro smartphone with titanium design"),
    ("iPhone 15", "Electronics", "Apple", 69999, 79999, 12, "Latest iPhone with Dynamic Island"),
    ("Samsung Galaxy S24 Ultra", "Electronics", "Samsung", 109999, 129999, 12, "Ultimate Galaxy experience"),
    ("Samsung Galaxy S24", "Electronics", "Samsung", 69999, 84999, 12, "Premium Android flagship"),
    ("MacBook Air M3", "Electronics", "Apple", 99999, 114999, 12, "Supercharged by M3 chip"),
    ("MacBook Pro 14", "Electronics", "Apple", 169999, 199999, 24, "Pro laptop for professionals"),
    ("iPad Pro 12.9", "Electronics", "Apple", 99999, 112999, 12, "Ultimate iPad experience"),
    ("iPad Air", "Electronics", "Apple", 59999, 69999, 12, "Powerful and versatile"),
    ("Apple Watch Series 9", "Electronics", "Apple", 41999, 49999, 12, "Advanced health features"),
    ("Apple Watch Ultra 2", "Electronics", "Apple", 79999, 89999, 24, "Adventure-ready smartwatch"),
    ("AirPods Pro 2", "Electronics", "Apple", 20999, 24999, 12, "Active noise cancellation"),
    ("AirPods Max", "Electronics", "Apple", 49999, 59999, 12, "High-fidelity audio"),
    ("Sony WH-1000XM5", "Electronics", "Sony", 24999, 29999, 24, "Industry-leading noise cancellation"),
    ("Sony WF-1000XM5", "Electronics", "Sony", 19999, 24999, 12, "Premium true wireless earbuds"),
    ("Dell XPS 15", "Electronics", "Dell", 129999, 149999, 24, "Premium Windows laptop"),
    ("Dell XPS 13", "Electronics", "Dell", 99999, 119999, 24, "Ultraportable powerhouse"),
    ("HP Spectre x360", "Electronics", "HP", 109999, 129999, 24, "Convertible laptop"),
    ("Samsung 65 OLED TV", "Electronics", "Samsung", 149999, 179999, 36, "Stunning OLED display"),
    ("Samsung 55 QLED TV", "Electronics", "Samsung", 79999, 99999, 36, "Quantum dot technology"),
    ("LG C3 OLED 55", "Electronics", "LG", 119999, 139999, 36, "Perfect blacks OLED"),
    ("Sony Bravia 55", "Electronics", "Sony", 89999, 109999, 36, "Cognitive processor XR"),
    ("Bose SoundLink Max", "Electronics", "Bose", 29999, 34999, 12, "Powerful portable speaker"),
    ("JBL Flip 6", "Electronics", "JBL", 9999, 12999, 12, "Waterproof Bluetooth speaker"),
    ("Canon EOS R6 II", "Electronics", "Canon", 199999, 229999, 24, "Full-frame mirrorless camera"),
    ("Sony A7 IV", "Electronics", "Sony", 219999, 249999, 24, "Professional mirrorless"),
    ("Nike Air Max 270", "Footwear", "Nike", 8999, 12999, 0, "Lifestyle sneakers"),
    ("Nike Air Jordan 1", "Footwear", "Nike", 12999, 16999, 0, "Iconic basketball shoes"),
    ("Nike Dunk Low", "Footwear", "Nike", 7999, 10999, 0, "Classic streetwear"),
    ("Adidas Ultraboost 23", "Footwear", "Adidas", 13999, 17999, 0, "Ultimate running comfort"),
    ("Adidas Stan Smith", "Footwear", "Adidas", 6999, 9999, 0, "Timeless tennis shoes"),
    ("Puma RS-X", "Footwear", "Puma", 6999, 9999, 0, "Retro running style"),
    ("Reebok Classic", "Footwear", "Reebok", 5999, 7999, 0, "Heritage sneakers"),
    ("New Balance 574", "Footwear", "New Balance", 7999, 10999, 0, "Classic comfort"),
    ("Levi's 501 Original", "Clothing", "Levi's", 3999, 5499, 0, "Iconic straight fit jeans"),
    ("Levi's 511 Slim", "Clothing", "Levi's", 3499, 4999, 0, "Modern slim fit"),
    ("Tommy Hilfiger Polo", "Clothing", "Tommy", 2999, 4499, 0, "Classic polo shirt"),
    ("Ralph Lauren Oxford", "Clothing", "Ralph Lauren", 5999, 7999, 0, "Premium oxford shirt"),
    ("Zara Blazer", "Clothing", "Zara", 4999, 6999, 0, "Contemporary blazer"),
    ("H&M Hoodie", "Clothing", "H&M", 1999, 2999, 0, "Casual comfort"),
    ("Uniqlo Airism Tee", "Clothing", "Uniqlo", 999, 1499, 0, "Breathable basics"),
    ("Allen Solly Formal", "Clothing", "Allen Solly", 2499, 3499, 0, "Office wear"),
    ("Peter England Shirt", "Clothing", "Peter England", 1499, 2299, 0, "Formal shirts"),
    ("Van Heusen Trousers", "Clothing", "Van Heusen", 1999, 2999, 0, "Formal trousers"),
    ("Basmati Rice 10kg", "Groceries", "India Gate", 899, 1199, 0, "Premium long grain rice"),
    ("Tata Salt 1kg", "Groceries", "Tata", 25, 32, 0, "Iodized salt"),
    ("Fortune Oil 5L", "Groceries", "Fortune", 699, 849, 0, "Refined sunflower oil"),
    ("Aashirvaad Atta 10kg", "Groceries", "Aashirvaad", 449, 549, 0, "Whole wheat flour"),
    ("Maggi Noodles Pack", "Groceries", "Nestle", 120, 150, 0, "Instant noodles 12 pack"),
    ("Tata Tea Gold 1kg", "Groceries", "Tata", 499, 599, 0, "Premium tea"),
    ("Nescafe Classic 200g", "Groceries", "Nestle", 449, 549, 0, "Instant coffee"),
    ("Amul Butter 500g", "Groceries", "Amul", 275, 320, 0, "Fresh butter"),
    ("Surf Excel 4kg", "Home Care", "HUL", 549, 649, 0, "Detergent powder"),
    ("Vim Dishwash 1.5L", "Home Care", "HUL", 199, 249, 0, "Dishwash liquid"),
    ("Harpic 1L", "Home Care", "Reckitt", 179, 219, 0, "Toilet cleaner"),
    ("Dettol 900ml", "Home Care", "Reckitt", 199, 249, 0, "Antiseptic liquid"),
    ("Lakme Face Cream", "Beauty", "Lakme", 399, 549, 0, "Daily moisturizer"),
    ("Dove Shampoo 650ml", "Beauty", "Dove", 399, 499, 0, "Nourishing shampoo"),
    ("Nivea Body Lotion", "Beauty", "Nivea", 299, 399, 0, "Deep moisture care"),
    ("Maybelline Lipstick", "Beauty", "Maybelline", 599, 799, 0, "Matte finish lipstick"),
    ("L'Oreal Face Wash", "Beauty", "L'Oreal", 349, 449, 0, "Deep clean face wash"),
    ("Godrej Office Chair", "Furniture", "Godrej", 8999, 12999, 12, "Ergonomic office chair"),
    ("Nilkamal Plastic Chair", "Furniture", "Nilkamal", 999, 1499, 6, "Durable plastic chair"),
    ("Urban Ladder Desk", "Furniture", "Urban Ladder", 12999, 17999, 12, "Work from home desk"),
    ("Pepperfry Bookshelf", "Furniture", "Pepperfry", 5999, 8999, 12, "Modern bookshelf"),
    ("Philips LED Bulb 9W", "Electricals", "Philips", 99, 149, 24, "Energy efficient LED"),
    ("Havells Fan", "Electricals", "Havells", 2499, 3299, 24, "Ceiling fan 1200mm"),
    ("Crompton Geyser 15L", "Electricals", "Crompton", 6999, 8999, 60, "Water heater"),
    ("Bajaj Iron", "Electricals", "Bajaj", 799, 1099, 24, "Dry iron press"),
    ("Prestige Cooker 5L", "Kitchen", "Prestige", 1999, 2699, 60, "Pressure cooker"),
    ("Butterfly Mixer Grinder", "Kitchen", "Butterfly", 2999, 3999, 24, "750W mixer grinder"),
    ("Philips Air Fryer", "Kitchen", "Philips", 7999, 9999, 24, "Healthy cooking"),
    ("Borosil Glass Set", "Kitchen", "Borosil", 599, 849, 0, "6 piece glass set"),
    ("Milton Water Bottle", "Kitchen", "Milton", 399, 549, 6, "1L stainless steel"),
]

CUSTOMERS = [
    ("Rahul Sharma", "rahul.sharma@email.com", "+919876543210", "A-101, Andheri West, Mumbai 400053"),
    ("Priya Patel", "priya.patel@email.com", "+919876543211", "B-202, Bandra East, Mumbai 400051"),
    ("Amit Kumar", "amit.kumar@email.com", "+919876543212", "C-303, Powai, Mumbai 400076"),
    ("Sneha Gupta", "sneha.gupta@email.com", "+919876543213", "D-404, Malad West, Mumbai 400064"),
    ("Vikram Singh", "vikram.singh@email.com", "+919876543214", "E-505, Goregaon East, Mumbai 400063"),
    ("Anita Reddy", "anita.reddy@email.com", "+919876543215", "F-606, Kandivali West, Mumbai 400067"),
    ("Rajesh Verma", "rajesh.verma@email.com", "+919876543216", "G-707, Borivali East, Mumbai 400066"),
    ("Pooja Iyer", "pooja.iyer@email.com", "+919876543217", "H-808, Thane West, Thane 400601"),
    ("Suresh Nair", "suresh.nair@email.com", "+919876543218", "I-909, Vashi, Navi Mumbai 400703"),
    ("Deepa Menon", "deepa.menon@email.com", "+919876543219", "J-1010, Airoli, Navi Mumbai 400708"),
    ("Karthik Rajan", "karthik.rajan@email.com", "+919876543220", "K-111, Nerul, Navi Mumbai 400706"),
    ("Lakshmi Rao", "lakshmi.rao@email.com", "+919876543221", "L-222, Panvel, Navi Mumbai 410206"),
    ("Arun Krishnan", "arun.krishnan@email.com", "+919876543222", "M-333, Kharghar, Navi Mumbai 410210"),
    ("Meera Joshi", "meera.joshi@email.com", "+919876543223", "N-444, Chembur, Mumbai 400071"),
    ("Sanjay Dubey", "sanjay.dubey@email.com", "+919876543224", "O-555, Ghatkopar East, Mumbai 400077"),
    ("Kavitha Pillai", "kavitha.pillai@email.com", "+919876543225", "P-666, Mulund West, Mumbai 400080"),
    ("Mohan Das", "mohan.das@email.com", "+919876543226", "Q-777, Vikhroli East, Mumbai 400083"),
    ("Swati Mishra", "swati.mishra@email.com", "+919876543227", "R-888, Kurla West, Mumbai 400070"),
    ("Prakash Hegde", "prakash.hegde@email.com", "+919876543228", "S-999, Sion, Mumbai 400022"),
    ("Divya Nambiar", "divya.nambiar@email.com", "+919876543229", "T-1000, Dadar East, Mumbai 400014"),
    ("Ajay Kulkarni", "ajay.kulkarni@email.com", "+919876543230", "U-1111, Worli, Mumbai 400018"),
    ("Rekha Bhat", "rekha.bhat@email.com", "+919876543231", "V-1212, Prabhadevi, Mumbai 400025"),
    ("Venkat Iyer", "venkat.iyer@email.com", "+919876543232", "W-1313, Lower Parel, Mumbai 400013"),
    ("Shweta Kapoor", "shweta.kapoor@email.com", "+919876543233", "X-1414, Mahalaxmi, Mumbai 400034"),
    ("Nitin Agarwal", "nitin.agarwal@email.com", "+919876543234", "Y-1515, Colaba, Mumbai 400005"),
    ("Padma Sundaram", "padma.sundaram@email.com", "+919876543235", "Z-1616, Fort, Mumbai 400001"),
    ("Girish Shetty", "girish.shetty@email.com", "+919876543236", "AA-1717, Churchgate, Mumbai 400020"),
    ("Asha Naik", "asha.naik@email.com", "+919876543237", "BB-1818, Marine Lines, Mumbai 400002"),
    ("Ramesh Patil", "ramesh.patil@email.com", "+919876543238", "CC-1919, Grant Road, Mumbai 400007"),
    ("Jaya Subramaniam", "jaya.subramaniam@email.com", "+919876543239", "DD-2020, Byculla, Mumbai 400008"),
    ("Manoj Tiwari", "manoj.tiwari@email.com", "+919876543240", "EE-2121, Lalbaug, Mumbai 400012"),
    ("Sunita Choudhary", "sunita.choudhary@email.com", "+919876543241", "FF-2222, Parel, Mumbai 400012"),
    ("Harish Menon", "harish.menon@email.com", "+919876543242", "GG-2323, Wadala, Mumbai 400031"),
    ("Bhavana Desai", "bhavana.desai@email.com", "+919876543243", "HH-2424, Matunga, Mumbai 400019"),
    ("Gautam Rao", "gautam.rao@email.com", "+919876543244", "II-2525, King Circle, Mumbai 400019"),
    ("Nandini Hegde", "nandini.hegde@email.com", "+919876543245", "JJ-2626, Santacruz East, Mumbai 400055"),
    ("Krishna Murthy", "krishna.murthy@email.com", "+919876543246", "KK-2727, Vileparle West, Mumbai 400056"),
    ("Anjali Sharma", "anjali.sharma@email.com", "+919876543247", "LL-2828, Juhu, Mumbai 400049"),
    ("Sunil Reddy", "sunil.reddy@email.com", "+919876543248", "MM-2929, Versova, Mumbai 400061"),
    ("Preeti Singh", "preeti.singh@email.com", "+919876543249", "NN-3030, Lokhandwala, Mumbai 400053"),
]

EXPENSE_CATEGORIES = [
    ("Rent", 65000, 75000),
    ("Salaries", 150000, 200000),
    ("Utilities", 8000, 15000),
    ("Marketing", 15000, 35000),
    ("Inventory Purchase", 50000, 100000),
    ("Maintenance", 5000, 15000),
    ("Insurance", 12000, 18000),
    ("Transportation", 10000, 25000),
    ("Office Supplies", 3000, 8000),
    ("Software Subscriptions", 8000, 15000),
    ("Internet & Phone", 5000, 10000),
    ("Security", 8000, 12000),
]

def generate_serial():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def seed_data():
    db = SessionLocal()
    try:
        print("🚀 Starting COMPREHENSIVE data seeding (5000+ records)...")
        print("=" * 60)
        
        # Get or create store
        store = db.query(models.Store).first()
        if not store:
            store = models.Store(
                name="SKOPE Electronics & Lifestyle Store",
                address="Shop No. 101-105, Phoenix Mall, Lower Parel, Mumbai 400013",
                phone="+91-22-40001234",
                email="store@skope.com",
                gst_number="27AABCS1234F1Z5",
                is_active=True
            )
            db.add(store)
            db.commit()
            db.refresh(store)
        store_id = store.id
        print(f"✅ Store: {store.name}")
        
        # Get admin and create staff
        print("\n👤 Creating staff members...")
        admin = db.query(models.User).filter(models.User.role == models.UserRole.SUPER_ADMIN).first()
        staff_users = [admin] if admin else []
        
        for name, email, role in STAFF:
            existing = db.query(models.User).filter(models.User.email == email).first()
            if existing:
                staff_users.append(existing)
            else:
                from passlib.context import CryptContext
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                user = models.User(
                    email=email,
                    username=email.split("@")[0],
                    hashed_password=pwd_context.hash("password123"),
                    full_name=name,
                    role=role,
                    is_active=True,
                    store_id=store_id
                )
                db.add(user)
                staff_users.append(user)
        db.commit()
        
        # Filter sales staff only for assigning to sales
        sales_staff = [u for u in staff_users if u and u.role in [models.UserRole.SALES_STAFF, models.UserRole.STORE_MANAGER, models.UserRole.SUPER_ADMIN]]
        print(f"✅ {len(staff_users)} staff members ready, {len(sales_staff)} sales staff")
        
        # Clear old data
        print("\n🧹 Clearing old transaction data...")
        db.query(models.SaleItem).delete()
        db.query(models.Sale).delete()
        db.query(models.Expense).delete()
        db.query(models.Batch).delete()
        db.commit()
        
        # Create Products with batches
        print("\n📦 Creating products and inventory batches...")
        products = []
        sku_counter = 10000
        
        for name, category, brand, cost, price, warranty, desc in PRODUCTS:
            existing = db.query(models.Product).filter(models.Product.name == name).first()
            if existing:
                existing.current_stock = random.randint(30, 300)
                existing.cost_price = cost
                existing.unit_price = price
                existing.brand = brand
                existing.description = desc
                existing.warranty_months = warranty
                products.append(existing)
            else:
                product = models.Product(
                    name=name,
                    sku=f"SKU{sku_counter}",
                    category=category,
                    brand=brand,
                    description=desc,
                    cost_price=cost,
                    unit_price=price,
                    gst_rate=18.0 if price > 1000 else 12.0 if price > 100 else 5.0,
                    warranty_months=warranty,
                    current_stock=random.randint(30, 300),
                    minimum_stock=10,
                    store_id=store_id,
                    is_active=True
                )
                db.add(product)
                products.append(product)
                sku_counter += 1
        db.commit()
        
        # Create batches for products
        for prod in products:
            for i in range(random.randint(1, 3)):
                batch = models.Batch(
                    batch_id=f"BATCH-{prod.id}-{i+1}-{random.randint(1000,9999)}",
                    product_id=prod.id,
                    quantity=random.randint(20, 100),
                    remaining_quantity=random.randint(10, 50),
                    manufacturing_date=datetime.now() - timedelta(days=random.randint(30, 180)),
                    received_date=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(batch)
        db.commit()
        print(f"✅ {len(products)} products with inventory batches")
        
        # Create Customers with full details
        print("\n👥 Creating customers with complete profiles...")
        customers = []
        for name, email, phone, address in CUSTOMERS:
            existing = db.query(models.Customer).filter(models.Customer.phone == phone).first()
            if existing:
                customers.append(existing)
            else:
                # Random birthday between 1970-2000
                birth_year = random.randint(1970, 2000)
                birth_month = random.randint(1, 12)
                birth_day = random.randint(1, 28)
                
                customer = models.Customer(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address,
                    date_of_birth=datetime(birth_year, birth_month, birth_day),
                    total_purchases=0,
                    loyalty_points=0,
                    store_id=store_id
                )
                db.add(customer)
                customers.append(customer)
        db.commit()
        print(f"✅ {len(customers)} customers")
        
        # Generate 5000 Sales from Dec 1, 2025 to Jan 2, 2026 (including today)
        print("\n💰 Generating 5000 sales transactions...")
        start_date = datetime(2025, 12, 1)
        end_date = datetime(2026, 1, 2, 23, 59, 59)  # Include full day of Jan 2
        total_days = (end_date - start_date).days + 1
        target_sales = 5000
        sales_per_day_base = target_sales // total_days
        
        sales_count = 0
        invoice_num = 100001
        current_date = start_date
        
        while current_date <= end_date and sales_count < target_sales:
            # Vary sales by day of week and holiday season
            if current_date.weekday() >= 5:  # Weekend
                daily_target = int(sales_per_day_base * 1.5)
            elif current_date.day >= 20 and current_date.month == 12:  # Holiday rush
                daily_target = int(sales_per_day_base * 2)
            elif current_date.month == 1 and current_date.day <= 3:  # New Year sale
                daily_target = int(sales_per_day_base * 1.8)
            else:
                daily_target = sales_per_day_base
            
            for _ in range(min(daily_target, target_sales - sales_count)):
                customer = random.choice(customers)
                seller = random.choice(sales_staff) if sales_staff else None
                num_items = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
                sale_products = random.sample(products, min(num_items, len(products)))
                
                subtotal = 0
                gst_total = 0
                
                # Random time during business hours (9 AM to 10 PM)
                sale_time = current_date + timedelta(
                    hours=random.randint(9, 21),
                    minutes=random.randint(0, 59),
                    seconds=random.randint(0, 59)
                )
                
                # Payment method distribution
                payment = random.choices(
                    [models.PaymentMode.CASH, models.PaymentMode.CARD, models.PaymentMode.UPI, models.PaymentMode.QR_CODE],
                    weights=[20, 35, 40, 5]
                )[0]
                
                # Discount for loyalty customers or promotions
                discount = 0
                if customer.loyalty_points and customer.loyalty_points > 100:
                    discount = random.choice([0, 5, 10])
                elif current_date.day >= 25 and current_date.month == 12:
                    discount = random.choice([5, 10, 15])
                
                sale = models.Sale(
                    invoice_number=f"INV{current_date.strftime('%y%m')}{invoice_num}",
                    customer_id=customer.id,
                    store_id=store_id,
                    created_by=seller.id if seller else None,
                    sale_date=sale_time,
                    payment_mode=payment,
                    payment_status="completed",
                    subtotal=0,
                    gst_amount=0,
                    total_amount=0,
                    discount=discount
                )
                db.add(sale)
                db.flush()
                invoice_num += 1
                
                for prod in sale_products:
                    qty = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
                    gst_rate = prod.gst_rate or 18.0
                    item_price = prod.unit_price * qty
                    item_gst = round(item_price * (gst_rate / 100), 2)
                    
                    # Add warranty and serial for electronics
                    serial = generate_serial() if prod.warranty_months > 0 else None
                    warranty_exp = None
                    if prod.warranty_months > 0:
                        warranty_exp = sale_time + timedelta(days=prod.warranty_months * 30)
                    
                    sale_item = models.SaleItem(
                        sale_id=sale.id,
                        product_id=prod.id,
                        quantity=qty,
                        unit_price=prod.unit_price,
                        gst_rate=gst_rate,
                        gst_amount=item_gst,
                        total_price=round(item_price + item_gst, 2),
                        serial_number=serial,
                        warranty_expires_at=warranty_exp
                    )
                    db.add(sale_item)
                    subtotal += item_price
                    gst_total += item_gst
                    
                    # Update stock
                    if prod.current_stock >= qty:
                        prod.current_stock -= qty
                
                # Apply discount and finalize
                total = subtotal + gst_total
                if discount > 0:
                    total = total * (1 - discount / 100)
                
                sale.subtotal = round(subtotal, 2)
                sale.gst_amount = round(gst_total, 2)
                sale.total_amount = round(total, 2)
                
                # Update customer stats
                customer.total_purchases = (customer.total_purchases or 0) + total
                customer.loyalty_points = (customer.loyalty_points or 0) + int(total / 100)
                
                sales_count += 1
                
                if sales_count % 500 == 0:
                    db.commit()
                    print(f"   📊 {sales_count} sales created...")
            
            current_date += timedelta(days=1)
        
        db.commit()
        print(f"✅ {sales_count} sales transactions created!")
        
        # Generate Expenses
        print("\n📊 Generating expenses...")
        expense_count = 0
        current_date = start_date
        
        while current_date <= end_date:
            # Major recurring expenses on 1st and 15th
            if current_date.day == 1:
                for cat, min_amt, max_amt in [("Rent", 65000, 75000), ("Insurance", 12000, 18000)]:
                    expense = models.Expense(
                        description=f"{cat} payment for {current_date.strftime('%B %Y')}",
                        amount=random.randint(min_amt, max_amt),
                        category=cat,
                        payment_mode=models.PaymentMode.UPI,
                        vendor_name=f"{cat} Provider",
                        receipt_number=f"RCP{current_date.strftime('%Y%m%d')}{expense_count}",
                        expense_date=current_date,
                        store_id=store_id,
                        created_by=admin.id if admin else None
                    )
                    db.add(expense)
                    expense_count += 1
            
            if current_date.day == 15:
                # Salaries
                expense = models.Expense(
                    description=f"Staff salaries for {current_date.strftime('%B %Y')}",
                    amount=random.randint(150000, 200000),
                    category="Salaries",
                    payment_mode=models.PaymentMode.UPI,
                    vendor_name="Staff Payroll",
                    receipt_number=f"SAL{current_date.strftime('%Y%m%d')}",
                    expense_date=current_date,
                    store_id=store_id,
                    created_by=admin.id if admin else None
                )
                db.add(expense)
                expense_count += 1
            
            # Random daily operational expenses
            if random.random() > 0.4:
                cat = random.choice(["Utilities", "Marketing", "Maintenance", "Office Supplies", "Transportation", "Internet & Phone"])
                min_amt, max_amt = next(((mi, ma) for c, mi, ma in EXPENSE_CATEGORIES if c == cat), (1000, 5000))
                expense = models.Expense(
                    description=f"{cat} - {random.choice(['Monthly', 'Weekly', 'Ad-hoc'])} expense",
                    amount=random.randint(min_amt // 5, max_amt // 3),
                    category=cat,
                    payment_mode=random.choice([models.PaymentMode.CASH, models.PaymentMode.UPI, models.PaymentMode.CARD]),
                    vendor_name=f"{cat} Vendor",
                    receipt_number=f"EXP{current_date.strftime('%Y%m%d')}{expense_count}",
                    expense_date=current_date,
                    store_id=store_id,
                    created_by=admin.id if admin else None
                )
                db.add(expense)
                expense_count += 1
            
            current_date += timedelta(days=1)
        
        db.commit()
        print(f"✅ {expense_count} expenses created")
        
        # Set some products to low stock for alerts
        print("\n⚠️  Setting low stock alerts...")
        low_stock_products = random.sample(products, 12)
        for prod in low_stock_products[:8]:
            prod.current_stock = random.randint(3, 9)
        for prod in low_stock_products[8:]:
            prod.current_stock = 0
        db.commit()
        
        # Calculate totals for summary
        total_revenue = db.query(models.Sale).with_entities(
            db.query(models.Sale).filter(models.Sale.store_id == store_id)
        ).all()
        
        print("\n" + "=" * 60)
        print("🎉 COMPREHENSIVE DATA SEEDING COMPLETE!")
        print("=" * 60)
        print(f"📦 Products: {len(products)}")
        print(f"👥 Customers: {len(customers)}")
        print(f"👤 Staff/Sellers: {len(staff_users)}")
        print(f"💰 Sales: {sales_count}")
        print(f"📊 Expenses: {expense_count}")
        print(f"⚠️  Low Stock Items: 12")
        print("=" * 60)
        print("\n👉 REFRESH YOUR BROWSER to see all the data!")
        print("👉 Restart backend if needed: python -m uvicorn app.main:app --reload --port 8000")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
