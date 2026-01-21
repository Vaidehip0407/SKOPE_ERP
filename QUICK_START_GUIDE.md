# 🚀 Quick Start Guide - SKOPE ERP Ad Integrations & Reports

## ⚡ Get Started in 5 Minutes

### Step 1: Install Backend Dependencies (1 min)

```bash
cd backend
pip install -r requirements.txt
```

The new packages installed include:
- `facebook-business==18.0.5` - Meta/Facebook Ads integration
- `google-ads==23.0.0` - Google Ads integration
- `google-auth` packages - OAuth authentication
- Additional utilities

### Step 2: Initialize Database (1 min)

The database will automatically create new tables when you start the backend:

```bash
python init_db.py
```

**New tables created:**
1. `ad_account_connections` - OAuth connections for Meta & Google
2. `creative_assets` - Image/video asset library
3. `ad_campaign_creations` - Ad campaigns
4. `audiences` - Custom audiences
5. `ad_campaign_analytics` - Campaign metrics
6. `conversion_tracking` - Attribution data
7. `staff_attendance` - Staff attendance records
8. `staff_targets` - Monthly targets & incentives

### Step 3: Start Backend (30 seconds)

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 4: Start Frontend (1 min)

```bash
cd frontend
npm run dev
```

Access at: **http://localhost:5173**

### Step 5: Explore New Features (2 minutes)

#### Login
- Use existing credentials
- Default admin: `admin` / `admin123`

#### Navigate to New Pages

1. **Ad Integrations** (in sidebar)
   - Connect Meta Business account
   - Connect Google Ads account
   - Create ad campaigns
   - View analytics

2. **Advanced Reports** (in sidebar)
   - Daily Sales Summary
   - Product-wise Sales
   - Category-wise Sales
   - Staff Performance Reports
   - Inventory Analytics
   - Profitability Reports
   - Customer Intelligence

---

## 🎯 Quick Feature Tour

### Ad Integrations Page

**What you can do:**
- ✅ Connect Meta (Facebook/Instagram/WhatsApp) account
- ✅ Connect Google Ads account
- ✅ Create campaigns using templates
- ✅ Upload creative assets
- ✅ Manage audiences
- ✅ View campaign analytics

**Campaign Templates Available:**
- Store Visit Campaign
- Lead Form Campaign
- WhatsApp Click Campaign
- Offer/Festival Campaign
- Product Catalog Campaign
- Local Search Ads
- Performance Max
- Display Remarketing
- YouTube Local Awareness

### Advanced Reports Page

**Report Categories:**

1. **Sales Reports** (3 reports)
   - Daily summary with comparisons
   - Product-wise breakdown
   - Category analysis

2. **Staff Reports** (3 reports)
   - Sales performance
   - Incentive tracking
   - Attendance correlation

3. **Inventory & Stock** (4 reports)
   - Live stock status
   - Movement analysis
   - Reorder recommendations
   - High-value stock

4. **Profitability & Finance** (5 reports)
   - Margin analysis
   - Brand profitability
   - Discount impact
   - Payment mode breakdown
   - Outstanding receivables

5. **Customer Analytics** (3 reports)
   - Repeat customers
   - Warranty due
   - Purchase history

---

## 🔗 API Endpoints Available

### View API Documentation
Open: **http://localhost:8000/docs**

**New endpoint groups:**
- `/api/v1/ads/meta/*` - Meta integration (7 endpoints)
- `/api/v1/ads/google/*` - Google Ads integration (6 endpoints)
- `/api/v1/ads/campaigns/*` - Campaign management (5 endpoints)
- `/api/v1/ads/audiences/*` - Audience management (3 endpoints)
- `/api/v1/ads/analytics/*` - Analytics (2 endpoints)
- `/api/v1/reports/sales/*` - Sales reports (3 endpoints)
- `/api/v1/reports/staff/*` - Staff reports (3 endpoints)
- `/api/v1/reports/inventory/*` - Inventory reports (4 endpoints)
- `/api/v1/reports/profitability/*` - Finance reports (3 endpoints)
- `/api/v1/reports/finance/*` - Payment reports (2 endpoints)
- `/api/v1/reports/customers/*` - Customer reports (3 endpoints)

---

## 🧪 Test the Features

### Test Reports (Without OAuth Setup)

1. Go to **Advanced Reports**
2. Select "Sales Reports" → "Daily Sales Summary"
3. View today's sales metrics
4. Try other reports in different categories

### Test Ad Integrations (Requires OAuth Setup)

#### For Meta:
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create an app
3. Add credentials to `backend/.env`
4. Connect account in UI

#### For Google Ads:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and OAuth credentials
3. Add to `backend/.env`
4. Connect account in UI

---

## 📁 Files Modified/Created

### Backend Files
```
backend/
├── app/
│   ├── db/
│   │   └── models.py (EXTENDED - 8 new models)
│   ├── api/v1/
│   │   ├── ads.py (NEW - 500+ lines)
│   │   └── reports.py (EXTENDED - 1000+ lines)
│   └── main.py (UPDATED - ads router added)
└── requirements.txt (UPDATED - new packages)
```

