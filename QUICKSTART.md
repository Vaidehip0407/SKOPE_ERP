# Quick Start Guide

Get your Retail Management System up and running in 5 minutes!

## ⚡ Quick Setup (5 Minutes)

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start server
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

### Step 2: Frontend Setup (3 minutes)

Open a **new terminal**:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: http://localhost:3000

### Step 3: Login

Open http://localhost:3000 in your browser

**Login credentials:**
- Username: `admin`
- Password: `admin123`

🎉 **You're all set!** Start exploring the dashboard.

## 🎯 What to Do Next

### 1. Add Your First Product
1. Go to **Inventory** → Click **Add Product**
2. Fill in product details (SKU, name, price, stock)
3. Click **Save**

### 2. Create a Customer
1. Go to **Customers** → Click **Add Customer**
2. Enter customer details (name, phone, email)
3. Click **Save**

### 3. Make Your First Sale
1. Go to **Sales** → Click **New Sale**
2. Select customer (optional)
3. Add products to cart
4. Select payment method
5. Complete the sale

### 4. View Reports
1. Go to **Reports**
2. Download any report (Sales, Inventory, etc.)
3. Reports are exported as Excel files

## 🔐 Security Note

⚠️ **Important**: Change the default password immediately!

1. Click on your profile
2. Select "Change Password"
3. Enter new secure password

## 📱 Features Overview

| Feature | Description |
|---------|-------------|
| **Dashboard** | Real-time sales, inventory, and financial metrics |
| **Inventory** | Product catalog, stock levels, batch tracking |
| **Sales/POS** | Create sales, manage transactions, invoices |
| **Customers** | Customer database, purchase history, warranties |
| **Financial** | Expenses, revenue tracking, daily closing |
| **Reports** | Export data in Excel format |
| **Users** | Manage staff accounts and permissions |

## 🎨 User Roles

### Super Admin (admin/admin123)
- Full system access
- Can create/manage users
- Can manage all stores

### Store Manager (manager/manager123)
- Store operations
- Inventory management
- Staff management (limited)

### Sales Staff (sales/sales123)
- POS operations
- Customer management
- View inventory

## 🆘 Quick Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
# On Windows:
netstat -ano | findstr :8000

# On macOS/Linux:
lsof -i :8000

# Use different port:
uvicorn app.main:app --reload --port 8001
```

### Frontend won't start?
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Can't login?
```bash
# Reinitialize database
cd backend
python init_db.py
```

## 📚 Documentation

- **Full Setup Guide**: See `SETUP_GUIDE.md`
- **API Documentation**: http://localhost:8000/docs
- **Deployment Guide**: See `DEPLOYMENT.md`
- **README**: See `README.md`

## 💡 Pro Tips

1. **Keyboard Shortcuts**: Most forms support Tab navigation
2. **Search**: Use search boxes to quickly find products/customers
3. **Filters**: Click filters to view specific data (e.g., low stock items)
4. **Export**: All reports can be exported to Excel
5. **Responsive**: Works on desktop, tablet, and mobile

## 🔄 Daily Workflow

### Morning Routine
1. Check Dashboard for yesterday's summary
2. Review low stock alerts
3. Check daily sales target

### During the Day
1. Create sales as transactions occur
2. Add new customers
3. Update inventory as needed

### Evening Routine
1. Generate daily closing report
2. Record cash in hand
3. Review expenses

## 📞 Need Help?

- **API Docs**: http://localhost:8000/docs
- **Check Logs**: Backend terminal shows detailed errors
- **Browser Console**: Press F12 to see frontend errors
- **Documentation**: Read the complete guides in the project

## 🎓 Learning Path

1. **Day 1**: Explore dashboard, create products
2. **Day 2**: Create customers, make test sales
3. **Day 3**: Add expenses, generate reports
4. **Day 4**: Manage users, configure settings
5. **Day 5**: Start using for real transactions

## ⚙️ Default Configuration

- **Database**: SQLite (stored in `backend/rms.db`)
- **Backend Port**: 8000
- **Frontend Port**: 3000
- **Session Timeout**: 30 minutes
- **Currency**: INR (₹)
- **GST Default**: 18%

## 🚀 Going to Production

When ready for production:

1. Change all default passwords
2. Use PostgreSQL instead of SQLite
3. Generate new SECRET_KEY
4. Enable HTTPS
5. Set up backups
6. See `DEPLOYMENT.md` for details

---

**Happy Selling!** 🛍️

Need more help? Check out the full documentation or create an issue on GitHub.

