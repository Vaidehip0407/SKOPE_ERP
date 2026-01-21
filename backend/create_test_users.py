"""
Create test users for different roles to test RBAC
"""
import sys
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.core.security import get_password_hash

def create_test_users():
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("Creating Test Users for RBAC Testing")
        print("=" * 70)
        
        # Get store
        store = db.query(models.Store).first()
        if not store:
            print("[ERROR] No store found! Run init_db.py first.")
            return
        
        print(f"\n[OK] Found store: {store.name} (ID: {store.id})")
        
        test_users = [
            {
                "username": "admin",
                "email": "admin@skope.com",
                "full_name": "System Administrator",
                "role": models.UserRole.SUPER_ADMIN,
                "password": "admin123",
                "store_id": store.id
            },
            {
                "username": "manager",
                "email": "manager@skope.com",
                "full_name": "Store Manager",
                "role": models.UserRole.STORE_MANAGER,
                "password": "manager123",
                "store_id": store.id
            },
            {
                "username": "sales",
                "email": "sales@skope.com",
                "full_name": "Sales Staff",
                "role": models.UserRole.SALES_STAFF,
                "password": "sales123",
                "store_id": store.id
            },
            {
                "username": "marketing",
                "email": "marketing@skope.com",
                "full_name": "Marketing Staff",
                "role": models.UserRole.MARKETING,
                "password": "marketing123",
                "store_id": store.id
            },
            {
                "username": "accounts",
                "email": "accounts@skope.com",
                "full_name": "Accounts Staff",
                "role": models.UserRole.ACCOUNTS,
                "password": "accounts123",
                "store_id": store.id
            }
        ]
        
        print("\n" + "=" * 70)
        print("Creating Users...")
        print("=" * 70)
        
        for user_data in test_users:
            # Check if user already exists
            existing_user = db.query(models.User).filter(
                models.User.username == user_data["username"]
            ).first()
            
            if existing_user:
                print(f"\n[SKIP] User '{user_data['username']}' already exists. Skipping.")
                continue
            
            # Create user
            db_user = models.User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                role=user_data["role"],
                store_id=user_data["store_id"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=True
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            print(f"\n[OK] Created: {user_data['full_name']}")
            print(f"   Role: {user_data['role'].value}")
            print(f"   Username: {user_data['username']}")
            print(f"   Password: {user_data['password']}")
        
        print("\n" + "=" * 70)
        print("[SUCCESS] Test Users Created Successfully!")
        print("=" * 70)
        
        print("\n[*] Login Credentials:")
        print("-" * 70)
        print("\n[SUPER ADMIN] (Full Access)")
        print("   Username: admin")
        print("   Password: admin123")
        
        print("\n[STORE MANAGER] (Store-level Management)")
        print("   Username: manager")
        print("   Password: manager123")
        
        print("\n[SALES STAFF] (Sales & Customers)")
        print("   Username: sales")
        print("   Password: sales123")
        
        print("\n[MARKETING STAFF] (Campaigns & Customers)")
        print("   Username: marketing")
        print("   Password: marketing123")
        
        print("\n[ACCOUNTS STAFF] (Financial & Reports)")
        print("   Username: accounts")
        print("   Password: accounts123")
        
        print("\n" + "=" * 70)
        print("[*] Testing Instructions:")
        print("=" * 70)
        print("\n1. Login with each user")
        print("2. Verify menu items show/hide based on role")
        print("3. Test permissions:")
        print("   - Super Admin: Can do everything")
        print("   - Store Manager: Can manage store, but not see other stores")
        print("   - Sales Staff: Can create sales, view products")
        print("   - Marketing: Can create campaigns, view customers")
        print("   - Accounts: Can add expenses, view financial reports")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n[ERROR] Error creating test users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()

