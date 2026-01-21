"""
Comprehensive Data Seeder for Advanced Reports
Seeds all data needed to make every advanced report work properly
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

# Sample data
CATEGORIES = ["Mobiles", "Laptops", "TVs", "ACs", "Refrigerators", "Washing Machines", "Accessories", "Audio"]
BRANDS = ["Samsung", "LG", "Sony", "Apple", "OnePlus", "Xiaomi", "HP", "Dell", "Whirlpool", "Haier"]
PAYMENT_MODES = [models.PaymentMode.CASH, models.PaymentMode.CARD, models.PaymentMode.UPI, models.PaymentMode.FINANCE]

PRODUCT_DATA = [
    # Mobiles
    {"name": "Samsung Galaxy S24 Ultra", "category": "Mobiles", "brand": "Samsung", "cost": 95000, "price": 124999, "stock": 15},
    {"name": "iPhone 15 Pro Max", "category": "Mobiles", "brand": "Apple", "cost": 125000, "price": 159900, "stock": 8},
    {"name": "OnePlus 12", "category": "Mobiles", "brand": "OnePlus", "cost": 52000, "price": 69999, "stock": 20},
    {"name": "Xiaomi 14 Ultra", "category": "Mobiles", "brand": "Xiaomi", "cost": 72000, "price": 99999, "stock": 12},
    {"name": "Samsung Galaxy A54", "category": "Mobiles", "brand": "Samsung", "cost": 28000, "price": 38999, "stock": 25},
    {"name": "iPhone 15", "category": "Mobiles", "brand": "Apple", "cost": 65000, "price": 79900, "stock": 10},
    {"name": "Redmi Note 13 Pro", "category": "Mobiles", "brand": "Xiaomi", "cost": 18000, "price": 25999, "stock": 30},
    {"name": "OnePlus Nord CE 4", "category": "Mobiles", "brand": "OnePlus", "cost": 20000, "price": 27999, "stock": 22},
    
    # Laptops
    {"name": "MacBook Pro 14 M3", "category": "Laptops", "brand": "Apple", "cost": 165000, "price": 199900, "stock": 5},
    {"name": "HP Pavilion 15", "category": "Laptops", "brand": "HP", "cost": 45000, "price": 59999, "stock": 12},
    {"name": "Dell Inspiron 15", "category": "Laptops", "brand": "Dell", "cost": 48000, "price": 64999, "stock": 10},
    {"name": "ASUS ROG Strix G16", "category": "Laptops", "brand": "ASUS", "cost": 95000, "price": 124999, "stock": 6},
    {"name": "Lenovo ThinkPad E14", "category": "Laptops", "brand": "Lenovo", "cost": 52000, "price": 69999, "stock": 8},
    
    # TVs
    {"name": "Samsung 55\" QLED 4K", "category": "TVs", "brand": "Samsung", "cost": 65000, "price": 89999, "stock": 7},
    {"name": "LG 65\" OLED C3", "category": "TVs", "brand": "LG", "cost": 145000, "price": 189999, "stock": 3},
    {"name": "Sony Bravia 55\" 4K", "category": "TVs", "brand": "Sony", "cost": 72000, "price": 94999, "stock": 5},
    {"name": "Samsung 43\" Crystal 4K", "category": "TVs", "brand": "Samsung", "cost": 28000, "price": 39999, "stock": 12},
    {"name": "LG 50\" NanoCell", "category": "TVs", "brand": "LG", "cost": 42000, "price": 57999, "stock": 8},
    
    # ACs
    {"name": "Samsung 1.5T Split AC", "category": "ACs", "brand": "Samsung", "cost": 32000, "price": 45999, "stock": 15},
    {"name": "LG 1.5T Dual Inverter", "category": "ACs", "brand": "LG", "cost": 38000, "price": 52999, "stock": 10},
    {"name": "Daikin 1.5T 5 Star", "category": "ACs", "brand": "Daikin", "cost": 42000, "price": 58999, "stock": 8},
    {"name": "Voltas 1T Window AC", "category": "ACs", "brand": "Voltas", "cost": 22000, "price": 32999, "stock": 6},
    
    # Refrigerators
    {"name": "Samsung 653L Side by Side", "category": "Refrigerators", "brand": "Samsung", "cost": 85000, "price": 119999, "stock": 4},
    {"name": "LG 260L Double Door", "category": "Refrigerators", "brand": "LG", "cost": 28000, "price": 38999, "stock": 10},
    {"name": "Whirlpool 190L Single Door", "category": "Refrigerators", "brand": "Whirlpool", "cost": 12000, "price": 17999, "stock": 15},
    {"name": "Samsung 324L Frost Free", "category": "Refrigerators", "brand": "Samsung", "cost": 32000, "price": 44999, "stock": 8},
    
    # Washing Machines
    {"name": "LG 8kg Front Load", "category": "Washing Machines", "brand": "LG", "cost": 38000, "price": 49999, "stock": 7},
    {"name": "Samsung 7kg Top Load", "category": "Washing Machines", "brand": "Samsung", "cost": 18000, "price": 26999, "stock": 12},
    {"name": "Whirlpool 7.5kg Semi Auto", "category": "Washing Machines", "brand": "Whirlpool", "cost": 10000, "price": 14999, "stock": 10},
    {"name": "Bosch 8kg Front Load", "category": "Washing Machines", "brand": "Bosch", "cost": 45000, "price": 59999, "stock": 5},
    
    # Accessories
    {"name": "Samsung Galaxy Buds Pro 2", "category": "Accessories", "brand": "Samsung", "cost": 12000, "price": 17999, "stock": 25},
    {"name": "Apple AirPods Pro 2", "category": "Accessories", "brand": "Apple", "cost": 18000, "price": 24900, "stock": 20},
    {"name": "JBL Flip 6 Speaker", "category": "Accessories", "brand": "JBL", "cost": 8000, "price": 12999, "stock": 18},
    {"name": "Samsung 25W Charger", "category": "Accessories", "brand": "Samsung", "cost": 800, "price": 1499, "stock": 50},
    {"name": "Apple 20W USB-C Charger", "category": "Accessories", "brand": "Apple", "cost": 1200, "price": 1900, "stock": 40},
    {"name": "Anker PowerCore 20000", "category": "Accessories", "brand": "Anker", "cost": 2500, "price": 3999, "stock": 30},
    {"name": "Sony WH-1000XM5", "category": "Audio", "brand": "Sony", "cost": 22000, "price": 29990, "stock": 10},
    {"name": "Bose QuietComfort 45", "category": "Audio", "brand": "Bose", "cost": 24000, "price": 32900, "stock": 8},
    
    # Low stock items for reorder alerts
    {"name": "iPhone 15 Pro", "category": "Mobiles", "brand": "Apple", "cost": 110000, "price": 134900, "stock": 2, "min_stock": 5},
    {"name": "Samsung Galaxy Z Fold 5", "category": "Mobiles", "brand": "Samsung", "cost": 140000, "price": 164999, "stock": 1, "min_stock": 3},
    {"name": "MacBook Air M3", "category": "Laptops", "brand": "Apple", "cost": 95000, "price": 114900, "stock": 1, "min_stock": 4},
    
    # High value slow moving items
    {"name": "Sony A9 OLED 77\"", "category": "TVs", "brand": "Sony", "cost": 350000, "price": 449999, "stock": 2, "min_stock": 1},
    {"name": "LG Signature OLED 88\"", "category": "TVs", "brand": "LG", "cost": 550000, "price": 699999, "stock": 1, "min_stock": 1},
]

CUSTOMER_DATA = [
    {"name": "Rajesh Kumar", "phone": "9876543210", "email": "rajesh.kumar@email.com"},
    {"name": "Priya Sharma", "phone": "9876543211", "email": "priya.sharma@email.com"},
    {"name": "Amit Patel", "phone": "9876543212", "email": "amit.patel@email.com"},
    {"name": "Sneha Gupta", "phone": "9876543213", "email": "sneha.gupta@email.com"},
    {"name": "Vikram Singh", "phone": "9876543214", "email": "vikram.singh@email.com"},
    {"name": "Anjali Verma", "phone": "9876543215", "email": "anjali.verma@email.com"},
    {"name": "Rohit Joshi", "phone": "9876543216", "email": "rohit.joshi@email.com"},
    {"name": "Neha Reddy", "phone": "9876543217", "email": "neha.reddy@email.com"},
    {"name": "Suresh Menon", "phone": "9876543218", "email": "suresh.menon@email.com"},
    {"name": "Kavita Nair", "phone": "9876543219", "email": "kavita.nair@email.com"},
    {"name": "Arjun Kapoor", "phone": "9876543220", "email": "arjun.kapoor@email.com"},
    {"name": "Deepika Rao", "phone": "9876543221", "email": "deepika.rao@email.com"},
    {"name": "Manish Agarwal", "phone": "9876543222", "email": "manish.agarwal@email.com"},
    {"name": "Pooja Desai", "phone": "9876543223", "email": "pooja.desai@email.com"},
    {"name": "Sanjay Khanna", "phone": "9876543224", "email": "sanjay.khanna@email.com"},
    {"name": "Ritu Malhotra", "phone": "9876543225", "email": "ritu.malhotra@email.com"},
    {"name": "Arun Bhatia", "phone": "9876543226", "email": "arun.bhatia@email.com"},
    {"name": "Meera Iyer", "phone": "9876543227", "email": "meera.iyer@email.com"},
    {"name": "Karan Mehta", "phone": "9876543228", "email": "karan.mehta@email.com"},
    {"name": "Shruti Saxena", "phone": "9876543229", "email": "shruti.saxena@email.com"},
]


def seed_reports_data():
    """Seed all data needed for advanced reports"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("SEEDING COMPREHENSIVE REPORTS DATA")
        print("=" * 60)
        
        # Get or create store
        store = db.query(models.Store).first()
        if not store:
            store = models.Store(
                name="Main Store",
                code="MAIN001",
                address="123 Main Street",
                phone="9999999999",
                email="store@skopeorp.com",
                is_active=True
            )
            db.add(store)
            db.commit()
            db.refresh(store)
            print(f"✓ Created store: {store.name}")
        else:
            print(f"✓ Using existing store: {store.name}")
        
        # Get sales staff users
        staff_users = db.query(models.User).filter(
            models.User.role.in_([models.UserRole.SALES_STAFF, models.UserRole.STORE_MANAGER, models.UserRole.ADMIN])
        ).all()
        
        if not staff_users:
            # Create some staff users
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            staff_data = [
                {"username": "staff1", "full_name": "Rahul Verma", "role": models.UserRole.SALES_STAFF},
                {"username": "staff2", "full_name": "Priya Singh", "role": models.UserRole.SALES_STAFF},
                {"username": "staff3", "full_name": "Amit Kumar", "role": models.UserRole.SALES_STAFF},
                {"username": "manager1", "full_name": "Vijay Sharma", "role": models.UserRole.STORE_MANAGER},
            ]
            
            for data in staff_data:
                user = models.User(
                    username=data["username"],
                    email=f"{data['username']}@skopeorp.com",
                    full_name=data["full_name"],
                    hashed_password=pwd_context.hash("password123"),
                    role=data["role"],
                    store_id=store.id,
                    is_active=True
                )
                db.add(user)
            
            db.commit()
            staff_users = db.query(models.User).filter(
                models.User.role.in_([models.UserRole.SALES_STAFF, models.UserRole.STORE_MANAGER])
            ).all()
            print(f"✓ Created {len(staff_users)} staff users")
        else:
            print(f"✓ Found {len(staff_users)} existing staff users")
        
        # Seed Products
        print("\n--- Seeding Products ---")
        products = []
        for pdata in PRODUCT_DATA:
            # Check if product exists
            existing = db.query(models.Product).filter(models.Product.name == pdata["name"]).first()
            if existing:
                products.append(existing)
                continue
            
            product = models.Product(
                name=pdata["name"],
                sku=f"SKU-{pdata['name'][:3].upper()}-{random.randint(1000, 9999)}",
                category=pdata["category"],
                brand=pdata["brand"],
                cost_price=Decimal(str(pdata["cost"])),
                selling_price=Decimal(str(pdata["price"])),
                current_stock=pdata["stock"],
                minimum_stock=pdata.get("min_stock", 5),
                store_id=store.id,
                is_active=True
            )
            db.add(product)
            products.append(product)
        
        db.commit()
        print(f"✓ Seeded {len(PRODUCT_DATA)} products")
        
        # Refresh products to get IDs
        products = db.query(models.Product).filter(models.Product.store_id == store.id).all()
        
        # Seed Customers
        print("\n--- Seeding Customers ---")
        customers = []
        for cdata in CUSTOMER_DATA:
            existing = db.query(models.Customer).filter(models.Customer.phone == cdata["phone"]).first()
            if existing:
                customers.append(existing)
                continue
            
            customer = models.Customer(
                name=cdata["name"],
                phone=cdata["phone"],
                email=cdata["email"],
                store_id=store.id,
                total_purchases=Decimal("0"),
                is_active=True
            )
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        print(f"✓ Seeded {len(CUSTOMER_DATA)} customers")
        
        # Refresh customers
        customers = db.query(models.Customer).filter(models.Customer.store_id == store.id).all()
        
        # Seed Sales
        print("\n--- Seeding Sales (last 60 days) ---")
        sale_count = 0
        now = datetime.now()
        
        for days_ago in range(60, -1, -1):
            sale_date = now - timedelta(days=days_ago)
            
            # More sales on weekends
            num_sales = random.randint(8, 15) if sale_date.weekday() >= 5 else random.randint(5, 12)
            
            for _ in range(num_sales):
                # Random time during business hours
                hour = random.randint(10, 21)
                minute = random.randint(0, 59)
                sale_datetime = sale_date.replace(hour=hour, minute=minute, second=random.randint(0, 59))
                
                # Random customer (or walk-in)
                customer = random.choice(customers) if random.random() > 0.3 else None
                
                # Random staff
                staff = random.choice(staff_users) if staff_users else None
                
                # Random payment mode
                payment_mode = random.choice(PAYMENT_MODES)
                
                # Random discount
                discount_percent = random.choice([0, 0, 0, 5, 10, 15]) if random.random() > 0.6 else 0
                
                # Create sale
                invoice_num = f"INV-{sale_datetime.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                # Check if invoice exists
                existing_sale = db.query(models.Sale).filter(models.Sale.invoice_number == invoice_num).first()
                if existing_sale:
                    continue
                
                sale = models.Sale(
                    invoice_number=invoice_num,
                    sale_date=sale_datetime,
                    customer_id=customer.id if customer else None,
                    store_id=store.id,
                    created_by=staff.id if staff else None,
                    payment_mode=payment_mode,
                    payment_status="completed" if payment_mode != models.PaymentMode.FINANCE else random.choice(["completed", "pending"]),
                    total_amount=Decimal("0"),
                    discount=Decimal("0"),
                    tax_amount=Decimal("0"),
                    notes=""
                )
                db.add(sale)
                db.flush()
                
                # Add 1-4 items per sale
                num_items = random.randint(1, 4)
                selected_products = random.sample(products, min(num_items, len(products)))
                
                subtotal = Decimal("0")
                for product in selected_products:
                    quantity = random.randint(1, 3) if product.category == "Accessories" else 1
                    unit_price = product.selling_price
                    total_price = unit_price * quantity
                    subtotal += total_price
                    
                    # Warranty for electronics
                    warranty_months = 12 if product.category in ["Mobiles", "Laptops", "TVs", "ACs"] else 0
                    warranty_expires = sale_datetime + timedelta(days=warranty_months * 30) if warranty_months > 0 else None
                    
                    sale_item = models.SaleItem(
                        sale_id=sale.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        warranty_months=warranty_months,
                        warranty_expires_at=warranty_expires,
                        serial_number=f"SN-{random.randint(100000, 999999)}" if warranty_months > 0 else None
                    )
                    db.add(sale_item)
                
                # Calculate final amounts
                discount_amount = subtotal * Decimal(str(discount_percent)) / Decimal("100")
                tax_amount = (subtotal - discount_amount) * Decimal("0.18")  # 18% GST
                total = subtotal - discount_amount + tax_amount
                
                sale.discount = discount_amount
                sale.tax_amount = tax_amount
                sale.total_amount = total
                
                # Update customer total purchases
                if customer:
                    customer.total_purchases += total
                
                sale_count += 1
        
        db.commit()
        print(f"✓ Seeded {sale_count} sales with items")
        
        # Seed Staff Targets
        print("\n--- Seeding Staff Targets ---")
        current_month = now.strftime("%Y-%m")
        prev_month = (now.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
        
        for month in [prev_month, current_month]:
            for staff in staff_users:
                existing = db.query(models.StaffTarget).filter(
                    models.StaffTarget.user_id == staff.id,
                    models.StaffTarget.month == month
                ).first()
                
                if existing:
                    continue
                
                target_amount = Decimal(str(random.randint(300000, 800000)))
                achieved = target_amount * Decimal(str(random.uniform(0.6, 1.2)))
                
                target = models.StaffTarget(
                    user_id=staff.id,
                    store_id=store.id,
                    month=month,
                    target_amount=target_amount,
                    achieved_amount=achieved,
                    incentive_earned=max((achieved - target_amount) * Decimal("0.02"), Decimal("0")) if achieved > target_amount else Decimal("0"),
                    incentive_paid=Decimal("0") if month == current_month else max((achieved - target_amount) * Decimal("0.02"), Decimal("0")),
                    incentive_pending=max((achieved - target_amount) * Decimal("0.02"), Decimal("0")) if month == current_month and achieved > target_amount else Decimal("0")
                )
                db.add(target)
        
        db.commit()
        print(f"✓ Seeded staff targets for {len(staff_users)} staff")
        
        # Seed Staff Attendance
        print("\n--- Seeding Staff Attendance ---")
        for days_ago in range(30, -1, -1):
            date = (now - timedelta(days=days_ago)).date()
            
            # Skip Sundays
            if date.weekday() == 6:
                continue
            
            for staff in staff_users:
                existing = db.query(models.StaffAttendance).filter(
                    models.StaffAttendance.user_id == staff.id,
                    models.StaffAttendance.date == date
                ).first()
                
                if existing:
                    continue
                
                # 90% attendance rate
                status = "present" if random.random() > 0.1 else random.choice(["absent", "leave"])
                hours = random.uniform(8, 10) if status == "present" else 0
                
                attendance = models.StaffAttendance(
                    user_id=staff.id,
                    store_id=store.id,
                    date=date,
                    status=status,
                    check_in=datetime.combine(date, datetime.min.time().replace(hour=10)) if status == "present" else None,
                    check_out=datetime.combine(date, datetime.min.time().replace(hour=19)) if status == "present" else None,
                    hours_worked=Decimal(str(round(hours, 2)))
                )
                db.add(attendance)
        
        db.commit()
        print(f"✓ Seeded attendance for {len(staff_users)} staff")
        
        print("\n" + "=" * 60)
        print("✓ ALL REPORTS DATA SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  - Products: {len(products)}")
        print(f"  - Customers: {len(customers)}")
        print(f"  - Sales: {sale_count}")
        print(f"  - Staff: {len(staff_users)}")
        print("\nYou can now use all Advanced Reports!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_reports_data()
