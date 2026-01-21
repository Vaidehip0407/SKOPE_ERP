import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import {
  CubeIcon,
  ShoppingCartIcon,
  UsersIcon,
  CurrencyDollarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline'
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts'

interface DashboardStats {
  inventory: {
    total_products: number
    low_stock_products: number
    out_of_stock_products: number
    total_stock_value: number
  }
  sales: {
    today_sales: number
    today_transactions: number
    month_sales: number
    month_transactions: number
    average_transaction_value: number
  }
  financial: {
    today_revenue: number
    today_expenses: number
    today_profit: number
    month_revenue: number
    month_expenses: number
    month_profit: number
  }
}

const COLORS = ['#1D3557', '#457B9D', '#A8DADC', '#E63946', '#F77F88']

interface Store {
  id: number
  name: string
}

export default function Dashboard() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  // Store selector (Super Admin only)
  const [stores, setStores] = useState<Store[]>([])
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>('all')

  // Date range and comparison states
  const [dateRange, setDateRange] = useState({
    startDate: new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  })
  const [comparisonMode, setComparisonMode] = useState<'none' | 'previous_period' | 'last_year'>('none')
  // Comparison data - to be implemented
  // const [comparisonData, setComparisonData] = useState<any>(null)

  // Sample data for charts (In production, fetch from API based on date range)
  const salesTrendData = [
    { name: 'Mon', sales: 4000, profit: 2400, lastYearSales: 3500, lastYearProfit: 2100 },
    { name: 'Tue', sales: 3000, profit: 1398, lastYearSales: 2800, lastYearProfit: 1200 },
    { name: 'Wed', sales: 2000, profit: 9800, lastYearSales: 1800, lastYearProfit: 9000 },
    { name: 'Thu', sales: 2780, profit: 3908, lastYearSales: 2500, lastYearProfit: 3500 },
    { name: 'Fri', sales: 1890, profit: 4800, lastYearSales: 1700, lastYearProfit: 4200 },
    { name: 'Sat', sales: 2390, profit: 3800, lastYearSales: 2200, lastYearProfit: 3400 },
    { name: 'Sun', sales: 3490, profit: 4300, lastYearSales: 3200, lastYearProfit: 3900 },
  ]

  const categoryData = [
    { name: 'Electronics', value: 400 },
    { name: 'Clothing', value: 300 },
    { name: 'Food', value: 200 },
    { name: 'Books', value: 100 },
    { name: 'Others', value: 150 },
  ]

  const paymentData = [
    { name: 'Cash', value: 45 },
    { name: 'Card', value: 30 },
    { name: 'UPI', value: 20 },
    { name: 'QR Code', value: 5 },
  ]

  const monthlyRevenueData = [
    { month: 'Jan', revenue: 45000, expenses: 25000 },
    { month: 'Feb', revenue: 52000, expenses: 28000 },
    { month: 'Mar', revenue: 48000, expenses: 26000 },
    { month: 'Apr', revenue: 61000, expenses: 30000 },
    { month: 'May', revenue: 55000, expenses: 29000 },
    { month: 'Jun', revenue: 67000, expenses: 32000 },
  ]

  useEffect(() => {
    if (user?.role === 'super_admin') {
      loadStores()
    }
    loadDashboardData()
  }, [])

  useEffect(() => {
    // Reload dashboard when store selection changes
    if (user?.role === 'super_admin') {
      loadDashboardData()
    }
  }, [selectedStoreId])

  const loadStores = async () => {
    try {
      const response = await api.get('/stores/')
      setStores(response.data)
    } catch (error) {
      console.error('Error loading stores:', error)
    }
  }

  const loadDashboardData = async () => {
    try {
      console.log('Loading dashboard data...')
      const [inventoryRes, salesRes, financialRes] = await Promise.all([
        api.get('/inventory/dashboard'),
        api.get('/sales/dashboard/stats'),
        api.get('/financial/dashboard/stats'),
      ])

      console.log('Dashboard data loaded:', {
        inventory: inventoryRes.data,
        sales: salesRes.data,
        financial: financialRes.data
      })

      setStats({
        inventory: inventoryRes.data,
        sales: salesRes.data,
        financial: financialRes.data,
      })
    } catch (error: any) {
      console.error('Failed to load dashboard data:', error)
      console.error('Error details:', error.response?.data)

      // Set default values on error
      setStats({
        inventory: {
          total_products: 0,
          low_stock_products: 0,
          out_of_stock_products: 0,
          total_stock_value: 0
        },
        sales: {
          today_sales: 0,
          today_transactions: 0,
          month_sales: 0,
          month_transactions: 0,
          average_transaction_value: 0
        },
        financial: {
          today_revenue: 0,
          today_expenses: 0,
          today_profit: 0,
          month_revenue: 0,
          month_expenses: 0,
          month_profit: 0
        }
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-neutral-600">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-primary">Dashboard</h1>
            <p className="text-neutral-600 mt-2">
              Welcome back, {user?.full_name || user?.username}!
            </p>
          </div>

          {/* Store Selector (Super Admin Only) */}
          {user?.role === 'super_admin' && stores.length > 0 && (
            <div className="flex items-center gap-3">
              <label className="text-sm font-medium text-neutral-700">View Store:</label>
              <select
                value={selectedStoreId}
                onChange={(e) => setSelectedStoreId(e.target.value === 'all' ? 'all' : parseInt(e.target.value))}
                className="input w-64"
              >
                <option value="all">📊 All Stores (Consolidated)</option>
                {stores.map((store) => (
                  <option key={store.id} value={store.id}>
                    🏪 {store.name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>

      {/* No Data Warning */}
      {stats && stats.inventory.total_products === 0 && stats.sales.today_sales === 0 && (
        <div className="card mb-8 bg-gradient-to-r from-yellow-50 to-orange-50 border-2 border-yellow-400">
          <div className="flex items-start gap-4">
            <div className="text-5xl">⚠️</div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-yellow-900 mb-2">
                No Data Available
              </h3>
              <p className="text-yellow-800 mb-4">
                Your database appears to be empty. To get started, you can:
              </p>
              <ul className="text-sm text-yellow-800 space-y-2 mb-4">
                <li>• <strong>Add Products:</strong> Go to Inventory page and add your products</li>
                <li>• <strong>Add Customers:</strong> Go to Customers page and add customers</li>
                <li>• <strong>Create Sales:</strong> Go to Sales page and record transactions</li>
                <li>• <strong>Load Sample Data:</strong> Run <code className="bg-yellow-200 px-2 py-1 rounded">python seed_data.py</code> in backend directory</li>
              </ul>
              <button
                onClick={() => loadDashboardData()}
                className="btn bg-yellow-600 hover:bg-yellow-700 text-white"
              >
                🔄 Refresh Dashboard
              </button>
            </div>
          </div>
        </div>
      )}


      {/* Date Range & Comparison Controls */}
      <div className="card mb-8 bg-gradient-to-r from-primary/5 to-accent/5 border-2 border-primary/20">
        <div className="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-bold text-primary mb-2 flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Custom Date Range
            </h3>
            <div className="flex flex-wrap gap-3">
              <div>
                <label className="text-xs text-neutral-600 font-medium">Start Date</label>
                <input
                  type="date"
                  value={dateRange.startDate}
                  onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
                  className="input mt-1"
                />
              </div>
              <div>
                <label className="text-xs text-neutral-600 font-medium">End Date</label>
                <input
                  type="date"
                  value={dateRange.endDate}
                  onChange={(e) => setDateRange({ ...dateRange, endDate: e.target.value })}
                  className="input mt-1"
                />
              </div>
            </div>
          </div>

          <div className="flex-1">
            <h3 className="text-lg font-bold text-primary mb-2 flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Comparison Mode
            </h3>
            <select
              value={comparisonMode}
              onChange={(e) => setComparisonMode(e.target.value as any)}
              className="input"
            >
              <option value="none">No Comparison</option>
              <option value="previous_period">vs Previous Period</option>
              <option value="last_year">vs Same Period Last Year (YoY)</option>
            </select>
          </div>

          <button
            onClick={() => loadDashboardData()}
            className="btn btn-primary self-end lg:self-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh Data
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm">Today's Sales</p>
              <p className="text-3xl font-bold mt-2">
                ₹{stats?.sales?.today_sales?.toFixed(0) || '0'}
              </p>
              <div className="flex items-center mt-2 text-blue-100 text-sm">
                <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
                <span>{stats?.sales?.today_transactions || 0} transactions</span>
              </div>
            </div>
            <ShoppingCartIcon className="w-12 h-12 text-blue-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm">Today's Profit</p>
              <p className="text-3xl font-bold mt-2">
                ₹{stats?.financial?.today_profit?.toFixed(0) || '0'}
              </p>
              <div className="flex items-center mt-2 text-green-100 text-sm">
                <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
                <span>Revenue - Expenses</span>
              </div>
            </div>
            <CurrencyDollarIcon className="w-12 h-12 text-green-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm">Total Products</p>
              <p className="text-3xl font-bold mt-2">
                {stats?.inventory?.total_products || 0}
              </p>
              <div className="flex items-center mt-2 text-purple-100 text-sm">
                {stats && stats.inventory && stats.inventory.low_stock_products > 0 ? (
                  <>
                    <ArrowTrendingDownIcon className="w-4 h-4 mr-1" />
                    <span>{stats.inventory.low_stock_products} low stock</span>
                  </>
                ) : (
                  <span>All items in stock</span>
                )}
              </div>
            </div>
            <CubeIcon className="w-12 h-12 text-purple-200" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-100 text-sm">Stock Value</p>
              <p className="text-3xl font-bold mt-2">
                ₹{stats?.inventory?.total_stock_value?.toFixed(0) || '0'}
              </p>
              <div className="flex items-center mt-2 text-orange-100 text-sm">
                <span>Total inventory</span>
              </div>
            </div>
            <UsersIcon className="w-12 h-12 text-orange-200" />
          </div>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Sales Trend Chart */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-primary">
              Sales Trend {comparisonMode === 'last_year' && '(YoY Comparison)'}
            </h2>
            {comparisonMode === 'last_year' && (
              <span className="text-xs bg-accent/10 text-accent font-bold px-3 py-1 rounded-full">
                📊 vs Last Year
              </span>
            )}
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={salesTrendData}>
              <defs>
                <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#1D3557" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#1D3557" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#457B9D" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#457B9D" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="sales"
                stroke="#1D3557"
                fillOpacity={1}
                fill="url(#colorSales)"
                name="Current Sales"
              />
              <Area
                type="monotone"
                dataKey="profit"
                stroke="#457B9D"
                fillOpacity={1}
                fill="url(#colorProfit)"
                name="Current Profit"
              />
              {comparisonMode === 'last_year' && (
                <>
                  <Area
                    type="monotone"
                    dataKey="lastYearSales"
                    stroke="#E63946"
                    strokeDasharray="5 5"
                    fillOpacity={0.3}
                    fill="#E63946"
                    name="Last Year Sales"
                  />
                  <Area
                    type="monotone"
                    dataKey="lastYearProfit"
                    stroke="#F77F88"
                    strokeDasharray="5 5"
                    fillOpacity={0.3}
                    fill="#F77F88"
                    name="Last Year Profit"
                  />
                </>
              )}
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Category Distribution */}
        <div className="card">
          <h2 className="text-xl font-bold text-primary mb-4">
            Sales by Category
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name}: ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Monthly Revenue vs Expenses */}
        <div className="card">
          <h2 className="text-xl font-bold text-primary mb-4">
            Monthly Revenue vs Expenses
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={monthlyRevenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="revenue" fill="#1D3557" name="Revenue" />
              <Bar dataKey="expenses" fill="#E63946" name="Expenses" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Payment Methods Distribution */}
        <div className="card">
          <h2 className="text-xl font-bold text-primary mb-4">
            Payment Methods Distribution
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={paymentData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}%`}
              >
                {paymentData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold text-primary mb-4">
            Monthly Sales Overview
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-neutral-200">
              <span className="text-neutral-600">Total Sales</span>
              <span className="font-bold text-lg text-green-600">
                ₹{stats?.sales.month_sales.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-neutral-200">
              <span className="text-neutral-600">Transactions</span>
              <span className="font-bold text-lg">
                {stats?.sales.month_transactions}
              </span>
            </div>
            <div className="flex justify-between items-center py-3">
              <span className="text-neutral-600">Avg. Transaction</span>
              <span className="font-bold text-lg">
                ₹{stats?.sales.average_transaction_value.toFixed(2)}
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-primary mb-4">
            Monthly Financial Overview
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-neutral-200">
              <span className="text-neutral-600">Revenue</span>
              <span className="font-bold text-lg text-green-600">
                ₹{stats?.financial.month_revenue.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-neutral-200">
              <span className="text-neutral-600">Expenses</span>
              <span className="font-bold text-lg text-red-600">
                ₹{stats?.financial.month_expenses.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between items-center py-3">
              <span className="text-neutral-600">Net Profit</span>
              <span className="font-bold text-lg text-primary">
                ₹{stats?.financial.month_profit.toFixed(2)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Alerts */}
      {stats && stats.inventory.low_stock_products > 0 && (
        <div className="card bg-accent-light/10 border-l-4 border-accent mt-6">
          <div className="flex items-center">
            <div className="flex-1">
              <h3 className="font-bold text-accent">Low Stock Alert!</h3>
              <p className="text-neutral-700 mt-1">
                {stats.inventory.low_stock_products} products are running low on stock.
                Please restock soon.
              </p>
            </div>
            <button
              onClick={() => window.location.href = '/inventory'}
              className="btn btn-accent ml-4"
            >
              View Products
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
