# 🔧 Fix: Dashboard Not Showing Data

## Problem
The dashboard is displaying but showing "₹" without values because the database is empty.

## Solution

### Option 1: Populate Database with Sample Data (Recommended)

Run this command in a **new terminal/command prompt**:

```bash
cd C:\Users\vrajr\Desktop\Store_management\backend
.\venv\Scripts\python.exe seed_data.py
```

This will add:
- ✅ Sample products (electronics, clothing, etc.)
- ✅ Sample customers
- ✅ Sample sales transactions
- ✅ Sample expenses
- ✅ Sample marketing campaigns

### Option 2: Add Data Manually

1. **Add Products:**
   - Go to "Inventory" page
   - Click "Add Product"
   - Fill in product details

2. **Add Customers:**
   - Go to "Customers" page
   - Click "Add Customer"
   - Fill in customer details

3. **Create Sales:**
   - Go to "Sales" page
   - Click "New Sale"
   - Add products and complete transaction

## After Running seed_data.py

1. **Refresh the Dashboard:**
   - Click the "🔄 Refresh Data" button on the dashboard
   - Or press F5 to reload the page

2. **You should now see:**
   - Today's Sales: ₹X,XXX
   - Today's Profit: ₹X,XXX
   - Total Products: XX
   - Stock Value: ₹XX,XXX
   - Charts with data

## Verification

Open browser console (F12) and check for:
- "Dashboard data loaded:" message with actual data
- No error messages

## Still Not Working?

If you still see "₹0" after running seed_data.py:

1. Check backend terminal for errors
2. Make sure backend is running on `http://localhost:8000`
3. Check browser console (F12) for API errors
4. Try logging out and logging back in
5. Clear browser cache and refresh

## Quick Test Commands

Test if backend is working:
```bash
# In browser, go to:
http://localhost:8000/docs

# Try these endpoints:
- GET /api/v1/inventory/dashboard
- GET /api/v1/sales/dashboard/stats
- GET /api/v1/financial/dashboard/stats
```

## Contact
If issue persists, provide:
- Backend terminal output
- Browser console errors (F12 → Console)
- Screenshot of dashboard


