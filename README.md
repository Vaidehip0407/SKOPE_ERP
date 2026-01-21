# Retail Management System (RMS)

A comprehensive SaaS platform for retail operations management built with React and FastAPI.

## 🎯 Features

### Core Operations
- **Inventory Management**: Centralized product master database with SKU tracking, batch management, and real-time stock monitoring
- **Sales Dashboard**: Point of Sale (POS) system with barcode scanning capability and automated GST invoice generation
- **Customer Relationship Management**: Complete customer profiles with purchase history and warranty tracking
- **Financial Management**: Expense tracking, invoice management, and comprehensive financial reporting

### Security & Access Control
- Secure authentication with JWT tokens
- Role-based access control (Super Admin, Store Manager, Sales Staff, Marketing, Accounts)
- Audit logging for all critical operations
- Session management and password recovery

### Reporting & Analytics
- Real-time dashboard with key metrics
- Daily sales statistics and monthly cumulative tracking
- Export reports in Excel format
- Daily closing reports with cash reconciliation

## 🏗️ Technology Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL/SQLite**: Database (configurable)
- **JWT**: Secure authentication
- **Pandas**: Data processing for reports

### Frontend
- **React 18**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Navigation
- **Zustand**: State management
- **React Query**: Server state management
- **Axios**: HTTP client

## 📁 Project Structure

```
Store_management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── inventory.py
│   │   │   │   ├── sales.py
│   │   │   │   ├── customers.py
│   │   │   │   ├── financial.py
│   │   │   │   └── reports.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── customer.py
│   │   │   ├── sale.py
│   │   │   ├── financial.py
│   │   │   └── store.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Inventory.tsx
│   │   │   ├── Sales.tsx
│   │   │   ├── Customers.tsx
│   │   │   ├── Financial.tsx
│   │   │   ├── Reports.tsx
│   │   │   └── Users.tsx
│   │   ├── store/
│   │   │   └── authStore.ts
│   │   ├── utils/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (optional, SQLite works for development)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
DATABASE_URL=sqlite:///./rms.db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run the application:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 👤 Default Login Credentials

After first setup, create a super admin user by running the initialization script (see Database Initialization section).

Default credentials (after running init script):
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change these credentials immediately in production!

## 🎨 Design System

### Color Palette
- **Primary**: Navy Blue (#1D3557) - Headers, buttons
- **Secondary**: Light Gray (#A8DADC, #F1FAEE) - Backgrounds, tables
- **Accent**: Red (#E63946) - Critical data, alerts
- **Neutrals**: Blue-gray tones (#3D5A80, #98C1D9)

### Principles
- 60% neutrals, 30% primary/secondary, 10% accent colors
- WCAG AA accessibility compliant
- Mobile-first responsive design

## 🔐 User Roles

### Super Admin
- Full system access
- All stores management
- User management
- System configuration

### Store Manager
- Single store access
- Inventory management
- Sales operations
- Financial reports
- Staff management (limited)

### Sales Staff
- POS operations
- Customer management
- View inventory
- Create sales

### Accounts
- Financial reports
- Expense management
- Invoice management

### Marketing
- Customer data access
- Sales analytics
- Report generation

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/change-password` - Change password
- `GET /api/v1/auth/me` - Get current user

### Inventory
- `GET /api/v1/inventory/products` - List products
- `POST /api/v1/inventory/products` - Create product
- `PUT /api/v1/inventory/products/{id}` - Update product
- `GET /api/v1/inventory/dashboard` - Inventory dashboard stats

### Sales
- `GET /api/v1/sales/` - List sales
- `POST /api/v1/sales/` - Create sale
- `GET /api/v1/sales/{id}` - Get sale details
- `GET /api/v1/sales/stats/daily` - Daily sales stats
- `GET /api/v1/sales/stats/monthly` - Monthly sales stats

### Customers
- `GET /api/v1/customers/` - List customers
- `POST /api/v1/customers/` - Create customer
- `GET /api/v1/customers/{id}` - Get customer details
- `GET /api/v1/customers/{id}/purchase-history` - Purchase history

### Financial
- `GET /api/v1/financial/expenses` - List expenses
- `POST /api/v1/financial/expenses` - Create expense
- `GET /api/v1/financial/daily-closing` - Daily closing report

### Reports
- `GET /api/v1/reports/sales/excel` - Download sales report
- `GET /api/v1/reports/inventory/excel` - Download inventory report
- `GET /api/v1/reports/expenses/excel` - Download expenses report
- `GET /api/v1/reports/customers/excel` - Download customers report

## 🗄️ Database Schema

### Main Tables
- **users**: User accounts and authentication
- **stores**: Store information
- **products**: Product catalog
- **batches**: Batch tracking for inventory
- **customers**: Customer information
- **sales**: Sales transactions
- **sale_items**: Individual sale line items
- **expenses**: Expense tracking
- **audit_logs**: System audit trail

## 🔧 Configuration

### Backend Configuration
Edit `backend/app/core/config.py` or use environment variables:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Frontend Configuration
Edit `frontend/vite.config.ts` for proxy settings and build configuration.

## 📦 Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: support@rms-platform.com

## 🔄 Version History

### Version 1.0.0 (Current)
- Initial release
- Core inventory management
- Sales and POS system
- Customer management
- Financial tracking
- Report generation
- Role-based access control

## 🎯 Roadmap

### Upcoming Features
- Barcode scanning integration
- WhatsApp/SMS integration for receipts
- Multi-store support enhancements
- Advanced analytics and forecasting
- Mobile app (React Native)
- Offline mode support
- API rate limiting
- Advanced security features

---

Built with ❤️ using React and FastAPI

