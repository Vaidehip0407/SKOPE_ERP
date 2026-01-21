"""
Database Initialization Script
This script creates the database tables and adds initial data including a default admin user.
"""
from app.db.database import engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash
from app.db.models import UserRole

def init_database():
    """Initialize the database with tables and default data"""
    print("Initializing database...")
    
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        
        if admin:
            print("INFO: Admin user already exists")
            return
        
        # Create default store
        print("Creating default store...")
        store = models.Store(
            name="Main Store",
            address="123 Main Street, City, State",
            phone="+1234567890",
            email="store@example.com",
            gst_number="GST123456789"
        )
        db.add(store)
        db.flush()
        print("Default store created")
        
        # Create admin user
        print("Creating admin user...")
        admin = models.User(
            email="admin@example.com",
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            store_id=store.id
        )
        db.add(admin)
        
        # Create sample store manager
        print("Creating sample store manager...")
        manager = models.User(
            email="manager@example.com",
            username="manager",
            full_name="Store Manager",
            hashed_password=get_password_hash("manager123"),
            role=UserRole.STORE_MANAGER,
            is_active=True,
            store_id=store.id
        )
        db.add(manager)
        
        # Create sample sales staff
        print("Creating sample sales staff...")
        staff = models.User(
            email="sales@example.com",
            username="sales",
            full_name="Sales Staff",
            hashed_password=get_password_hash("sales123"),
            role=UserRole.SALES_STAFF,
            is_active=True,
            store_id=store.id
        )
        db.add(staff)
        
        db.commit()
        
        print("\n" + "="*60)
        print("SUCCESS: Database initialized successfully!")
        print("="*60)
        print("\nDefault User Credentials:")
        print("\n1. Super Admin:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n2. Store Manager:")
        print("   Username: manager")
        print("   Password: manager123")
        print("\n3. Sales Staff:")
        print("   Username: sales")
        print("   Password: sales123")
        print("\nIMPORTANT: Please change these passwords immediately!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"ERROR: Failed to initialize database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()

