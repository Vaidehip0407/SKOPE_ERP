import { useState, useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import Modal from '../components/Modal'
import {
  BuildingStorefrontIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  PhoneIcon,
  EnvelopeIcon,
  MapPinIcon,
} from '@heroicons/react/24/outline'

interface Store {
  id: number
  name: string
  address?: string
  phone?: string
  email?: string
  gst_number?: string
  is_active: boolean
  created_at: string
}

interface StoreStats {
  store_id: number
  store_name: string
  total_products: number
  total_sales: number
  total_customers: number
  total_users: number
}

export default function Stores() {
  const { user } = useAuthStore()
  const [stores, setStores] = useState<Store[]>([])
  const [storeStats, setStoreStats] = useState<StoreStats[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingStore, setEditingStore] = useState<Store | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    phone: '',
    email: '',
    gst_number: ''
  })

  useEffect(() => {
    loadStores()
    loadStoreStats()
  }, [])

  const loadStores = async () => {
    try {
      const response = await api.get('/stores/')
      setStores(response.data)
    } catch (error) {
      console.error('Error loading stores:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadStoreStats = async () => {
    try {
      const response = await api.get('/stores/stats')
      setStoreStats(response.data)
    } catch (error) {
      console.error('Error loading store stats:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingStore) {
        await api.put(`/stores/${editingStore.id}`, formData)
      } else {
        await api.post('/stores/', formData)
      }
      setShowModal(false)
      resetForm()
      loadStores()
      loadStoreStats()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error saving store')
    }
  }

  const handleEdit = (store: Store) => {
    setEditingStore(store)
    setFormData({
      name: store.name,
      address: store.address || '',
      phone: store.phone || '',
      email: store.email || '',
      gst_number: store.gst_number || ''
    })
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to deactivate this store?')) return
    
    try {
      await api.delete(`/stores/${id}`)
      loadStores()
      loadStoreStats()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error deleting store')
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      address: '',
      phone: '',
      email: '',
      gst_number: ''
    })
    setEditingStore(null)
  }

  const getStoreStats = (storeId: number) => {
    return storeStats.find(s => s.store_id === storeId)
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading...</div>
  }

  // Only Super Admin can access
  if (user?.role !== 'super_admin') {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-2">Access Denied</h2>
          <p className="text-neutral-600">Only Super Admin can manage stores.</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-primary">Store Management</h1>
          <p className="text-neutral-600 mt-2">Manage multiple stores and view analytics</p>
        </div>
        <button
          onClick={() => {
            resetForm()
            setShowModal(true)
          }}
          className="btn btn-primary flex items-center gap-2"
        >
          <PlusIcon className="w-5 h-5" />
          Add New Store
        </button>
      </div>

      {/* Store Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <h3 className="text-sm font-medium text-blue-100">Total Stores</h3>
          <p className="text-3xl font-bold mt-2">{stores.length}</p>
        </div>
        <div className="card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <h3 className="text-sm font-medium text-green-100">Total Revenue</h3>
          <p className="text-3xl font-bold mt-2">
            ₹{storeStats.reduce((sum, s) => sum + s.total_sales, 0).toLocaleString()}
          </p>
        </div>
        <div className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <h3 className="text-sm font-medium text-purple-100">Total Products</h3>
          <p className="text-3xl font-bold mt-2">
            {storeStats.reduce((sum, s) => sum + s.total_products, 0)}
          </p>
        </div>
        <div className="card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
          <h3 className="text-sm font-medium text-orange-100">Total Users</h3>
          <p className="text-3xl font-bold mt-2">
            {storeStats.reduce((sum, s) => sum + s.total_users, 0)}
          </p>
        </div>
      </div>

      {/* Stores Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stores.map((store) => {
          const stats = getStoreStats(store.id)
          return (
            <div key={store.id} className="card hover:shadow-2xl transition-all duration-300">
              {/* Store Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary to-primary-dark rounded-xl flex items-center justify-center">
                    <BuildingStorefrontIcon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-primary">{store.name}</h3>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      store.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {store.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(store)}
                    className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Edit"
                  >
                    <PencilIcon className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(store.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <TrashIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Store Details */}
              <div className="space-y-2 mb-4 text-sm">
                {store.address && (
                  <div className="flex items-start gap-2 text-neutral-600">
                    <MapPinIcon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    <span>{store.address}</span>
                  </div>
                )}
                {store.phone && (
                  <div className="flex items-center gap-2 text-neutral-600">
                    <PhoneIcon className="w-4 h-4" />
                    <span>{store.phone}</span>
                  </div>
                )}
                {store.email && (
                  <div className="flex items-center gap-2 text-neutral-600">
                    <EnvelopeIcon className="w-4 h-4" />
                    <span>{store.email}</span>
                  </div>
                )}
                {store.gst_number && (
                  <div className="text-neutral-600">
                    <span className="font-medium">GST:</span> {store.gst_number}
                  </div>
                )}
              </div>

              {/* Store Stats */}
              {stats && (
                <div className="pt-4 border-t border-neutral-200">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-neutral-500">Products</p>
                      <p className="text-lg font-bold text-primary">{stats.total_products}</p>
                    </div>
                    <div>
                      <p className="text-xs text-neutral-500">Revenue</p>
                      <p className="text-lg font-bold text-green-600">₹{stats.total_sales.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-xs text-neutral-500">Customers</p>
                      <p className="text-lg font-bold text-primary">{stats.total_customers}</p>
                    </div>
                    <div>
                      <p className="text-xs text-neutral-500">Users</p>
                      <p className="text-lg font-bold text-primary">{stats.total_users}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* No Stores Message */}
      {stores.length === 0 && (
        <div className="text-center py-12">
          <BuildingStorefrontIcon className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-neutral-700 mb-2">No Stores Yet</h3>
          <p className="text-neutral-500 mb-4">Get started by adding your first store</p>
          <button
            onClick={() => setShowModal(true)}
            className="btn btn-primary"
          >
            <PlusIcon className="w-5 h-5 mr-2" />
            Add Store
          </button>
        </div>
      )}

      {/* Add/Edit Store Modal */}
      <Modal
        isOpen={showModal}
        onClose={() => {
          setShowModal(false)
          resetForm()
        }}
        title={editingStore ? 'Edit Store' : 'Add New Store'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Store Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="input"
              required
            />
          </div>

          <div>
            <label className="label">Address</label>
            <textarea
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              className="input"
              rows={3}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Phone</label>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="input"
              />
            </div>
            <div>
              <label className="label">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="input"
              />
            </div>
          </div>

          <div>
            <label className="label">GST Number</label>
            <input
              type="text"
              value={formData.gst_number}
              onChange={(e) => setFormData({ ...formData, gst_number: e.target.value })}
              className="input"
              placeholder="e.g., 22AAAAA0000A1Z5"
            />
          </div>

          <div className="flex gap-3 justify-end pt-4">
            <button
              type="button"
              onClick={() => {
                setShowModal(false)
                resetForm()
              }}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingStore ? 'Update Store' : 'Create Store'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  )
}

