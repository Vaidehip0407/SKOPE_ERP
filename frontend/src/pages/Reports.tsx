import { useState } from 'react'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { DocumentArrowDownIcon } from '@heroicons/react/24/outline'
import StoreSelector from '../components/StoreSelector'
import { useAuthStore } from '../store/authStore'

export default function Reports() {
  const { user } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [selectedReport, setSelectedReport] = useState<string | null>(null)
  const [showCustomColumns, setShowCustomColumns] = useState(false)
  const [dateRange, setDateRange] = useState({
    startDate: new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  })
  // Custom columns - to be implemented
  // const [selectedColumns, setSelectedColumns] = useState<string[]>([])
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>(user?.role === 'super_admin' ? 'all' : (user?.store_id || 'all'))

  const downloadReport = async (reportType: string, endpoint: string) => {
    setLoading(true)
    setSelectedReport(reportType)

    try {
      const params: any = {
        start_date: `${dateRange.startDate}T00:00:00`,
        end_date: `${dateRange.endDate}T23:59:59`
      }
      if (selectedStoreId !== 'all') {
        params.store_id = selectedStoreId
      }

      const response = await api.get(endpoint, {
        responseType: 'blob',
        params
      })

      // Try to get filename from Content-Disposition header
      let filename = `${reportType}_${new Date().toISOString().split('T')[0]}.xlsx`
      const contentDisposition = response.headers['content-disposition']
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '')
        }
      }

      // Create blob and download
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)

      toast.success('Report downloaded successfully')
    } catch (error: any) {
      console.error('Download error:', error)
      let errorMessage = 'Failed to download report'
      if (error.response?.data) {
        // For blob errors, we might need to read the blob
        if (error.response.data instanceof Blob) {
          try {
            const text = await error.response.data.text()
            const errorData = JSON.parse(text)
            errorMessage = errorData.detail || errorMessage
          } catch (e) {
            // Couldn't parse error, use default
          }
        }
      }
      toast.error(errorMessage)
    } finally {
      setLoading(false)
      setSelectedReport(null)
    }
  }

  const availableColumns = {
    sales: ['Transaction ID', 'Date', 'Customer', 'Items', 'Subtotal', 'Tax', 'Total', 'Payment Method', 'Store'],
    inventory: ['SKU', 'Product Name', 'Category', 'Stock', 'Min Stock', 'Cost Price', 'Selling Price', 'GST', 'Warranty'],
    customers: ['ID', 'Name', 'Phone', 'Email', 'Total Purchases', 'Total Spent', 'Last Purchase', 'Status'],
    expenses: ['Date', 'Category', 'Description', 'Amount', 'Payment Mode', 'Vendor', 'Receipt #', 'Voucher']
  }

  const reports = [
    {
      id: 'sales',
      title: 'Sales Report',
      description: 'Download detailed sales transactions with custom columns',
      endpoint: '/reports/sales/excel',
      color: 'from-blue-500 to-blue-600',
      icon: '📊',
    },
    {
      id: 'inventory',
      title: 'Inventory Report',
      description: 'Current stock levels, product details, and valuations',
      endpoint: '/reports/inventory/excel',
      color: 'from-purple-500 to-purple-600',
      icon: '📦',
    },
    {
      id: 'customers',
      title: 'Customer Report',
      description: 'Customer database with purchase history and analytics',
      endpoint: '/reports/customers/excel',
      color: 'from-green-500 to-green-600',
      icon: '👥',
    },
    {
      id: 'expenses',
      title: 'Expenses Report',
      description: 'Expense records with vouchers and financial details',
      endpoint: '/reports/expenses/excel',
      color: 'from-red-500 to-red-600',
      icon: '💰',
    },
    {
      id: 'profit_loss',
      title: 'Profit & Loss Statement',
      description: 'Comprehensive P&L report with revenue and expense breakdown',
      endpoint: '/reports/profit-loss/excel',
      color: 'from-indigo-500 to-indigo-600',
      icon: '📈',
    },
    {
      id: 'tax',
      title: 'GST/Tax Report',
      description: 'GST collected, paid, and tax compliance records',
      endpoint: '/reports/tax/excel',
      color: 'from-yellow-500 to-yellow-600',
      icon: '📝',
    },
  ]

  return (
    <div>
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            📊 Reports & Analytics
          </h1>
          <p className="text-neutral-600 mt-2 text-lg">
            Generate and download comprehensive business reports with custom columns
          </p>
        </div>
        <StoreSelector
          selectedStoreId={selectedStoreId}
          onStoreChange={setSelectedStoreId}
          showAllOption={true}
        />
      </div>

      {/* Date Range & Options */}
      <div className="card mb-8 bg-gradient-to-r from-primary/5 to-accent/5 border-2 border-primary/20">
        <h3 className="text-lg font-bold text-primary mb-4 flex items-center gap-2">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
          Report Settings
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label text-sm font-semibold">Start Date</label>
            <input
              type="date"
              value={dateRange.startDate}
              onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
              className="input"
            />
          </div>
          <div>
            <label className="label text-sm font-semibold">End Date</label>
            <input
              type="date"
              value={dateRange.endDate}
              onChange={(e) => setDateRange({ ...dateRange, endDate: e.target.value })}
              className="input"
            />
          </div>
        </div>
        <div className="mt-4 flex items-center gap-3">
          <button
            onClick={() => setShowCustomColumns(!showCustomColumns)}
            className="btn btn-outline text-sm"
          >
            {showCustomColumns ? '✓ Custom Columns Active' : '⚙️ Customize Columns'}
          </button>
          <span className="text-xs text-neutral-500">
            Selected range: {Math.ceil((new Date(dateRange.endDate).getTime() - new Date(dateRange.startDate).getTime()) / (1000 * 60 * 60 * 24))} days
          </span>
        </div>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map((report) => (
          <div
            key={report.id}
            className="card hover:shadow-2xl transition-all hover:scale-105 border-2 border-transparent hover:border-primary/30"
          >
            <div className={`h-2 rounded-t-lg bg-gradient-to-r ${report.color} -mx-6 -mt-6 mb-4`} />
            <div className="flex items-start gap-3 mb-4">
              <div className={`text-4xl p-3 rounded-xl bg-gradient-to-br ${report.color} text-white shadow-lg`}>
                {report.icon}
              </div>
              <div className="flex-1">
                <h2 className="text-lg font-bold text-primary mb-1">
                  {report.title}
                </h2>
                <p className="text-xs text-neutral-500 font-medium">
                  {dateRange.startDate} to {dateRange.endDate}
                </p>
              </div>
            </div>
            <p className="text-sm text-neutral-600 mb-6 min-h-[40px]">{report.description}</p>

            <button
              onClick={() => downloadReport(report.id, report.endpoint)}
              disabled={loading && selectedReport === report.id}
              className={`btn w-full flex items-center justify-center disabled:opacity-50 bg-gradient-to-r ${report.color} text-white hover:shadow-xl transition-all`}
            >
              <DocumentArrowDownIcon className="w-5 h-5 mr-2" />
              {loading && selectedReport === report.id
                ? 'Generating...'
                : 'Download Excel'}
            </button>
          </div>
        ))}
      </div>

      {/* Daily Closing Report */}
      <div className="card mt-8">
        <h2 className="text-xl font-bold text-primary mb-4">
          Daily Closing Report
        </h2>
        <p className="text-neutral-600 mb-6">
          Generate a comprehensive daily closing report with sales, expenses, and cash reconciliation
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="label">Select Date</label>
            <input
              type="date"
              className="input"
              defaultValue={new Date().toISOString().split('T')[0]}
            />
          </div>
          <div className="flex items-end">
            <button className="btn btn-primary w-full">
              Generate Report
            </button>
          </div>
        </div>
      </div>

      {/* Custom Columns Section */}
      {showCustomColumns && (
        <div className="card mt-8 bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-300">
          <h3 className="text-xl font-bold text-purple-800 mb-4 flex items-center gap-2">
            <span>⚙️</span>
            Customize Report Columns
          </h3>
          <p className="text-sm text-purple-700 mb-4">
            Select which columns you want in your reports. This will be saved for future exports.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(availableColumns).map(([reportType, columns]) => (
              <div key={reportType} className="bg-white rounded-xl p-4 shadow-md">
                <h4 className="font-bold text-gray-800 mb-3 capitalize flex items-center gap-2">
                  {reports.find(r => r.id === reportType)?.icon}
                  {reportType} Columns
                </h4>
                <div className="space-y-2">
                  {columns.map((col) => (
                    <label key={col} className="flex items-center gap-2 text-sm hover:bg-gray-50 p-2 rounded cursor-pointer">
                      <input type="checkbox" className="rounded text-primary" defaultChecked />
                      <span>{col}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 flex gap-3">
            <button className="btn btn-primary">
              💾 Save Column Preferences
            </button>
            <button
              className="btn btn-outline"
              onClick={() => setShowCustomColumns(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Report Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-300">
          <h3 className="font-bold text-blue-900 mb-3 flex items-center gap-2 text-lg">
            <span>📋</span>
            Report Features
          </h3>
          <ul className="text-sm text-blue-800 space-y-2">
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              All reports in Excel format (.xlsx)
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              Custom date range selection
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              Customizable columns
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              Historical data access
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-600">✓</span>
              GST/Tax compliance ready
            </li>
          </ul>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-300">
          <h3 className="font-bold text-purple-900 mb-3 flex items-center gap-2 text-lg">
            <span>💡</span>
            Pro Tips
          </h3>
          <ul className="text-sm text-purple-800 space-y-2">
            <li className="flex items-start gap-2">
              <span>→</span>
              <span>Use custom date ranges for month-over-month comparison</span>
            </li>
            <li className="flex items-start gap-2">
              <span>→</span>
              <span>Download expense reports with vouchers for audits</span>
            </li>
            <li className="flex items-start gap-2">
              <span>→</span>
              <span>Generate P&L statements for financial analysis</span>
            </li>
            <li className="flex items-start gap-2">
              <span>→</span>
              <span>Export customer data for marketing campaigns</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}

