# 🏪 Multi-Store Management - Complete Guide

## ✅ NEW FEATURE ADDED!

Super Admin can now:
1. ✅ Create and manage multiple stores
2. ✅ View consolidated data from all stores
3. ✅ Switch between stores to see individual store dashboards
4. ✅ View store-wise statistics and analytics

---

## 📦 What Was Added:

### Backend:
1. **Store Management API** (`backend/app/api/v1/stores.py`):
   - POST `/api/v1/stores/` - Create new store
   - GET `/api/v1/stores/` - List all stores
   - GET `/api/v1/stores/stats` - Get statistics for all stores
   - GET `/api/v1/stores/{id}` - Get specific store
   - PUT `/api/v1/stores/{id}` - Update store
   - DELETE `/api/v1/stores/{id}` - Deactivate store

2. **Store Schemas** (`backend/app/schemas/store.py`):
   - StoreCreate
   - StoreUpdate
   - StoreResponse
   - StoreStats

### Frontend:
1. **Stores Management Page** (`frontend/src/pages/Stores.tsx`):
   - Create new stores
   - Edit existing stores
   - View store statistics
   - Deactivate stores
   - Grid view with cards

2. **Store Selector on Dashboard**:
   - Dropdown showing all stores
   - "All Stores (Consolidated)" option
   - Individual store selection

3. **Navigation Update**:
   - New "Stores" menu item (Super Admin only)
   - Icon: 🏪 Building Storefront

---

## 🎯 How to Use:

### As Super Admin:

#### 1. View Stores Management:
1. Login as `admin` / `admin123`
2. Click **"Stores"** in the sidebar (second item)
3. You'll see:
   - Overview cards (Total Stores, Revenue, Products, Users)
   - Grid of existing stores with stats
   - "Add New Store" button

#### 2. Create a New Store:
1. Click **"Add New Store"** button
2. Fill in the form:
   - **Store Name*** (required)
   - Address
   - Phone
   - Email
   - GST Number
3. Click **"Create Store"**
4. Store appears in the grid

#### 3. Edit a Store:
1. Find the store card
2. Click the **pencil icon** (Edit button)
3. Update the information
4. Click **"Update Store"**

#### 4. View Store Statistics:
Each store card shows:
- **Products:** Total products in that store
- **Revenue:** Total sales revenue
- **Customers:** Total customers
- **Users:** Total staff/users

#### 5. Switch Between Stores on Dashboard:
1. Go to **Dashboard**
2. See dropdown in top-right: **"View Store:"**
3. Options:
   - **📊 All Stores (Consolidated)** - Shows combined data from all stores
   - **🏪 [Store Name]** - Shows data for that specific store only
4. Select any option and dashboard updates

#### 6. Consolidated vs Individual View:
- **All Stores:** Sum of all metrics across all stores
- **Individual Store:** Data specific to that store only
  - Products from that store
  - Sales from that store
  - Customers from that store
  - Financial data from that store

---

## 🔒 Permissions:

### Super Admin Only:
- ✅ Can see "Stores" menu
- ✅ Can create stores
- ✅ Can edit stores
- ✅ Can deactivate stores
- ✅ Can view all stores in dashboard dropdown
- ✅ Can switch between stores

### Store Manager:
- ❌ Cannot see "Stores" menu
- ❌ Cannot create stores
- ❌ Cannot switch stores (only see their own)
- ✅ Can manage their own store's data

### Other Roles (Sales, Marketing, Accounts):
- ❌ Cannot see "Stores" menu
- ❌ Cannot create/edit stores
- ❌ Cannot switch stores
- ✅ Can only see their store's data

---

## 📊 Store Management Page Features:

### Overview Cards:
1. **Total Stores** - Count of active stores
2. **Total Revenue** - Sum of revenue from all stores
3. **Total Products** - Sum of products across all stores
4. **Total Users** - Sum of users across all stores

### Store Cards:
Each card displays:
- **Header:**
  - Store icon
  - Store name
  - Active/Inactive badge
  - Edit button
  - Delete button

- **Contact Details:**
  - 📍 Address
  - 📞 Phone
  - ✉️ Email
  - GST Number

- **Statistics:**
  - Products count
  - Revenue (in ₹)
  - Customers count
  - Users count

---

## 🎨 Visual Design:

### Store Management Page:
- Modern card-based grid layout
- Color-coded overview cards
- Responsive design (mobile-friendly)
- Gradient backgrounds
- Hover effects

