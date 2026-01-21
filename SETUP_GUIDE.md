# Retail Management System - Setup Guide

This guide will walk you through setting up the Retail Management System from scratch.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Required Software
- **Python 3.9 or higher**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher**: [Download Node.js](https://nodejs.org/)
- **Git**: [Download Git](https://git-scm.com/downloads)

### Optional
- **PostgreSQL**: For production use (SQLite is fine for development)
- **VS Code**: Recommended code editor

## 🔧 Step-by-Step Setup

### Step 1: Clone or Setup the Project

If you have the project files:
```bash
cd Store_management
```

If starting fresh, create the directory structure as shown in the README.

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory
```bash
cd backend
```

#### 2.2 Create Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 2.3 Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- JWT libraries
- Pandas
- And more...

#### 2.4 Create Environment File

Create a `.env` file in the `backend` directory:

**For Development (SQLite):**
```env
DATABASE_URL=sqlite:///./rms.db
SECRET_KEY=dev-secret-key-change-in-production-123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**For Production (PostgreSQL):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/rms_db
SECRET_KEY=your-super-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

⚠️ **Important**: Generate a strong SECRET_KEY for production:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 2.5 Initialize the Database

The database will be created automatically when you first run the application.

Create an initialization script `backend/init_db.py`:

```python
from app.db.database import engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash
from app.db.models import UserRole

# Create tables
models.Base.metadata.create_all(bind=engine)

# Create default admin user
db = SessionLocal()

# Check if admin exists
admin = db.query(models.User).filter(models.User.username == "admin").first()

if not admin:
    # Create default store
    store = models.Store(
        name="Main Store",
        address="123 Main Street",
        phone="+1234567890",
        email="store@example.com"
    )
    db.add(store)
    db.flush()
    
    # Create admin user
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
    db.commit()
    print("✅ Database initialized successfully!")
    print("Admin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("⚠️  PLEASE CHANGE THE PASSWORD IMMEDIATELY!")
else:
    print("ℹ️  Database already initialized")

db.close()
```

Run the initialization:
```bash
python init_db.py
```

#### 2.6 Start the Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ Backend is now running!

**Test it**: Open http://localhost:8000/docs in your browser to see the API documentation.

### Step 3: Frontend Setup

Open a **new terminal window** (keep the backend running).

#### 3.1 Navigate to Frontend Directory
```bash
cd frontend
```

#### 3.2 Install Node Dependencies
```bash
npm install
```

This will install:
- React
- TypeScript
- Tailwind CSS
- React Router
- Axios
- And more...

#### 3.3 Start the Development Server
```bash
npm run dev
```

You should see:
```
VITE v5.0.8  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

✅ Frontend is now running!

**Test it**: Open http://localhost:3000 in your browser.

### Step 4: First Login

1. Navigate to http://localhost:3000
2. You should see the login page
3. Enter the default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
4. Click "Login"

You should now see the dashboard! 🎉

## 🔒 Post-Setup Security

### Important: Change Default Password

1. Log in with default credentials
2. Navigate to your profile or settings
3. Change the password immediately

Or use the API:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/change-password" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "admin123",
    "new_password": "your-new-secure-password"
  }'
```

### Generate Secure SECRET_KEY

For production, always generate a new secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update your `.env` file with this key.

## 📊 Adding Sample Data

To test the system with sample data, you can create additional users, products, and customers.

### Create Sample Users

Access the Users page (logged in as admin) and add:
- Store Manager
- Sales Staff
- Accounts user

### Create Sample Products

Access the Inventory page and add some products:
- Product name
- SKU
- Price
- Initial stock
- Category

### Create Sample Customers

Access the Customers page and add customer profiles.

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

**Issue**: `Database connection error`
**Solution**: Check your `DATABASE_URL` in `.env` file

**Issue**: `Port 8000 already in use`
**Solution**: Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**Issue**: `npm install` fails
**Solution**: Try clearing npm cache:
```bash
npm cache clean --force
npm install
```

**Issue**: `Cannot connect to API`
**Solution**: Check that backend is running on port 8000

**Issue**: `Port 3000 already in use`
**Solution**: The dev server will prompt you to use a different port, or you can specify:
```bash
npm run dev -- --port 3001
```

### Common Errors

**CORS Error**
- Backend and frontend are configured to work together
- If you change ports, update the CORS settings in `backend/app/main.py`

**Authentication Error**
- Make sure you're using the correct credentials
- Check that the database was initialized properly
- Token might be expired, try logging in again

## 🔄 Updating the Application

### Update Backend
```bash
cd backend
git pull  # if using git
pip install -r requirements.txt
```

### Update Frontend
```bash
cd frontend
git pull  # if using git
npm install
```

## 🚀 Production Deployment

### Backend Production Setup

1. Use PostgreSQL instead of SQLite
2. Set strong SECRET_KEY
3. Disable debug mode
4. Use a production ASGI server (Gunicorn + Uvicorn)
5. Set up HTTPS
6. Configure firewall rules

### Frontend Production Build

```bash
cd frontend
npm run build
```

Serve the `dist` folder with a web server (Nginx, Apache, etc.)

## 📞 Getting Help

If you encounter issues:

1. Check this guide again
2. Review the README.md
3. Check the API documentation at http://localhost:8000/docs
4. Look for error messages in the terminal
5. Create an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version, Node version)

## ✅ Checklist

Before you start using the system:

- [ ] Backend running successfully
- [ ] Frontend running successfully
- [ ] Can access login page
- [ ] Can log in with default credentials
- [ ] Changed default admin password
- [ ] Created at least one store
- [ ] Added sample products
- [ ] Tested creating a sale
- [ ] Generated a report

---

**Congratulations!** 🎉 Your Retail Management System is now set up and running!

