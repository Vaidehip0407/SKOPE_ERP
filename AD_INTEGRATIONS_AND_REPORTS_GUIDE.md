# 🚀 Meta & Google Ads Integration + Comprehensive Reporting Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Meta Integration Setup](#meta-integration-setup)
3. [Google Ads Integration Setup](#google-ads-integration-setup)
4. [Campaign Creation Engine](#campaign-creation-engine)
5. [Comprehensive Reports](#comprehensive-reports)
6. [API Endpoints](#api-endpoints)
7. [Database Schema](#database-schema)

---

## 🎯 Overview

This implementation includes:
- **Meta (Facebook/Instagram/WhatsApp) Integration** with OAuth 2.0
- **Google Ads Integration** with OAuth 2.0
- **Campaign Creation Engine** with pre-built templates
- **Creative Asset Management** system
- **Audience Targeting & Automation**
- **Conversion Tracking & Attribution**
- **Comprehensive Analytics Dashboard**
- **15+ Advanced Business Reports**

---

## 🔐 Meta Integration Setup

### Prerequisites
1. Meta Business Account
2. Meta App created in Meta for Developers
3. Business verification completed

### Step 1: Create Meta App

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app
3. Add these products:
   - Facebook Login
   - Marketing API
   - Instagram Basic Display
   - WhatsApp Business Management
4. Configure OAuth Redirect URI: `http://localhost:3000/ads/meta/callback`

### Step 2: Configure Environment Variables

Create or update `.env` file in `backend/` directory:

```env
META_APP_ID=your_meta_app_id
META_APP_SECRET=your_meta_app_secret
META_REDIRECT_URI=http://localhost:3000/ads/meta/callback
```

### Step 3: Required Permissions

The following permissions are requested:
- `ads_management` - Create and manage ads
- `ads_read` - Read ad account insights
- `business_management` - Access business account
- `pages_read_engagement` - Read Page insights
- `pages_manage_ads` - Create ads on Pages
- `instagram_basic` - Instagram account access
- `instagram_manage_insights` - Instagram insights
- `whatsapp_business_management` - WhatsApp Business account

### Step 4: Store Ad Account Details

After OAuth connection, store:
- Ad Account ID (act_xxxxx)
- Pixel ID
- Page ID
- Business ID

---

## 🔍 Google Ads Integration Setup

### Prerequisites
1. Google Ads Account
2. Google Cloud Project
3. Google Ads API access enabled

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Ads API
4. Create OAuth 2.0 credentials

### Step 2: Configure OAuth Consent Screen

1. Configure OAuth consent screen
2. Add scopes:
   - `https://www.googleapis.com/auth/adwords`
   - `https://www.googleapis.com/auth/analytics.readonly`

### Step 3: Environment Variables

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/ads/google/callback
GOOGLE_DEVELOPER_TOKEN=your_google_ads_developer_token
```

### Step 4: Get Developer Token

1. Go to Google Ads
2. Navigate to Tools & Settings > Setup > API Center
3. Request access and get developer token

---

## 🎨 Campaign Creation Engine

### Campaign Templates

#### Meta Templates

1. **Store Visit Campaign**
   - Objective: Drive foot traffic to physical store
   - Features: Location targeting, store radius

2. **Lead Form Campaign**
   - Objective: Collect customer leads
   - Features: Native lead forms

3. **WhatsApp Click Campaign**
   - Objective: Direct customers to WhatsApp
   - Features: Click-to-WhatsApp ads

4. **Offer/Festival Campaign**
   - Objective: Promote special offers
   - Features: Dynamic offers, urgency

5. **Product Catalog Campaign**
   - Objective: Showcase products
   - Features: Dynamic product ads

#### Google Templates

1. **Local Search Ads**
   - Objective: Appear in local searches
   - Features: Location extensions

2. **Performance Max (Retail)**
   - Objective: Maximize conversions
   - Features: AI-powered optimization

3. **Display Remarketing**
   - Objective: Retarget website visitors
   - Features: Custom audiences

4. **YouTube Local Awareness**
   - Objective: Video awareness in local area
   - Features: Geographic targeting

### Campaign Creation Flow

```
1. Select Platform (Meta/Google)
2. Choose Template
3. Upload Creatives
4. Set Budget & Schedule
5. Define Audience
6. Submit for Approval
7. Launch to Platform
```

### Approval Workflow

- **Store Manager**: Can create, approve, and launch campaigns for their store
- **Brand Head (Super Admin)**: Read-only view of all stores' campaigns
- **Marketing Team**: Can create campaigns, requires approval

---

## 📊 Comprehensive Reports

### A. Sales Reports

#### 1. Daily Sales Summary
```
GET /api/v1/reports/sales/daily-summary
```
**Features:**
- Total sales, bills, average bill value
- Payment mode breakdown (Cash/Card/UPI)
- Comparisons: vs Yesterday, vs Same Day Last Week
- Growth percentages

#### 2. Product-wise Sales Report
```
GET /api/v1/reports/sales/product-wise
```
**Data:**
- Product name, SKU
- Quantity sold
- Sales value
- Discount given
- Margin earned

#### 3. Category-wise Sales Report
```
GET /api/v1/reports/sales/category-wise
```
**Data:**
- Category (Mobiles/TVs/AC/Accessories)
- Revenue contribution %
- Profit contribution %

---

### B. Staff Reports

#### 1. Staff-wise Sales Report
```
GET /api/v1/reports/staff/sales-report
```
**Metrics:**
- Bills generated
- Sales value
- Units sold
- Conversion rate

#### 2. Staff Incentive Report
```
GET /api/v1/reports/staff/incentive-report
```
**Data:**
- Target vs Achieved
- Incentive earned
- Incentive paid
- Pending incentive

#### 3. Staff Attendance + Sales Correlation
```
GET /api/v1/reports/staff/attendance-sales-correlation
```
**Insights:**
- Present days
- Sales per day
- Sales per hour
- Performance correlation

---

### C. Inventory & Stock Analytics

#### 1. Live Stock Report
```
GET /api/v1/reports/inventory/live-stock
```
**Info:**
- Item name, SKU
- Available quantity
- Store location
- Last sold date

#### 2. Fast Moving vs Slow Moving Items
```
GET /api/v1/reports/inventory/movement-analysis
```
**Analysis:**
- Days since last sale
- Stock ageing (0-30/31-60/60+ days)
- Movement status

#### 3. Reorder Level Report
```
GET /api/v1/reports/inventory/reorder-level
```
**Recommendations:**
- Current vs Minimum stock
- Suggested reorder quantity
- Estimated cost

#### 4. High-Value Stock Report
```
GET /api/v1/reports/inventory/high-value-stock
```
**Focus:**
- Items with high value but low movement
- Capital blocked
- Optimization suggestions

---

### D. Profitability & Finance Reports

#### 1. Item-wise Margin Report
```
GET /api/v1/reports/profitability/item-wise-margin
```
**Details:**
- Purchase price
- Selling price
- Discount impact
- Net margin %

#### 2. Brand-wise Profitability
```
GET /api/v1/reports/profitability/brand-wise
```
**Metrics:**
- Revenue vs Gross profit
- Margin % by brand
- Brand performance ranking

#### 3. Invoice Discount Impact Report
```
GET /api/v1/reports/profitability/discount-impact
```
**Analysis:**
- Total discount given
- Discount vs profit erosion
- Optimization recommendations

#### 4. Payment Mode Report
```
GET /api/v1/reports/finance/payment-mode-report
```
**Breakdown:**
- Cash / UPI / Card / EMI / Finance
- Transaction count by mode
- Amount by mode

#### 5. Outstanding Receivables
```
GET /api/v1/reports/finance/outstanding-receivables
```
**Tracking:**
- Finance pending
- Customer dues
- Days pending
- Collection priority

---

### E. Customer Analytics

#### 1. Repeat Customer Report
```
GET /api/v1/reports/customers/repeat-customers
```
**Insights:**
- Number of repeat visits
- Lifetime value
- Preferred products

#### 2. Warranty / AMC Due Report
```
GET /api/v1/reports/customers/warranty-due
```
**Follow-up:**
- Warranty expiry dates
- Service opportunities
- Proactive engagement

#### 3. Customer Purchase History
```
GET /api/v1/reports/customers/{customer_id}/purchase-history
```
**Intelligence:**
- Last purchase date
- Purchase patterns
- Accessory cross-sell suggestions

---

## 🔌 API Endpoints

### Ad Integration Endpoints

#### Meta Integration
```
GET  /api/v1/ads/meta/auth-url          - Get OAuth URL
POST /api/v1/ads/meta/callback          - Handle OAuth callback
POST /api/v1/ads/meta/connect           - Save connection
```

#### Google Ads Integration
```
GET  /api/v1/ads/google/auth-url        - Get OAuth URL
POST /api/v1/ads/google/callback        - Handle OAuth callback
POST /api/v1/ads/google/connect         - Save connection
```

#### Account Management
```
GET  /api/v1/ads/connections                     - Get all connections
POST /api/v1/ads/connections/{id}/refresh-token  - Refresh token
```

#### Creative Assets
```
POST /api/v1/ads/assets/upload           - Upload creative
GET  /api/v1/ads/assets                  - Get all assets
POST /api/v1/ads/assets/{id}/approve     - Approve asset
```

#### Campaign Management
```
GET  /api/v1/ads/campaign-templates      - Get templates
POST /api/v1/ads/campaigns/create        - Create campaign
GET  /api/v1/ads/campaigns               - List campaigns
POST /api/v1/ads/campaigns/{id}/approve  - Approve campaign
POST /api/v1/ads/campaigns/{id}/launch   - Launch to platform
```

#### Audience Management
```
POST /api/v1/ads/audiences/create        - Create audience
GET  /api/v1/ads/audiences               - List audiences
POST /api/v1/ads/audiences/{id}/sync     - Sync to platform
```

#### Analytics
```
GET  /api/v1/ads/campaigns/{id}/analytics  - Campaign analytics
GET  /api/v1/ads/analytics/overview        - Overall analytics
```

---

## 🗄️ Database Schema

### New Tables

#### 1. ad_account_connections
```sql
- id, store_id, platform
- meta_ad_account_id, meta_pixel_id, meta_page_id
- google_customer_id, google_conversion_actions
- access_token, refresh_token, token_expires_at
- is_active, last_sync_at
```

#### 2. creative_assets
```sql
- id, store_id, name, asset_type
- file_path, file_url
- meta_creative_id, google_asset_id
- is_approved, created_by
```

#### 3. ad_campaign_creations
```sql
- id, store_id, ad_account_id
- campaign_name, campaign_template, platform
- objective, budget_daily, budget_total
- headline, description, call_to_action
- target_audience, location_radius
- external_campaign_id, status
- created_by, approved_by
```

#### 4. audiences
```sql
- id, store_id, ad_account_id
- name, audience_type, platform
- source_criteria, customer_ids
- external_audience_id, size
- auto_sync, last_synced_at
```

#### 5. ad_campaign_analytics
```sql
- id, campaign_id, date
- impressions, clicks, spend, reach
- leads, store_visits, sales_attributed
- ctr, cpc, cpl, roas
```

#### 6. staff_attendance
```sql
- id, user_id, store_id, date
- check_in, check_out, hours_worked
- status (present/absent/half_day/leave)
```

#### 7. staff_targets
```sql
- id, user_id, store_id, month
- target_amount, achieved_amount
- incentive_earned, incentive_paid
- incentive_pending
```

#### 8. conversion_tracking
```sql
- id, store_id, campaign_id
- conversion_type, customer_id, sale_id
- platform, conversion_value
- click_id, utm_source, utm_campaign
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔑 Key Features

### 1. Token Refresh Automation
- Automatic token refresh before expiry
- Meta: 60-day tokens, auto-refresh at 50 days
- Google: 1-hour tokens, refresh using refresh_token

### 2. Store-Level Access Control
- Each store manager controls only their store's campaigns
- Brand head has read-only access to all stores
- Secure campaign approval workflow

### 3. Dynamic Creative Insertion
- Auto-insert store name, location, offers
- Brand-approved creative library
- Multi-format support (images, videos, carousels)

### 4. Audience Auto-Sync
- Sync ERP customer data to ad platforms every 24 hours
- Custom audiences from CRM data
- Lookalike audience generation

### 5. Conversion Attribution
- Track clicks with fbclid/gclid
- Offline conversion upload
- ROI measurement

---

## 📈 Reporting Features

### Export Options
All reports support:
- Excel export
- PDF export (via reportlab)
- CSV export
- API JSON response

### Date Range Filters
- Custom date ranges
- Preset ranges (Today, This Week, This Month, Last Month)
- Year-over-year comparison

### Store Filtering
- Super Admin: View all stores or specific store
- Store Manager: Only their store
- Automatic filtering based on role

---

## 🎯 Next Steps

1. **Configure OAuth Apps**: Set up Meta and Google OAuth applications
2. **Add Environment Variables**: Update `.env` file with credentials
3. **Test Connections**: Connect test ad accounts
4. **Create Test Campaign**: Use templates to create first campaign
5. **Enable Analytics**: Set up conversion tracking
6. **Train Users**: Onboard store managers on campaign creation

---

## 📞 Support

For issues or questions:
- Check API documentation: http://localhost:8000/docs
- Review logs in backend console
- Test endpoints using Swagger UI

---

## 🔒 Security Notes

⚠️ **Important:**
- Never commit `.env` files to git
- Use encrypted tokens in production
- Implement rate limiting for API calls
- Regular token rotation
- Audit logs for all campaign changes
- HTTPS required for production OAuth callbacks

---

## ✅ Feature Checklist

- [x] Meta OAuth Integration
- [x] Google OAuth Integration
- [x] Token Refresh Automation
- [x] Campaign Templates (Meta & Google)
- [x] Creative Asset Management
- [x] Audience Management
- [x] Campaign Creation Engine
- [x] Approval Workflow
- [x] Conversion Tracking
- [x] Analytics Dashboard
- [x] Daily Sales Summary
- [x] Product-wise Sales Report
- [x] Category-wise Sales Report
- [x] Staff Sales Report
- [x] Staff Incentive Report
- [x] Attendance-Sales Correlation
- [x] Live Stock Report
- [x] Stock Movement Analysis
- [x] Reorder Level Report
- [x] High-Value Stock Report
- [x] Item-wise Margin Report
- [x] Brand-wise Profitability
- [x] Discount Impact Report
- [x] Payment Mode Report
- [x] Outstanding Receivables
- [x] Repeat Customer Report
- [x] Warranty Due Report
- [x] Customer Purchase History

---

**All features implemented and ready for use!** 🎉

