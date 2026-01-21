# 🚀 SKOPE ERP - Complete Project Setup Guide

## Overview
SKOPE ERP is a comprehensive SaaS platform for retail operations management with integrated marketing automation, Meta/Google Ads integration, and multi-store support.

---

## 📋 Features

### Core Features
- ✅ **Multi-Store Management** - Manage multiple retail locations
- ✅ **Inventory Management** - Products, SKUs, batches, stock tracking
- ✅ **Sales & POS** - Invoice generation, multiple payment modes
- ✅ **Customer Management** - Customer database with purchase history
- ✅ **Financial Management** - Expense tracking, reports, GST
- ✅ **User Management** - Role-based access control (RBAC)

### Marketing Features
- ✅ **Marketing Campaigns** - WhatsApp, SMS, Email, Push Notifications
- ✅ **Campaign Automation** - Birthday, Festival, Warranty expiry triggers
- ✅ **Meta Ads Integration** - Facebook, Instagram, WhatsApp campaigns
- ✅ **Google Ads Integration** - Local search, Performance Max campaigns
- ✅ **Analytics & Reporting** - Campaign performance, ROAS tracking

### Advanced Features
- ✅ **Staff Performance** - Attendance, targets, incentives
- ✅ **Customer Segmentation** - Automated audience creation
- ✅ **Conversion Tracking** - Track sales from ads
- ✅ **Audit Logs** - Complete activity tracking

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (can be switched to PostgreSQL/MySQL)
- **JWT** - Authentication
- **Pydantic** - Data validation

### Frontend
- **React** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Zustand** - State management

### Integration APIs
- **Facebook Business SDK** - Meta Ads integration
- **Google Ads API** - Google Ads integration

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Quick Start (Recommended)

#### Option 1: Automated Setup (Windows)

1. **Open Command Prompt** in the project directory

2. **Run Backend Setup:**
```cmd
cd backend
QUICK_SETUP.bat
```

This will:
- Create virtual environment
- Install all Python packages
- Create and populate database with realistic data
- Start the backend server

3. **Open a New Terminal and Run Frontend:**
```cmd
cd frontend
npm install
npm run dev
```

4. **Access the Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

#### Option 2: Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

