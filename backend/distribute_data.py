"""Distribute products and data across all stores"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import random
from app.db.database import SessionLocal
from app.db import models

def distribute_data():
    db = SessionLocal()
    try:
        print("🔄 Distributing data across all stores...")
        
        stores = db.query(models.Store).filter(models.Store.is_active == True).all()
        print(f"📍 Found {len(stores)} stores")
        
        if len(stores) < 2:
            print("❌ Need at least 2 stores")
            return
            
        # Get all products
        products = db.query(models.Product).all()
        print(f"📦 Found {len(products)} products")
        
        # Distribute products across stores (some to each store)
        for i, prod in enumerate(products):
            store_idx = i % len(stores)
            prod.store_id = stores[store_idx].id
        db.commit()
        print("✅ Products distributed")
        
        # Get all customers
        customers = db.query(models.Customer).all()
        print(f"👥 Found {len(customers)} customers")
        
        # Distribute customers
        for i, cust in enumerate(customers):
            store_idx = i % len(stores)
            cust.store_id = stores[store_idx].id
        db.commit()
        print("✅ Customers distributed")
        
        # Get all users (except super admin)
        users = db.query(models.User).filter(models.User.role != models.UserRole.SUPER_ADMIN).all()
        print(f"👤 Found {len(users)} non-admin users")
        
        # Distribute users
        for i, user in enumerate(users):
            store_idx = i % len(stores)
            user.store_id = stores[store_idx].id
        db.commit()
        print("✅ Users distributed")
        
        # Verify
        print("\n📊 Store Stats After Distribution:")
        for store in stores:
            prods = db.query(models.Product).filter(models.Product.store_id == store.id).count()
            custs = db.query(models.Customer).filter(models.Customer.store_id == store.id).count()
            users = db.query(models.User).filter(models.User.store_id == store.id).count()
            sales = db.query(models.Sale).filter(models.Sale.store_id == store.id).count()
            print(f"   {store.name}: {prods} products, {custs} customers, {users} users, {sales} sales")
        
        print("\n🎉 DONE! Refresh your browser!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    distribute_data()
