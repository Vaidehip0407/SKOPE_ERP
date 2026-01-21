"""Add sales from Dec 27 to TODAY (Jan 2, 2026)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import random
import string
from app.db.database import SessionLocal
from app.db import models

def generate_serial():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def add_recent_sales():
    db = SessionLocal()
    try:
        now = datetime.now()
        print("🚀 Adding sales from Dec 27 to TODAY...")
        print(f"📅 Current date/time: {now}")
        
        # Get store
        store = db.query(models.Store).first()
        store_id = store.id
        print(f"🏪 Store: {store.name} (ID: {store_id})")
        
        # Get products and customers
        products = db.query(models.Product).filter(models.Product.store_id == store_id).all()
        if not products:
            products = db.query(models.Product).all()
        customers = db.query(models.Customer).filter(models.Customer.store_id == store_id).all()
        if not customers:
            customers = db.query(models.Customer).all()
        
        # Get sales staff
        sales_staff = db.query(models.User).filter(
            models.User.role.in_([models.UserRole.SALES_STAFF, models.UserRole.STORE_MANAGER, models.UserRole.SUPER_ADMIN])
        ).all()
        
        print(f"📦 Products: {len(products)}, 👥 Customers: {len(customers)}, 👤 Staff: {len(sales_staff)}")
        
        # Generate sales from Dec 27 to today
        start_date = datetime(2025, 12, 27)
        end_date = now  # Include current time
        
        sales_count = 0
        invoice_base = 500000
        current_date = start_date
        
        while current_date.date() <= end_date.date():
            # Vary sales: more on weekends and new year
            if current_date.weekday() >= 5:
                daily_sales = random.randint(80, 120)
            elif current_date.month == 1:
                daily_sales = random.randint(100, 150)  # New year sales
            else:
                daily_sales = random.randint(60, 100)
            
            print(f"   📅 {current_date.date()}: Adding {daily_sales} sales...")
            
            for i in range(daily_sales):
                customer = random.choice(customers)
                seller = random.choice(sales_staff) if sales_staff else None
                num_items = random.randint(1, 3)
                sale_products = random.sample(products, min(num_items, len(products)))
                
                subtotal = 0
                gst_total = 0
                
                # For today, use times up to current hour
                if current_date.date() == now.date():
                    max_hour = now.hour
                else:
                    max_hour = 21
                
                sale_hour = random.randint(9, max(9, max_hour))
                sale_time = current_date.replace(hour=sale_hour, minute=random.randint(0, 59), second=random.randint(0, 59))
                
                payment = random.choice([models.PaymentMode.CASH, models.PaymentMode.CARD, models.PaymentMode.UPI, models.PaymentMode.UPI])
                discount = random.choice([0, 0, 0, 5, 10])
                
                sale = models.Sale(
                    invoice_number=f"INV2601{invoice_base + sales_count}",
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
            
            db.commit()
            current_date += timedelta(days=1)
        
        # Add expenses for recent days
        print("\n📊 Adding expenses for recent days...")
        expense_count = 0
        current_date = datetime(2025, 12, 27)
        while current_date.date() <= end_date.date():
            if random.random() > 0.3:
                cat = random.choice(["Utilities", "Marketing", "Maintenance", "Transportation"])
                expense = models.Expense(
                    description=f"{cat} expense - {current_date.strftime('%d %b')}",
                    amount=random.randint(1000, 8000),
                    category=cat,
                    payment_mode=random.choice([models.PaymentMode.CASH, models.PaymentMode.UPI]),
                    expense_date=current_date,
                    store_id=store_id
                )
                db.add(expense)
                expense_count += 1
            current_date += timedelta(days=1)
        db.commit()
        
        # Verify today's sales
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_sales = db.query(models.Sale).filter(
            models.Sale.sale_date >= today_start,
            models.Sale.sale_date < today_start + timedelta(days=1),
            models.Sale.store_id == store_id
        ).all()
        
        print("\n" + "=" * 60)
        print("🎉 DONE!")
        print("=" * 60)
        print(f"✅ Added {sales_count} sales from Dec 27 to today")
        print(f"✅ Added {expense_count} expenses")
        print(f"\n📊 TODAY'S SALES: {len(today_sales)} transactions")
        print(f"💰 TODAY'S REVENUE: ₹{sum(s.total_amount for s in today_sales):,.2f}")
        print("\n👉 REFRESH YOUR BROWSER NOW!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_recent_sales()
