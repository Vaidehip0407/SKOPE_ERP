import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'

interface CustomerFormProps {
  onSuccess: () => void
  onCancel: () => void
}

export default function CustomerForm({ onSuccess, onCancel }: CustomerFormProps) {
  const { user } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    gst_number: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/customers/', {
        ...formData,
        store_id: user?.store_id || 1,
      })
      toast.success('Customer created successfully!')
      onSuccess()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create customer')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="label">Customer Name *</label>
        <input
          type="text"
          required
          className="input"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        />
      </div>

      <div>
        <label className="label">Phone *</label>
        <input
          type="tel"
          required
          className="input"
          value={formData.phone}
          onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
          placeholder="+1234567890"
        />
      </div>

      <div>
        <label className="label">Email</label>
        <input
          type="email"
          className="input"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        />
      </div>

      <div>
        <label className="label">Address</label>
        <textarea
          className="input"
          rows={3}
          value={formData.address}
          onChange={(e) => setFormData({ ...formData, address: e.target.value })}
        />
      </div>

      <div>
        <label className="label">GST Number</label>
        <input
          type="text"
          className="input"
          value={formData.gst_number}
          onChange={(e) => setFormData({ ...formData, gst_number: e.target.value })}
        />
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary flex-1"
        >
          {loading ? 'Creating...' : 'Create Customer'}
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

