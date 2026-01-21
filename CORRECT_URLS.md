# 🌐 Correct URLs for Your RMS Application

## ⚠️ IMPORTANT: Use These URLs

### ✅ Frontend Application
**URL:** http://localhost:5173

**NOT:** ~~http://localhost:3002~~ ❌

### ✅ Backend API
**URL:** http://localhost:8000

### ✅ API Documentation (Swagger)
**URL:** http://localhost:8000/docs

---

## 🚀 Quick Start Steps

1. **Wait 10-15 seconds** for the frontend server to fully start (check the new CMD window that opened)

2. **Open your browser** and go to:
   ```
   http://localhost:5173
   ```

3. **Login** with these credentials:
   - **Email:** admin@example.com
   - **Password:** admin123

4. **Click "Marketing"** in the left sidebar (📢 Megaphone icon)

5. **Explore** the 8 sample marketing campaigns!

---

## 🔍 Troubleshooting

### If you see a blank page:
- ✅ Make sure you're using **http://localhost:5173** (NOT 3002)
- ✅ Check the CMD window to see if Vite is running
- ✅ Look for a message like "Local: http://localhost:5173/"
- ✅ Wait a few more seconds for the dev server to start

### If you get connection errors:
- ✅ Check both CMD windows are open (backend and frontend)
- ✅ Backend should show "Uvicorn running on http://0.0.0.0:8000"
- ✅ Frontend should show "Local: http://localhost:5173/"

### Default Login Credentials:
- **Super Admin:**
  - Email: admin@example.com
  - Password: admin123

- **Store Manager:**
  - Email: manager@example.com
  - Password: manager123

---

## 📊 What You'll See

### Dashboard (Home Page)
- 4 KPI cards (Sales, Revenue, Customers, Products)
- 6 interactive charts:
  - Weekly Sales Trend
  - Sales by Category
  - Revenue vs Expenses
  - Payment Methods
  - Monthly Performance
  - Real-time metrics

### Marketing Page (NEW!)
- 5 Marketing KPI cards
- 8 Sample campaigns
- Create Campaign button
- Filter by status
- Campaign analytics

---

## 🎯 Pages Available

1. **Dashboard** - `/` - Overview with charts
2. **Inventory** - `/inventory` - Product management
3. **Sales** - `/sales` - POS and sales history
4. **Customers** - `/customers` - Customer management
5. **Financial** - `/financial` - Expense tracking
6. **Marketing** - `/marketing` - Campaign automation ✨ NEW
7. **Reports** - `/reports` - Analytics and reports
8. **Users** - `/users` - User management (Admin only)

---

## 💡 Remember

**Always use:** http://localhost:5173

**Port 5173** = Frontend (React/Vite)
**Port 8000** = Backend (FastAPI)

---

Happy Testing! 🚀