### Frontend Files
```
frontend/
├── src/
│   ├── pages/
│   │   ├── AdIntegrations.tsx (NEW - 300+ lines)
│   │   └── AdvancedReports.tsx (NEW - 400+ lines)
│   ├── components/
│   │   └── Layout.tsx (UPDATED - navigation added)
│   └── App.tsx (UPDATED - routes added)
```

### Documentation Files
```
├── AD_INTEGRATIONS_AND_REPORTS_GUIDE.md (NEW)
├── IMPLEMENTATION_COMPLETE_SUMMARY.md (NEW)
└── QUICK_START_GUIDE.md (NEW - this file)
```

---

## 🎨 UI Preview

### Ad Integrations Page
```
┌─────────────────────────────────────────┐
│ Ad Platform Integrations                │
├─────────────────────────────────────────┤
│ [Connections] [Campaigns] [Analytics]   │
├─────────────────────────────────────────┤
│                                          │
│  📘 Meta Business        🔴 Not Connected│
│  Facebook, Instagram,                   │
│  WhatsApp                               │
│  [Connect Meta Business]                │
│                                          │
│  🔴 Google Ads          🔴 Not Connected│
│  Search, Display,                       │
│  YouTube                                │
│  [Connect Google Ads]                   │
│                                          │
└─────────────────────────────────────────┘
```

### Advanced Reports Page
```
┌──────┬────────────────────────────────┐
│      │  Advanced Reports & Analytics  │
│ 📊   ├────────────────────────────────┤
│Sales │ [Date Range: ___ to ___]      │
│      │                                │
│👥    │ Select a report:               │
│Staff │ • Daily Sales Summary          │
│      │ • Product-wise Sales           │
│📦    │ • Category-wise Sales          │
│Inv   │                                │
│      │ [View Report] [Export Excel]   │
│💰    │                                │
│Fin   │                                │
│      │                                │
│👤    │                                │
│Cust  │                                │
└──────┴────────────────────────────────┘
```

---

## 🔑 Key Features Summary

### 1. OAuth Integration
- ✅ Meta Business (FB/IG/WA)
- ✅ Google Ads
- ✅ Token auto-refresh
- ✅ Secure storage

### 2. Campaign Management
- ✅ 9 pre-built templates
- ✅ Guided creation flow
- ✅ Approval workflow
- ✅ Launch to platforms

### 3. Creative Management
- ✅ Upload images/videos
- ✅ Brand approval system
- ✅ Dynamic insertion

### 4. Audience Targeting
- ✅ Custom audiences from CRM
- ✅ Lookalike audiences
- ✅ Auto-sync (24 hours)

### 5. Analytics
- ✅ Real-time metrics
- ✅ ROAS tracking
- ✅ Store-level isolation

### 6. Reports (15+ reports)
- ✅ Sales analytics
- ✅ Staff performance
- ✅ Inventory insights
- ✅ Financial analysis
- ✅ Customer intelligence

---

## 🎯 What's Included

### Backend API (35+ endpoints)
- Meta OAuth (3 endpoints)
- Google OAuth (3 endpoints)
- Account management (2 endpoints)
- Creative assets (3 endpoints)
- Campaign CRUD (5 endpoints)
- Audience management (3 endpoints)
- Analytics (2 endpoints)
- Sales reports (3 endpoints)
- Staff reports (3 endpoints)
- Inventory reports (4 endpoints)
- Finance reports (5 endpoints)
- Customer reports (3 endpoints)

### Frontend Pages
- Ad Integrations page (full-featured)
- Advanced Reports page (15+ reports)
- Updated navigation
- Beautiful UI with TailwindCSS

### Database
- 8 new tables
- Proper relationships
- Optimized indexes

---

## 📞 Need Help?

### Check API Documentation
```
http://localhost:8000/docs
```

### Read Detailed Guides
- `AD_INTEGRATIONS_AND_REPORTS_GUIDE.md` - Complete setup
- `IMPLEMENTATION_COMPLETE_SUMMARY.md` - Feature list

### Test Endpoints
Use Swagger UI at `/docs` to test all endpoints

---

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads successfully
- [ ] Can navigate to "Ad Integrations" page
- [ ] Can navigate to "Advanced Reports" page
- [ ] API docs accessible at /docs
- [ ] Database tables created (check with SQL browser)
- [ ] Can view reports without OAuth (uses existing data)
- [ ] No linting errors in code

---

## 🎊 You're All Set!

**The system is fully functional and ready to use!**

### To Enable Ad Platform Features:
1. Set up Meta App (developers.facebook.com)
2. Set up Google Cloud Project (console.cloud.google.com)
3. Add credentials to `.env`
4. Connect accounts in UI

### To Use Reports (Works Immediately):
1. Navigate to "Advanced Reports"
2. Select a report category
3. Choose a report
4. Set date range (optional)
5. View or export data

---

## 🚀 Production Deployment

When ready for production:

1. **Environment Variables**
   ```env
   DATABASE_URL=postgresql://...
   META_APP_ID=prod_app_id
   GOOGLE_CLIENT_ID=prod_client_id
   ```

2. **Security**
   - Enable HTTPS
   - Secure token encryption
   - Rate limiting
   - CORS configuration

3. **Performance**
   - PostgreSQL database
   - Redis caching
   - CDN for assets

---

**Happy building with SKOPE ERP! 🎉**

All requirements from the SKOPE documents have been fully implemented and are ready for use!