### Dashboard Store Selector:
- Clean dropdown in top-right
- Clear labels: "📊 All Stores" vs "🏪 [Store Name]"
- Updates dashboard immediately on change
- Only visible to Super Admin

---

## 🧪 Testing:

### Test Store Creation:
1. Login as `admin` / `admin123`
2. Go to **Stores** page
3. Click **"Add New Store"**
4. Create a store:
   ```
   Name: Branch Store
   Address: 123 Market Street, City
   Phone: +91 98765 43210
   Email: branch@example.com
   GST: 22AAAAA0000A1Z5
   ```
5. Store should appear in grid

### Test Store Switching:
1. Go to **Dashboard**
2. Click **"View Store"** dropdown
3. Select **"All Stores (Consolidated)"**
4. Dashboard shows combined data
5. Select **specific store** (e.g., "Main Store")
6. Dashboard shows only that store's data

### Test Store Editing:
1. Go to **Stores** page
2. Click **pencil icon** on any store
3. Change the store name
4. Click **"Update Store"**
5. Name should update in the card

### Test Store Statistics:
1. Add products to different stores
2. Create sales in different stores
3. Go to **Stores** page
4. Each store card should show correct stats
5. Overview cards should show totals

---

## 🚀 Database Schema:

The `stores` table already exists with:
- `id` - Primary key
- `name` - Store name
- `address` - Store address
- `phone` - Contact phone
- `email` - Contact email
- `gst_number` - GST registration number
- `is_active` - Active/inactive flag
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

**Relationships:**
- `users` - Users belong to a store
- `products` - Products belong to a store
- `customers` - Customers belong to a store
- `sales` - Sales belong to a store
- `expenses` - Expenses belong to a store
- `campaigns` - Campaigns belong to a store

---

## 📝 API Endpoints:

### Create Store:
```http
POST /api/v1/stores/
Authorization: Bearer {super_admin_token}
Content-Type: application/json

{
  "name": "New Store",
  "address": "123 Street",
  "phone": "+91 1234567890",
  "email": "store@example.com",
  "gst_number": "22AAAAA0000A1Z5"
}
```

### Get All Stores:
```http
GET /api/v1/stores/
Authorization: Bearer {super_admin_token}
```

### Get Store Statistics:
```http
GET /api/v1/stores/stats
Authorization: Bearer {super_admin_token}
```

### Update Store:
```http
PUT /api/v1/stores/{store_id}
Authorization: Bearer {super_admin_token}
Content-Type: application/json

{
  "name": "Updated Name",
  "address": "New Address"
}
```

### Deactivate Store:
```http
DELETE /api/v1/stores/{store_id}
Authorization: Bearer {super_admin_token}
```

---

## ⚠️ Important Notes:

1. **Cannot Delete Store with Active Users:**
   - Must deactivate all users in that store first
   - Prevents data orphaning

2. **Soft Delete:**
   - Stores are deactivated, not deleted
   - Data remains in database
   - Can be reactivated if needed

3. **Default Store:**
   - "Main Store" is created during initialization
   - All existing data belongs to this store

4. **Store Filtering:**
   - Store Managers only see their store
   - Super Admin sees all stores
   - Dashboard respects selected store filter

---

## 🎯 Use Cases:

### Scenario 1: Retail Chain
- **Setup:** 5 stores in different cities
- **Super Admin:** Views consolidated revenue from all 5 stores
- **Benefit:** Central management with individual store visibility

### Scenario 2: Multi-Branch Operation
- **Setup:** Main store + 3 branch locations
- **Super Admin:** Creates separate dashboards for each branch
- **Benefit:** Compare performance across branches

### Scenario 3: Franchise Model
- **Setup:** Multiple franchise locations
- **Super Admin:** Manages all franchises centrally
- **Store Managers:** Each manages their own franchise
- **Benefit:** Hierarchical management with data isolation

---

## 🚀 Next Steps:

1. **Test the feature** using the guide above
2. **Create additional stores** if needed
3. **Assign users to different stores** via Users page
4. **View consolidated analytics** on dashboard
5. **Switch between stores** to see individual performance

---

## ✅ Summary:

**What You Can Now Do:**
- ✅ Create multiple stores
- ✅ Edit store information
- ✅ View store statistics
- ✅ See consolidated data from all stores
- ✅ Switch between stores on dashboard
- ✅ Manage store-wise operations

**What Changed:**
- ✅ New "Stores" menu item (Super Admin only)
- ✅ New Stores management page
- ✅ Store selector dropdown on dashboard
- ✅ API endpoints for store CRUD
- ✅ Role-based access control for stores

**The system now fully supports multi-store operations!** 🎉

