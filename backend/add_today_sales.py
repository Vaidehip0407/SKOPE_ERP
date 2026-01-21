"""
Quick fix: Add TODAY's sales explicitly with correct timestamps
Run this AFTER the main seed script
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import random
import string
from app.db.database import SessionLocal
from app.db import models

def generate_serial():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def add_today_sales():
    db = SessionLocal()
    try:
        print("🚀 Adding TODAY's sales...")
        
        # Get current time
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        print(f"📅 Today is: {today_start.date()}")
        print(f"🕐 Current time: {now}")
        
        # Get store - use the first store
        store = db.query(models.Store).first()
        if not store:
            print("❌ No store found!")
            return
        store_id = store.id
        print(f"🏪 Store: {store.name} (ID: {store_id})")
        
        # Get sales staff
        sales_staff = db.query(models.User).filter(
            models.User.role.in_([models.UserRole.SALES_STAFF, models.UserRole.STORE_MANAGER, models.UserRole.SUPER_ADMIN])
        ).all()
        print(f"👤 Found {len(sales_staff)} sales staff")
        
        # Get products and customers
        products = db.query(models.Product).filter(models.Product.store_id == store_id).all()
        if not products:
            products = db.query(models.Product).all()
        customers = db.query(models.Customer).filter(models.Customer.store_id == store_id).all()
        if not customers:
            customers = db.query(models.Customer).all()
        
        print(f"📦 Products: {len(products)}")
        print(f"👥 Customers: {len(customers)}")
        
        if not products or not customers:
            print("❌ No products or customers found!")
            return
        
        # Get current highest invoice number
        last_sale = db.query(models.Sale).order_by(models.Sale.id.desc()).first()
        invoice_base = 200000
        if last_sale and last_sale.invoice_number:
            try:
                # Extract numbers from invoice
                nums = ''.join(c for c in last_sale.invoice_number if c.isdigit())
                if nums:
                    invoice_base = int(nums[-6:]) + 1
            except:
                pass
        
        # Add 50 sales for TODAY with times from 9 AM to current time
        current_hour = now.hour
        if current_hour < 9:
            current_hour = 9
        
        sales_count = 0
        total_revenue = 0
        
        print(f"\n💰 Creating 50 sales for today (9 AM to {current_hour}:00)...")
        
        for i in range(50):
            customer = random.choice(customers)
            seller = random.choice(sales_staff) if sales_staff else None
            num_items = random.randint(1, 3)
            sale_products = random.sample(products, min(num_items, len(products)))
            
            subtotal = 0
            gst_total = 0
            
            # Time between 9 AM and now (hour already passed)
            sale_hour = random.randint(9, max(9, current_hour - 1))
            sale_minute = random.randint(0, 59)
            sale_time = today_start.replace(hour=sale_hour, minute=sale_minute, second=random.randint(0, 59))
            
            payment = random.choice([models.PaymentMode.CASH, models.PaymentMode.CARD, models.PaymentMode.UPI, models.PaymentMode.UPI])
            discount = random.choice([0, 0, 0, 5, 10])
            
            sale = models.Sale(
                invoice_number=f"INVTODAY{invoice_base + i}",
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
            
            for prod in sale_products:
                qty = random.randint(1, 2)
                gst_rate = prod.gst_rate or 18.0
                item_price = prod.unit_price * qty
                item_gst = round(item_price * (gst_rate / 100), 2)
                
                serial = generate_serial() if prod.warranty_months and prod.warranty_months > 0 else None
                warranty_exp = sale_time + timedelta(days=prod.warranty_months * 30) if prod.warranty_months and prod.warranty_months > 0 else None
                
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
            
            total = subtotal + gst_total
            if discount > 0:
                total = total * (1 - discount / 100)
            
            sale.subtotal = round(subtotal, 2)
            sale.gst_amount = round(gst_total, 2)
            sale.total_amount = round(total, 2)
            
            customer.total_purchases = (customer.total_purchases or 0) + total
            
            sales_count += 1
            total_revenue += total
        
        db.commit()
        
        # Verify by checking today's sales
        print(f"\n✅ Added {sales_count} sales for today!")
        print(f"💵 Total revenue: ₹{total_revenue:,.2f}")
        
        # Double check
        today_check = db.query(models.Sale).filter(
            models.Sale.sale_date >= today_start,
            models.Sale.sale_date < today_start + timedelta(days=1),
            models.Sale.store_id == store_id
        ).all()
        
        print(f"\n🔍 Verification: Found {len(today_check)} sales for today in database")
        print(f"   Total: ₹{sum(s.total_amount for s in today_check):,.2f}")
        
        print("\n" + "=" * 50)
        print("🎉 DONE! Refresh your browser now!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_today_sales()
