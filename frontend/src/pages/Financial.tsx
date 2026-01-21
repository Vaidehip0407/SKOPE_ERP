import { useEffect, useState } from 'react'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { Expense } from '../utils/types'
import { PlusIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline'
import { format } from 'date-fns'
import Modal from '../components/Modal'
import ExpenseForm from '../components/ExpenseForm'
import StoreSelector from '../components/StoreSelector'

export default function Financial() {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [stats, setStats] = useState<any>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>('all')

  useEffect(() => {
    loadData()
  }, [selectedStoreId])

  const loadData = async () => {
    try {
      const params: any = {}
      if (selectedStoreId !== 'all') params.store_id = selectedStoreId
      
      const [expensesRes, statsRes] = await Promise.all([
        api.get('/financial/expenses', { params }),
        api.get('/financial/dashboard/stats', { params }),
      ])
      setExpenses(expensesRes.data)
      setStats(statsRes.data)
    } catch (error) {
      toast.error('Failed to load financial data')
    } finally {
      setLoading(false)
    }
  }

  const filteredExpenses = expenses.filter(
    (expense) =>
      expense.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      expense.category.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-neutral-600">Loading financial data...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-primary">Financial Management</h1>
          <p className="text-neutral-600 mt-2">
            Track expenses, revenue, and profitability
          </p>
        </div>
        <div className="flex items-center gap-4">
          <StoreSelector
            selectedStoreId={selectedStoreId}
            onStoreChange={setSelectedStoreId}
            showAllOption={true}
          />
          <button
            onClick={() => setShowAddModal(true)}
            className="btn btn-primary flex items-center"
          >
            <PlusIcon className="w-5 h-5 mr-2" />
            Add Expense
          </button>
        </div>
      </div>

      {/* Financial Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <p className="text-green-100">Monthly Revenue</p>
          <p className="text-3xl font-bold mt-2">
            ₹{stats?.month_revenue?.toFixed(2) || '0.00'}
          </p>
        </div>

        <div className="card bg-gradient-to-br from-red-500 to-red-600 text-white">
          <p className="text-red-100">Monthly Expenses</p>
          <p className="text-3xl font-bold mt-2">
            ₹{stats?.month_expenses?.toFixed(2) || '0.00'}
          </p>
        </div>

        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <p className="text-blue-100">Monthly Profit</p>
          <p className="text-3xl font-bold mt-2">
            ₹{stats?.month_profit?.toFixed(2) || '0.00'}
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="relative">
          <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-400" />
          <input
            type="text"
            placeholder="Search expenses..."
            className="input pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Expenses Table */}
      <div className="card overflow-hidden">
        <h2 className="text-xl font-bold text-primary mb-4 px-6 pt-6">
          Recent Expenses
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-50 border-b border-neutral-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-600 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-600 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-600 uppercase tracking-wider">
                  Description
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-600 uppercase tracking-wider">
                  Vendor
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-600 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-neutral-600 uppercase tracking-wider">
                  Payment
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-neutral-200">
              {filteredExpenses.map((expense) => (
                <tr key={expense.id} className="hover:bg-neutral-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600">
                    {format(new Date(expense.expense_date), 'MMM dd, yyyy')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800 capitalize">
                      {expense.category.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-neutral-900">
                    {expense.description}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600">
                    {expense.vendor_name || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-red-600">
                    ₹{expense.amount.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800 uppercase">
                      {expense.payment_mode}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredExpenses.length === 0 && (
          <div className="text-center py-12 text-neutral-600">
            No expenses found
          </div>
        )}
      </div>

      {/* Add Expense Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Record New Expense"
      >
        <ExpenseForm
          onSuccess={() => {
            setShowAddModal(false)
            loadData()
          }}
          onCancel={() => setShowAddModal(false)}
        />
      </Modal>
    </div>
  )
}

