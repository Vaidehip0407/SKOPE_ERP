"""Check what's in the database and fix any issues"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db import models

def debug_and_fix():
    db = SessionLocal()
    try:
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        print("=" * 60)
        print("DATABASE DEBUG REPORT")
        print("=" * 60)
        print(f"Current time: {now}")
        print(f"Today start: {today_start}")
        print(f"Today end: {today_end}")
        
        # Check stores
        stores = db.query(models.Store).all()
        print(f"\n📍 STORES: {len(stores)}")
        for s in stores:
            print(f"   ID: {s.id}, Name: {s.name}")
        
        # Check users
        users = db.query(models.User).all()
        print(f"\n👤 USERS: {len(users)}")
        for u in users[:5]:
            print(f"   ID: {u.id}, Email: {u.email}, Role: {u.role}, Store ID: {u.store_id}")
        
        # Check all sales
        all_sales = db.query(models.Sale).count()
        print(f"\n💰 TOTAL SALES: {all_sales}")
        
        # Check sales by date range
        jan_2_sales = db.query(models.Sale).filter(
            models.Sale.sale_date >= datetime(2026, 1, 2),
            models.Sale.sale_date < datetime(2026, 1, 3)
        ).all()
        print(f"\n📅 SALES ON JAN 2, 2026: {len(jan_2_sales)}")
        if jan_2_sales:
            print(f"   Sample dates: {[s.sale_date for s in jan_2_sales[:5]]}")
            print(f"   Store IDs: {set(s.store_id for s in jan_2_sales)}")
            print(f"   Total amount: ₹{sum(s.total_amount for s in jan_2_sales):,.2f}")
        
        # Check today's sales using same logic as API
        today_sales = db.query(models.Sale).filter(
            models.Sale.sale_date >= today_start,
            models.Sale.sale_date < today_end
        ).all()
        print(f"\n🔍 TODAY'S SALES (using API logic): {len(today_sales)}")
        if today_sales:
            print(f"   Sample dates: {[s.sale_date for s in today_sales[:5]]}")
            print(f"   Total: ₹{sum(s.total_amount for s in today_sales):,.2f}")
        
        # Check today's expenses
        today_expenses = db.query(models.Expense).filter(
            models.Expense.expense_date >= today_start,
            models.Expense.expense_date < today_end
        ).all()
        print(f"\n📊 TODAY'S EXPENSES: {len(today_expenses)}")
        if today_expenses:
            print(f"   Total: ₹{sum(e.amount for e in today_expenses):,.2f}")
        
        # Get the last 5 sales to see their dates
        recent_sales = db.query(models.Sale).order_by(models.Sale.sale_date.desc()).limit(10).all()
        print(f"\n🕐 MOST RECENT 10 SALES:")
        for s in recent_sales:
            print(f"   {s.invoice_number}: {s.sale_date} - ₹{s.total_amount:,.2f} (Store: {s.store_id})")
        
        # FIX: If Jan 2 sales exist but today filter doesn't find them
        if jan_2_sales and not today_sales:
            print("\n⚠️  DATE MISMATCH DETECTED!")
            print(f"   Jan 2 sales dates use: {jan_2_sales[0].sale_date if jan_2_sales else 'N/A'}")
            print(f"   Today filter expects >= {today_start} and < {today_end}")
            
            # Calculate the date difference
            if jan_2_sales:
                sample_date = jan_2_sales[0].sale_date
                print(f"\n   Sample sale date: {sample_date}")
                print(f"   Is >= today_start? {sample_date >= today_start}")
                print(f"   Is < today_end? {sample_date < today_end}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_and_fix()
