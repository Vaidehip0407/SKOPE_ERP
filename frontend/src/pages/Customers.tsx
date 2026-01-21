import { useEffect, useState } from 'react'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { Customer } from '../utils/types'
import { PlusIcon, MagnifyingGlassIcon, PhoneIcon, EnvelopeIcon } from '@heroicons/react/24/outline'
import Modal from '../components/Modal'
import CustomerForm from '../components/CustomerForm'
import StoreSelector from '../components/StoreSelector'

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>('all')

  useEffect(() => {
    loadCustomers()
  }, [selectedStoreId])

  const loadCustomers = async () => {
    try {
      const params: any = {}
      if (selectedStoreId !== 'all') params.store_id = selectedStoreId
      
      const response = await api.get('/customers/', { params })
      setCustomers(response.data)
    } catch (error) {
      toast.error('Failed to load customers')
    } finally {
      setLoading(false)
    }
  }

  const filteredCustomers = customers.filter(
    (customer) =>
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.phone.includes(searchTerm) ||
      (customer.email?.toLowerCase() || '').includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-neutral-600">Loading customers...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-primary">Customer Management</h1>
          <p className="text-neutral-600 mt-2">
            Manage customer information and purchase history
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
            Add Customer
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="card mb-6">
        <div className="relative">
          <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-400" />
          <input
            type="text"
            placeholder="Search customers by name, phone, or email..."
            className="input pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Customers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCustomers.map((customer) => (
          <div key={customer.id} className="card hover:shadow-lg transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-primary">{customer.name}</h3>
                <p className="text-sm text-neutral-600">
                  Customer ID: #{customer.id}
                </p>
              </div>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center text-sm text-neutral-600">
                <PhoneIcon className="w-4 h-4 mr-2" />
                {customer.phone}
              </div>
              {customer.email && (
                <div className="flex items-center text-sm text-neutral-600">
                  <EnvelopeIcon className="w-4 h-4 mr-2" />
                  {customer.email}
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-neutral-200">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-xs text-neutral-600">Total Purchases</p>
                  <p className="text-lg font-bold text-green-600">
                    ₹{customer.total_purchases.toFixed(2)}
                  </p>
                </div>
                <button className="btn btn-outline btn-sm">
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredCustomers.length === 0 && (
        <div className="card text-center py-12 text-neutral-600">
          No customers found
        </div>
      )}

      {/* Add Customer Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Customer"
      >
        <CustomerForm
          onSuccess={() => {
            setShowAddModal(false)
            loadCustomers()
          }}
          onCancel={() => setShowAddModal(false)}
        />
      </Modal>
    </div>
  )
}

