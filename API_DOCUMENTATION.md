# API Documentation

Complete API reference for the Retail Management System.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All endpoints except `/auth/login` require authentication using JWT Bearer tokens.

### Request Headers
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

## 🔐 Authentication Endpoints

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "full_name": "System Administrator",
    "role": "super_admin",
    "store_id": 1,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Get Current User
```http
GET /auth/me
```

**Response:** User object

### Change Password
```http
POST /auth/change-password
```

**Request Body:**
```json
{
  "old_password": "admin123",
  "new_password": "newpassword123"
}
```

## 👥 User Management Endpoints

### List Users
```http
GET /users/
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:** Array of User objects

### Create User
```http
POST /users/
```

**Required Role:** Super Admin

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "password123",
  "role": "sales_staff",
  "store_id": 1
}
```

### Get User by ID
```http
GET /users/{user_id}
```

### Update User
```http
PUT /users/{user_id}
```

**Required Role:** Super Admin

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "role": "store_manager",
  "is_active": true
}
```

### Delete User
```http
DELETE /users/{user_id}
```

**Required Role:** Super Admin

## 📦 Inventory Management Endpoints

### List Products
```http
GET /inventory/products
```

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Records per page
- `store_id` (int): Filter by store
- `low_stock` (bool): Show only low stock items

**Response:**
```json
[
  {
    "id": 1,
    "sku": "PROD001",
    "name": "Product Name",
    "description": "Product description",
    "category": "Electronics",
    "brand": "Brand Name",
    "unit_price": 999.99,
    "cost_price": 750.00,
    "gst_rate": 18.0,
    "image_url": "https://example.com/image.jpg",
    "warranty_months": 12,
    "current_stock": 50,
    "minimum_stock": 10,
    "store_id": 1,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### Create Product
```http
POST /inventory/products
```

**Required Role:** Store Manager or Admin

**Request Body:**
```json
{
  "sku": "PROD001",
  "name": "Product Name",
  "description": "Product description",
  "category": "Electronics",
  "brand": "Brand Name",
  "unit_price": 999.99,
  "cost_price": 750.00,
  "gst_rate": 18.0,
  "warranty_months": 12,
  "current_stock": 50,
  "minimum_stock": 10,
  "store_id": 1
}
```

### Update Product
```http
PUT /inventory/products/{product_id}
```

### Get Inventory Dashboard
```http
GET /inventory/dashboard
```

**Response:**
```json
{
  "total_products": 150,
  "low_stock_products": 12,
  "out_of_stock_products": 3,
  "total_stock_value": 150000.00
}
```

### Create Batch
```http
POST /inventory/batches
```

**Request Body:**
```json
{
  "batch_id": "BATCH001",
  "product_id": 1,
  "quantity": 100,
  "serial_numbers": "SN001,SN002,SN003",
  "manufacturing_date": "2024-01-01T00:00:00",
  "expiry_date": "2025-01-01T00:00:00"
}
```

### List Batches
```http
GET /inventory/batches
```

**Query Parameters:**
- `product_id` (int): Filter by product

## 🛒 Sales Endpoints

### Create Sale
```http
POST /sales/
```

**Request Body:**
```json
{
  "customer_id": 1,
  "store_id": 1,
  "payment_mode": "cash",
  "discount": 50.00,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 999.99,
      "serial_number": "SN001"
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "invoice_number": "INV120240101001",
  "customer_id": 1,
  "store_id": 1,
  "subtotal": 1999.98,
  "gst_amount": 359.996,
  "discount": 50.00,
  "total_amount": 2309.976,
  "payment_mode": "cash",
  "payment_status": "completed",
  "sale_date": "2024-01-01T12:00:00",
  "items": [...]
}
```

### List Sales
```http
GET /sales/
```

**Query Parameters:**
- `skip` (int): Pagination
- `limit` (int): Records per page
- `store_id` (int): Filter by store
- `customer_id` (int): Filter by customer
- `start_date` (datetime): Start date filter
- `end_date` (datetime): End date filter

### Get Sale by ID
```http
GET /sales/{sale_id}
```

### Daily Sales Statistics
```http
GET /sales/stats/daily
```

**Query Parameters:**
- `date` (datetime): Specific date (default: today)
- `store_id` (int): Filter by store

**Response:**
```json
{
  "date": "2024-01-01T00:00:00",
  "total_sales": 15000.00,
  "total_transactions": 45,
  "cash_sales": 5000.00,
  "card_sales": 6000.00,
  "upi_sales": 3000.00,
  "qr_code_sales": 1000.00
}
```

### Monthly Sales Statistics
```http
GET /sales/stats/monthly
```

**Query Parameters:**
- `month` (int): Month (1-12)
- `year` (int): Year
- `store_id` (int): Filter by store

### Sales Dashboard
```http
GET /sales/dashboard/stats
```

**Response:**
```json
{
  "today_sales": 5000.00,
  "today_transactions": 15,
  "month_sales": 150000.00,
  "month_transactions": 450,
  "average_transaction_value": 333.33
}
```

## 👤 Customer Management Endpoints

### List Customers
```http
GET /customers/
```

**Query Parameters:**
- `skip` (int): Pagination
- `limit` (int): Records per page
- `store_id` (int): Filter by store
- `search` (string): Search by name or phone

### Create Customer
```http
POST /customers/
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "gst_number": "GST123456",
  "store_id": 1
}
```

### Get Customer Details
```http
GET /customers/{customer_id}
```

### Get Purchase History
```http
GET /customers/{customer_id}/purchase-history
```

**Response:**
```json
{
  "customer": {...},
  "total_purchases": 5000.00,
  "purchase_count": 15,
  "recent_purchases": [...],
  "active_warranties": [
    {
      "product_id": 1,
      "product_name": "Product Name",
      "serial_number": "SN001",
      "purchase_date": "2024-01-01T00:00:00",
      "warranty_expires_at": "2025-01-01T00:00:00",
      "invoice_number": "INV001"
    }
  ]
}
```

### Update Customer
```http
PUT /customers/{customer_id}
```

### Delete Customer
```http
DELETE /customers/{customer_id}
```

## 💰 Financial Management Endpoints

### Create Expense
```http
POST /financial/expenses
```

**Request Body:**
```json
{
  "store_id": 1,
  "category": "petty_cash",
  "description": "Office supplies",
  "amount": 500.00,
  "payment_mode": "cash",
  "vendor_name": "Vendor Name",
  "receipt_number": "RCP001",
  "expense_date": "2024-01-01T00:00:00"
}
```

### List Expenses
```http
GET /financial/expenses
```

**Query Parameters:**
- `skip` (int): Pagination
- `limit` (int): Records per page
- `store_id` (int): Filter by store
- `category` (string): Filter by category
- `start_date` (datetime): Start date
- `end_date` (datetime): End date

### Get Expense by ID
```http
GET /financial/expenses/{expense_id}
```

### Update Expense
```http
PUT /financial/expenses/{expense_id}
```

**Required Role:** Store Manager or Admin

### Delete Expense
```http
DELETE /financial/expenses/{expense_id}
```

**Required Role:** Store Manager or Admin

### Daily Closing Report
```http
GET /financial/daily-closing
```

**Query Parameters:**
- `date` (datetime): Specific date (default: today)
- `store_id` (int): Filter by store

**Response:**
```json
{
  "date": "2024-01-01T00:00:00",
  "total_sales": 15000.00,
  "cash_collected": 5000.00,
  "card_collected": 6000.00,
  "upi_collected": 3000.00,
  "qr_code_collected": 1000.00,
  "total_expenses": 2000.00,
  "net_cash_in_hand": 3000.00,
  "total_transactions": 45
}
```

### Financial Dashboard
```http
GET /financial/dashboard/stats
```

**Response:**
```json
{
  "today_revenue": 5000.00,
  "today_expenses": 500.00,
  "today_profit": 4500.00,
  "month_revenue": 150000.00,
  "month_expenses": 15000.00,
  "month_profit": 135000.00
}
```

## 📊 Reports Endpoints

### Download Sales Report
```http
GET /reports/sales/excel
```

**Query Parameters:**
- `start_date` (datetime): Start date
- `end_date` (datetime): End date
- `store_id` (int): Filter by store

**Response:** Excel file download

### Download Inventory Report
```http
GET /reports/inventory/excel
```

**Query Parameters:**
- `store_id` (int): Filter by store

**Response:** Excel file download

### Download Expenses Report
```http
GET /reports/expenses/excel
```

**Query Parameters:**
- `start_date` (datetime): Start date
- `end_date` (datetime): End date
- `store_id` (int): Filter by store

**Response:** Excel file download

### Download Customers Report
```http
GET /reports/customers/excel
```

**Query Parameters:**
- `store_id` (int): Filter by store

**Response:** Excel file download

## 🔒 Role-Based Access Control

### Permission Matrix

| Endpoint | Super Admin | Store Manager | Sales Staff | Accounts | Marketing |
|----------|-------------|---------------|-------------|----------|-----------|
| Create User | ✅ | ❌ | ❌ | ❌ | ❌ |
| View Users | ✅ | ✅ | ❌ | ❌ | ❌ |
| Manage Inventory | ✅ | ✅ | ❌ | ❌ | ❌ |
| Create Sale | ✅ | ✅ | ✅ | ❌ | ❌ |
| View Sales | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage Customers | ✅ | ✅ | ✅ | ❌ | ✅ |
| Manage Expenses | ✅ | ✅ | ❌ | ✅ | ❌ |
| Generate Reports | ✅ | ✅ | ❌ | ✅ | ✅ |

## 🚨 Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## 📝 Notes

- All datetime values are in ISO 8601 format
- Amounts are in decimal format with 2 decimal places
- Phone numbers should include country code
- GST rates are in percentage (e.g., 18.0 for 18%)
- Pagination default: skip=0, limit=100

## 🔗 Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

Visit `http://localhost:8000/redoc` for alternative documentation view.

