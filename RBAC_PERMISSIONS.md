# 🔐 Role-Based Access Control (RBAC) - SKOPE ERP

## Roles Hierarchy

```
Super Admin (Full System Access)
    ↓
Store Manager (Store-level Management)
    ↓
Staff (Sales Staff, Marketing, Accounts - Limited Access)
```

---

## 📊 Permissions Matrix

| Feature | Super Admin | Store Manager | Sales Staff | Marketing | Accounts |
|---------|------------|---------------|-------------|-----------|----------|
| **USERS** |
| View Users | ✅ All Users | ✅ Store Users | ❌ | ❌ | ❌ |
| Create User | ✅ All Roles | ✅ Staff Only | ❌ | ❌ | ❌ |
| Edit User | ✅ | ✅ Store Users | ❌ | ❌ | ❌ |
| Delete User | ✅ | ✅ Store Users | ❌ | ❌ | ❌ |
| Change Roles | ✅ | ❌ | ❌ | ❌ | ❌ |
| **STORES** |
| View All Stores | ✅ | ❌ | ❌ | ❌ | ❌ |
| Create Store | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Store | ✅ | ✅ Own Store | ❌ | ❌ | ❌ |
| **INVENTORY** |
| View Products | ✅ | ✅ | ✅ | ❌ | ✅ |
| Add Product | ✅ | ✅ | ❌ | ❌ | ❌ |
| Edit Product | ✅ | ✅ | ❌ | ❌ | ❌ |
| Delete Product | ✅ | ✅ | ❌ | ❌ | ❌ |
| Update Stock | ✅ | ✅ | ❌ | ❌ | ❌ |
| **SALES** |
| View Sales | ✅ All | ✅ Store Sales | ✅ Own Sales | ❌ | ✅ |
| Create Sale | ✅ | ✅ | ✅ | ❌ | ❌ |
| View Sale Details | ✅ | ✅ | ✅ Own | ❌ | ✅ |
| Delete Sale | ✅ | ✅ | ❌ | ❌ | ❌ |
| **CUSTOMERS** |
| View Customers | ✅ All | ✅ Store Customers | ✅ Store Customers | ✅ Store Customers | ✅ Store Customers |
| Add Customer | ✅ | ✅ | ✅ | ✅ | ❌ |
| Edit Customer | ✅ | ✅ | ✅ | ✅ | ❌ |
| Delete Customer | ✅ | ✅ | ❌ | ❌ | ❌ |
| **FINANCIAL** |
| View Expenses | ✅ All | ✅ Store Expenses | ❌ | ❌ | ✅ Store Expenses |
| Add Expense | ✅ | ✅ | ❌ | ❌ | ✅ |
| Edit Expense | ✅ | ✅ | ❌ | ❌ | ✅ |
| Delete Expense | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Financial Reports | ✅ All | ✅ Store | ❌ | ❌ | ✅ Store |
| **MARKETING** |
| View Campaigns | ✅ All | ✅ Store Campaigns | ❌ | ✅ Store Campaigns | ❌ |
| Create Campaign | ✅ | ✅ | ❌ | ✅ | ❌ |
| Edit Campaign | ✅ | ✅ | ❌ | ✅ | ❌ |
| Delete Campaign | ✅ | ✅ | ❌ | ✅ | ❌ |
| View Analytics | ✅ All | ✅ Store | ❌ | ✅ Store | ❌ |
| **REPORTS** |
| Sales Reports | ✅ All | ✅ Store | ✅ Own | ❌ | ✅ Store |
| Inventory Reports | ✅ All | ✅ Store | ❌ | ❌ | ✅ Store |
| Customer Reports | ✅ All | ✅ Store | ❌ | ✅ Store | ✅ Store |
| Financial Reports | ✅ All | ✅ Store | ❌ | ❌ | ✅ Store |
| GST/Tax Reports | ✅ All | ✅ Store | ❌ | ❌ | ✅ Store |
| **DASHBOARD** |
| View Dashboard | ✅ All Data | ✅ Store Data | ✅ Limited | ✅ Marketing | ✅ Financial |