Windows:
```cmd
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Setup database with complete data:**
```bash
python setup_complete_database.py
```

6. **Start backend server:**
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

The frontend will be available at: http://localhost:5173

---

## 🔐 Default Login Credentials

The database comes pre-populated with the following users:

### 1. Super Admin (Full Access)
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Super Admin (All permissions)

### 2. Store Manager (Delhi)
- **Username:** `rajesh.kumar`
- **Password:** `manager123`
- **Role:** Store Manager (Delhi Store)

### 3. Store Manager (Mumbai)
- **Username:** `priya.sharma`
- **Password:** `manager123`
- **Role:** Store Manager (Mumbai Store)

### 4. Store Manager (Bangalore)
- **Username:** `amit.patel`
- **Password:** `manager123`
- **Role:** Store Manager (Bangalore Store)

### 5. Marketing Team
- **Username:** `marketing`
- **Password:** `marketing123`
- **Role:** Marketing (Campaign management)

### 6. Sales Staff
- **Username:** `vikram.singh`
- **Password:** `sales123`
- **Role:** Sales Staff (POS access)

### 7. Accounts
- **Username:** `accounts`
- **Password:** `accounts123`
- **Role:** Accounts (Financial access)

> ⚠️ **IMPORTANT:** Change these passwords immediately in production!

---

## 📊 Pre-Populated Data

The database includes realistic business data:

### Stores (3 stores)
- SKPOE Delhi Store
- SKPOE Mumbai Store
- SKPOE Bangalore Store

### Products (130+ products across all stores)
Categories:
- Electronics (Smartphones, Laptops, TVs, Cameras, Headphones)
- Clothing (Shoes, Jeans, T-shirts, Formal wear)
- Home & Kitchen (Appliances, Cookware, Storage)
- Sports & Fitness (Equipment, Accessories)
- Books & Stationery
- Beauty & Personal Care
- Food & Beverages

### Customers (78 customers)
- Complete contact information
- Purchase history
- Date of birth for birthday campaigns
- Loyalty points

### Sales Transactions (3600+ transactions)
- 60 days of sales history
- Multiple products per sale
- Various payment modes (Cash, Card, UPI, QR Code)
- GST calculations
- Discount tracking

### Expenses (360+ records)
- 60 days of expense data
- Categories: Rent, utilities, salaries, stock purchase, maintenance, marketing, etc.
- Vendor information
- Receipt tracking

### Marketing Campaigns (24 campaigns)
- Diwali Mega Sale
- Birthday Special (Automated)
- Weekend Flash Sale
- Warranty Expiry Reminders
- Win-Back Campaign
- New Year Sale
- Referral Program
- Purchase Anniversary

### Ad Integrations
- **Meta Ads:** Connected for all stores
- **Google Ads:** Connected for all stores
- **Ad Campaigns:** 15 active campaigns
- **Analytics Data:** 30 days of performance metrics

---

## 🎯 Key Features Guide

### 1. Dashboard
- Real-time sales overview
- Revenue analytics
- Top products
- Recent transactions

### 2. Inventory Management
- Add/Edit products
- Track stock levels
- Low stock alerts
- Batch management with serial numbers

### 3. Sales & POS
- Create invoices
- Multiple payment modes
- Customer selection
- Discount application
- GST calculation
- Print invoices with QR codes

### 4. Customer Management
- Customer database
- Purchase history
- Loyalty points
- Birthday tracking
- Customer segmentation

### 5. Marketing Campaigns
- Create WhatsApp/SMS/Email campaigns
- Automated triggers (Birthday, Festival, Warranty)
- Template management
- Campaign analytics
- Performance tracking

### 6. Meta & Google Ads
- Connect ad accounts
- Create campaigns from templates
- Target local audiences
- Track conversions
- ROI analysis

### 7. Financial Reports
- Sales reports
- Expense tracking
- Profit/Loss statements
- GST reports
- Custom date ranges

### 8. User Management
- Role-based access control
- Store assignment
- Activity logs
- Permission management

---

## 🔍 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user

#### Products
- `GET /api/v1/inventory/products` - List products
- `POST /api/v1/inventory/products` - Create product
- `GET /api/v1/inventory/products/{id}` - Get product
- `PUT /api/v1/inventory/products/{id}` - Update product

#### Sales
- `GET /api/v1/sales` - List sales
- `POST /api/v1/sales` - Create sale
- `GET /api/v1/sales/{id}` - Get sale
- `DELETE /api/v1/sales/{id}` - Delete sale

#### Customers
- `GET /api/v1/customers` - List customers
- `POST /api/v1/customers` - Create customer
- `GET /api/v1/customers/{id}` - Get customer

#### Marketing
- `GET /api/v1/campaigns` - List campaigns
- `POST /api/v1/campaigns` - Create campaign
- `GET /api/v1/campaigns/{id}/analytics` - Campaign analytics

---

## 🧪 Testing

### Quick Test Checklist

1. **Login Test:**
   - Open http://localhost:5173
   - Login with `admin` / `admin123`
   - Verify dashboard loads

2. **View Products:**
   - Navigate to Inventory
   - Verify products are displayed
   - Check stock levels

3. **Create Sale:**
   - Go to Sales
   - Click "New Sale"
   - Select customer and products
   - Complete transaction

4. **View Reports:**
   - Go to Reports
   - Check Sales Report
   - View Financial Summary

5. **Marketing Campaigns:**
   - Go to Marketing → Campaigns
   - View existing campaigns
   - Check campaign statistics

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=sqlite:///./rms.db
SECRET_KEY=your-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Database Configuration

The default configuration uses SQLite. To use PostgreSQL or MySQL:

1. Update `DATABASE_URL` in `.env`:
```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# MySQL
DATABASE_URL=mysql://user:password@localhost/dbname
```

2. Install database driver:
```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install pymysql
```

---

## 📱 Mobile Responsiveness

The frontend is fully responsive and works on:
- Desktop (1920x1080 and above)
- Laptop (1366x768)
- Tablet (768x1024)
- Mobile (375x667)

---

## 🛡️ Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- SQL injection protection (SQLAlchemy ORM)
- CORS configuration
- Input validation (Pydantic)
- Audit logging

---

## 📈 Scalability

### Current Setup
- SQLite database
- Single server deployment
- Suitable for 1-10 stores
- Handles 1000+ products
- Supports 10,000+ customers

### Production Scaling
- Switch to PostgreSQL/MySQL
- Add Redis for caching
- Deploy with Docker
- Use load balancer
- CDN for static assets
- Separate analytics database

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError`
- **Solution:** Make sure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt
```

**Problem:** Database connection error
- **Solution:** Delete `rms.db` and run setup again
```bash
del rms.db
python setup_complete_database.py
```

**Problem:** Port 8000 already in use
- **Solution:** Kill the process or use a different port
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**Problem:** `npm install` fails
- **Solution:** Clear npm cache and try again
```bash
npm cache clean --force
npm install
```

**Problem:** Build errors
- **Solution:** Delete `node_modules` and reinstall
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problem:** CORS errors
- **Solution:** Ensure backend is running and CORS is configured correctly in `app/main.py`

---

## 📝 Development

### Project Structure

```
Store_management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/          # API endpoints
│   │   ├── core/            # Config, security
│   │   ├── db/              # Database models
│   │   └── schemas/         # Pydantic schemas
│   ├── setup_complete_database.py
│   ├── requirements.txt
│   └── rms.db              # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── store/           # State management
│   │   ├── utils/           # Utilities
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
└── COMPLETE_PROJECT_SETUP.md (this file)
```

### Adding New Features

1. **Backend (API Endpoint):**
   - Add model in `backend/app/db/models.py`
   - Add schema in `backend/app/schemas/`
   - Add endpoint in `backend/app/api/v1/`
   - Update database with Alembic migration

2. **Frontend (UI Component):**
   - Add component in `frontend/src/components/`
   - Add page in `frontend/src/pages/`
   - Update routing in `App.tsx`
   - Add API calls in `utils/api.ts`

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 💬 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Email: support@skpoe.com
- Documentation: http://localhost:8000/docs

---

## 🎉 Congratulations!

Your SKOPE ERP system is now fully set up with:
- ✅ Complete database with realistic data
- ✅ 3 stores with full inventory
- ✅ 78 customers with purchase history
- ✅ 3600+ sales transactions
- ✅ 24 marketing campaigns
- ✅ Meta & Google Ads integrations
- ✅ 30 days of analytics data
- ✅ Multiple user roles and permissions

**Ready to start managing your retail empire! 🚀**

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [Meta Business SDK](https://developers.facebook.com/docs/business-sdk)
- [Google Ads API](https://developers.google.com/google-ads/api/docs/start)

---

**Version:** 1.0.0  
**Last Updated:** December 2024  
**Developed by:** SKPOE Development Team

