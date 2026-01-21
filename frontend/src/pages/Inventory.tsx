import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { Product } from '../utils/types'
import { PlusIcon, PencilIcon, MagnifyingGlassIcon, CubeIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import Modal from '../components/Modal'
import ProductForm from '../components/ProductForm'
import StoreSelector from '../components/StoreSelector'

export default function Inventory() {
  const { user } = useAuthStore()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [showLowStock, setShowLowStock] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>('all')

  useEffect(() => {
    loadProducts()
  }, [showLowStock, selectedStoreId])

  const loadProducts = async () => {
    try {
      const params: any = {}
      if (showLowStock) params.low_stock = true
      if (selectedStoreId !== 'all') params.store_id = selectedStoreId
      
      const response = await api.get('/inventory/products', { params })
      setProducts(response.data)
    } catch (error) {
      toast.error('Failed to load products')
    } finally {
      setLoading(false)
    }
  }

  const filteredProducts = products.filter(
    (product) =>
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (product.category?.toLowerCase() || '').includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 space-y-4">
        <div className="loading-spinner w-16 h-16"></div>
        <p className="text-neutral-600 font-medium">Loading inventory...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with gradient */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h1 className="text-4xl font-black gradient-text flex items-center">
            <CubeIcon className="w-10 h-10 mr-3 text-primary" />
            Inventory Management
          </h1>
          <p className="text-neutral-600 mt-2 font-medium">
            Manage your product catalog and stock levels
          </p>
        </div>
        <div className="flex items-center gap-4">
          <StoreSelector
            selectedStoreId={selectedStoreId}
            onStoreChange={setSelectedStoreId}
            showAllOption={true}
          />
          {(user?.role === 'super_admin' || user?.role === 'store_manager') && (
            <button
              onClick={() => setShowAddModal(true)}
              className="btn btn-primary flex items-center space-x-2"
            >
              <PlusIcon className="w-5 h-5" />
              <span>Add Product</span>
            </button>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="stat-card bg-gradient-to-br from-blue-500 to-blue-600">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-blue-100 text-sm font-semibold mb-1">Total Products</p>
              <p className="text-4xl font-black">{products.length}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <CubeIcon className="w-8 h-8" />
            </div>
          </div>
        </div>
        
        <div className="stat-card bg-gradient-to-br from-yellow-500 to-orange-500">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-yellow-100 text-sm font-semibold mb-1">Low Stock Items</p>
              <p className="text-4xl font-black">{products.filter(p => p.current_stock <= p.minimum_stock).length}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <ExclamationTriangleIcon className="w-8 h-8" />
            </div>
          </div>
        </div>
        
        <div className="stat-card bg-gradient-to-br from-green-500 to-emerald-600">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-green-100 text-sm font-semibold mb-1">In Stock</p>
              <p className="text-4xl font-black">{products.filter(p => p.current_stock > p.minimum_stock).length}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <CubeIcon className="w-8 h-8" />
            </div>
          </div>
        </div>
      </div>

      {/* Filters Card */}
      <div className="card">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="w-5 h-5 absolute left-4 top-1/2 transform -translate-y-1/2 text-neutral-400" />
            <input
              type="text"
              placeholder="Search products by name, SKU, or category..."
              className="input pl-12"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <label className="flex items-center space-x-3 px-5 py-3 bg-gradient-to-r from-primary/10 to-accent/10 rounded-xl cursor-pointer hover:from-primary/20 hover:to-accent/20 transition-all">
            <input
              type="checkbox"
              checked={showLowStock}
              onChange={(e) => setShowLowStock(e.target.checked)}
              className="w-5 h-5 rounded accent-primary cursor-pointer"
            />
            <span className="font-semibold text-primary">Show Low Stock Only</span>
          </label>
        </div>
      </div>

      {/* Products Table */}
      <div className="card overflow-hidden p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gradient-to-r from-primary to-primary-light text-white">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">SKU</th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Product Name</th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Category</th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Price</th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Stock</th>
                <th className="px-6 py-4 text-left text-xs font-bold uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-right text-xs font-bold uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-neutral-100">
              {filteredProducts.map((product, index) => (
                <tr key={product.id} className="table-row hover:shadow-md transition-all" style={{animationDelay: `${index * 0.05}s`}}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-mono text-sm font-bold text-primary">{product.sku}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div>
                      <div className="font-semibold text-neutral-900">{product.name}</div>
                      {product.brand && (
                        <div className="text-sm text-neutral-500">{product.brand}</div>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="badge badge-info">{product.category || 'Uncategorized'}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-bold text-lg text-green-600">₹{product.unit_price.toFixed(2)}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="font-bold text-neutral-900">{product.current_stock}</div>
                      <div className="text-xs text-neutral-500">Min: {product.minimum_stock}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {product.current_stock === 0 ? (
                      <span className="badge badge-danger">Out of Stock</span>
                    ) : product.current_stock <= product.minimum_stock ? (
                      <span className="badge badge-warning">Low Stock</span>
                    ) : (
                      <span className="badge badge-success">In Stock</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button className="p-2 text-primary hover:bg-primary/10 rounded-lg transition-all hover:scale-110">
                      <PencilIcon className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-16">
            <CubeIcon className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
            <p className="text-neutral-600 font-medium">No products found</p>
          </div>
        )}
      </div>

      {/* Add Product Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Add New Product"
      >
        <ProductForm
          onSuccess={() => {
            setShowAddModal(false)
            loadProducts()
          }}
          onCancel={() => setShowAddModal(false)}
        />
      </Modal>
    </div>
  )
}
