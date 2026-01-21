import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'

interface ProductFormProps {
  onSuccess: () => void
  onCancel: () => void
}

export default function ProductForm({ onSuccess, onCancel }: ProductFormProps) {
  const { user } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    sku: '',
    name: '',
    description: '',
    category: '',
    brand: '',
    unit_price: '',
    cost_price: '',
    gst_rate: '18',
    warranty_months: '0',
    current_stock: '',
    minimum_stock: '10',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/inventory/products', {
        ...formData,
        unit_price: parseFloat(formData.unit_price),
        cost_price: formData.cost_price ? parseFloat(formData.cost_price) : 0,
        gst_rate: parseFloat(formData.gst_rate),
        warranty_months: parseInt(formData.warranty_months),
        current_stock: parseInt(formData.current_stock),
        minimum_stock: parseInt(formData.minimum_stock),
        store_id: user?.store_id || 1,
      })
      toast.success('Product created successfully!')
      onSuccess()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create product')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">SKU *</label>
          <input
            type="text"
            required
            className="input"
            value={formData.sku}
            onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Product Name *</label>
          <input
            type="text"
            required
            className="input"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />
        </div>
      </div>

      <div>
        <label className="label">Description</label>
        <textarea
          className="input"
          rows={2}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Category</label>
          <input
            type="text"
            className="input"
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Brand</label>
          <input
            type="text"
            className="input"
            value={formData.brand}
            onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Unit Price *</label>
          <input
            type="number"
            step="0.01"
            required
            className="input"
            value={formData.unit_price}
            onChange={(e) => setFormData({ ...formData, unit_price: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Cost Price</label>
          <input
            type="number"
            step="0.01"
            className="input"
            value={formData.cost_price}
            onChange={(e) => setFormData({ ...formData, cost_price: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">GST Rate (%)</label>
          <input
            type="number"
            step="0.01"
            className="input"
            value={formData.gst_rate}
            onChange={(e) => setFormData({ ...formData, gst_rate: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Warranty (Months)</label>
          <input
            type="number"
            className="input"
            value={formData.warranty_months}
            onChange={(e) => setFormData({ ...formData, warranty_months: e.target.value })}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Current Stock *</label>
          <input
            type="number"
            required
            className="input"
            value={formData.current_stock}
            onChange={(e) => setFormData({ ...formData, current_stock: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Minimum Stock</label>
          <input
            type="number"
            className="input"
            value={formData.minimum_stock}
            onChange={(e) => setFormData({ ...formData, minimum_stock: e.target.value })}
          />
        </div>
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary flex-1"
        >
          {loading ? 'Creating...' : 'Create Product'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="btn btn-outline flex-1"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}