---

## 🎯 Key Differences

### Super Admin
- **Access:** ALL stores, ALL data
- **Can:** Create stores, create store managers, view all analytics
- **Scope:** System-wide

### Store Manager
- **Access:** ONLY their store's data
- **Can:** Manage inventory, sales, staff, expenses, customers for their store
- **Cannot:** View other stores, create store managers, change user roles
- **Scope:** Store-level

### Sales Staff
- **Access:** View products, create sales, view customers
- **Can:** Make sales, add customers
- **Cannot:** Manage inventory, view expenses, delete anything
- **Scope:** Operational

### Marketing Staff
- **Access:** Customers, campaigns, marketing analytics
- **Can:** Create campaigns, view customer data, manage marketing
- **Cannot:** View sales details, manage inventory, view expenses
- **Scope:** Marketing-focused

### Accounts Staff
- **Access:** Financial data, expenses, reports
- **Can:** Add expenses, view financial reports
- **Cannot:** Make sales, manage inventory, delete data
- **Scope:** Finance-focused

---

## 🔒 Security Rules

1. **Data Isolation:** Users can only see data from their store (except Super Admin)
2. **Hierarchical:** Super Admin > Store Manager > Staff
3. **No Lateral Movement:** Sales Staff cannot access Marketing features, etc.
4. **Audit Trail:** All actions are logged with user_id and timestamp
5. **Store Binding:** All data is linked to store_id

---

## 🚫 Common Restrictions

### Store Manager CANNOT:
- ❌ View other stores' data
- ❌ Create or delete stores
- ❌ Change user roles
- ❌ Access system-wide analytics
- ❌ Create Super Admin or Store Manager users

### Sales Staff CANNOT:
- ❌ View or edit expenses
- ❌ Delete products or sales
- ❌ View financial reports
- ❌ Manage users
- ❌ View profit/cost data

### Marketing Staff CANNOT:
- ❌ View sales amounts or financial data
- ❌ Manage inventory
- ❌ View expenses
- ❌ Make sales transactions

### Accounts Staff CANNOT:
- ❌ Make sales
- ❌ Manage inventory
- ❌ Delete any records
- ❌ Manage marketing campaigns

---

## 📱 Frontend Visibility

Based on role, the UI should show/hide:

### Super Admin - Sees Everything
- All menu items
- All stores selector
- System-wide analytics

### Store Manager - Limited to Store
- ❌ Store selector (auto-set to their store)
- ✅ All store management features
- ❌ System settings

### Sales Staff - Minimal UI
- ✅ Dashboard (sales view)
- ✅ Sales (create, view own)
- ✅ Customers (view, add)
- ❌ Inventory management
- ❌ Financial
- ❌ Marketing
- ❌ Reports
- ❌ Users

### Marketing Staff
- ✅ Dashboard (marketing view)
- ✅ Customers (full access)
- ✅ Marketing (full access)
- ❌ Sales (no amounts)
- ❌ Inventory
- ❌ Financial
- ❌ Users

### Accounts Staff
- ✅ Dashboard (financial view)
- ✅ Financial (full access)
- ✅ Reports (financial, GST)
- ❌ Sales (create)
- ❌ Marketing
- ❌ Users

---

## 🎨 UI Indicators

Show user's role prominently:
- Badge color: Super Admin (Gold), Store Manager (Blue), Staff (Gray)
- Sidebar shows only allowed menu items
- Buttons show/hide based on permissions
- Tooltips explain why actions are disabled

---

## 🔧 Implementation Checklist

- [ ] Apply `require_role()` to all API endpoints
- [ ] Add store_id filtering for non-Super Admin users
- [ ] Hide menu items based on role in frontend
- [ ] Show role badge in user profile
- [ ] Test each role thoroughly
- [ ] Create demo users for each role
- [ ] Document permission errors clearly

---

This ensures proper security and clear separation of duties!

