import { useEffect, useState } from 'react'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { Sale } from '../utils/types'
import { PlusIcon, MagnifyingGlassIcon, ShoppingCartIcon, CurrencyDollarIcon, ClockIcon } from '@heroicons/react/24/outline'
import { format } from 'date-fns'
import StoreSelector from '../components/StoreSelector'
import Modal from '../components/Modal'
import SaleForm from '../components/SaleForm'

export default function Sales() {
  const [sales, setSales] = useState<Sale[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>('all')
  const [showSaleModal, setShowSaleModal] = useState(false)

  useEffect(() => {
    loadSales()
  }, [selectedStoreId])

  const loadSales = async () => {
    try {
      setError(null)
      console.log('Fetching sales from API...')
      const params: any = {}
      if (selectedStoreId !== 'all') params.store_id = selectedStoreId
      
      const response = await api.get('/sales/', { params })
      console.log('Sales data received:', response.data)
      setSales(response.data)
      toast.success(`Loaded ${response.data.length} sales transactions`)
    } catch (error: any) {
      console.error('Sales API error:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to load sales'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const filteredSales = sales.filter(
    (sale) =>
      sale.invoice_number.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Calculate stats
  const todaySales = sales.filter(sale => {
    const saleDate = new Date(sale.sale_date)
    const today = new Date()
    return saleDate.toDateString() === today.toDateString()
  })

  const totalAmount = sales.reduce((sum, sale) => sum + sale.total_amount, 0)
  const todayAmount = todaySales.reduce((sum, sale) => sum + sale.total_amount, 0)

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 space-y-4">
        <div className="loading-spinner w-16 h-16"></div>
        <p className="text-neutral-600 font-medium">Loading sales data...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h1 className="text-4xl font-black gradient-text flex items-center">
            <ShoppingCartIcon className="w-10 h-10 mr-3 text-primary" />
            Sales & POS
          </h1>
          <p className="text-neutral-600 mt-2 font-medium">
            Manage sales transactions and point of sale
          </p>
        </div>
        <div className="flex items-center gap-4">
          <StoreSelector
            selectedStoreId={selectedStoreId}
            onStoreChange={setSelectedStoreId}
            showAllOption={true}
          />
          <button
            onClick={() => setShowSaleModal(true)}
            className="btn btn-primary flex items-center space-x-2"
          >
            <PlusIcon className="w-5 h-5" />
            <span>New Sale</span>
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="stat-card bg-gradient-to-br from-blue-500 to-blue-600">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-blue-100 text-sm font-semibold mb-1">Total Sales</p>
              <p className="text-4xl font-black">{sales.length}</p>
              <p className="text-blue-100 text-sm mt-2">Transactions</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <ShoppingCartIcon className="w-8 h-8" />
            </div>
          </div>
        </div>
        
        <div className="stat-card bg-gradient-to-br from-green-500 to-emerald-600">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-green-100 text-sm font-semibold mb-1">Total Revenue</p>
              <p className="text-4xl font-black">₹{totalAmount.toFixed(0)}</p>
              <p className="text-green-100 text-sm mt-2">All Time</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <CurrencyDollarIcon className="w-8 h-8" />
            </div>
          </div>
        </div>
        
        <div className="stat-card bg-gradient-to-br from-purple-500 to-purple-600">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-purple-100 text-sm font-semibold mb-1">Today's Sales</p>
              <p className="text-4xl font-black">₹{todayAmount.toFixed(0)}</p>
              <p className="text-purple-100 text-sm mt-2">{todaySales.length} transactions</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <ClockIcon className="w-8 h-8" />
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="card bg-red-50 border-l-4 border-red-500">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-red-800">Error Loading Sales</h3>
              <p className="text-red-600 mt-1">{error}</p>
            </div>
            <button onClick={loadSales} className="btn btn-accent">
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="card">
        <div className="relative">
          <MagnifyingGlassIcon className="w-5 h-5 absolute left-4 top-1/2 transform -translate-y-1/2 text-neutral-400" />
          <input
            type="text"
            placeholder="Search by invoice number..."
            className="input pl-12"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Sales Table */}
      <div className="card overflow-hidden p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gradient-to-r from-primary to-primary-light text-white">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Invoice #
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Customer
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Items
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Payment
                </th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-neutral-100">
              {filteredSales.map((sale, index) => (
                <tr key={sale.id} className="table-row hover:shadow-md transition-all" style={{animationDelay: `${index * 0.05}s`}}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-mono text-sm font-bold text-primary">{sale.invoice_number}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600">
                    {format(new Date(sale.sale_date), 'MMM dd, yyyy HH:mm')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 font-medium">
                    {sale.customer_id ? 'Customer' : 'Walk-in'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600">
                    {sale.items?.length || 0} items
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-bold text-lg text-green-600">₹{sale.total_amount.toFixed(2)}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="badge badge-info uppercase">
                      {sale.payment_mode}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="badge badge-success capitalize">
                      {sale.payment_status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredSales.length === 0 && !error && (
          <div className="text-center py-16">
            <ShoppingCartIcon className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
            <p className="text-neutral-600 font-medium">No sales found</p>
            <button onClick={loadSales} className="btn btn-primary mt-4">
              Refresh Data
            </button>
          </div>
        )}
      </div>

      {/* New Sale Modal */}
      <Modal
        isOpen={showSaleModal}
        onClose={() => setShowSaleModal(false)}
        title="Create New Sale"
      >
        <SaleForm
          onSuccess={() => {
            setShowSaleModal(false)
            loadSales()
          }}
          onCancel={() => setShowSaleModal(false)}
        />
      </Modal>
    </div>
  )
}
