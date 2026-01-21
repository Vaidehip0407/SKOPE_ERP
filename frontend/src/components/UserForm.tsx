import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { UserRole } from '../utils/types'

interface UserFormProps {
  onSuccess: () => void
  onCancel: () => void
}

export default function UserForm({ onSuccess, onCancel }: UserFormProps) {
  const { user } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    password: '',
    role: 'sales_staff' as UserRole,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/users/', {
        ...formData,
        store_id: user?.store_id || 1,
      })
      toast.success('User created successfully!')
      onSuccess()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create user')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="label">Full Name *</label>
        <input
          type="text"
          required
          className="input"
          value={formData.full_name}
          onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Username *</label>
          <input
            type="text"
            required
            className="input"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Email *</label>
          <input
            type="email"
            required
            className="input"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
        </div>
      </div>

      <div>
        <label className="label">Password *</label>
        <input
          type="password"
          required
          className="input"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          minLength={6}
        />
      </div>

      <div>
        <label className="label">Role *</label>
        <select
          required
          className="input"
          value={formData.role}
          onChange={(e) => setFormData({ ...formData, role: e.target.value as UserRole })}
        >
          <option value="sales_staff">Sales Staff</option>
          <option value="store_manager">Store Manager</option>
          <option value="accounts">Accounts</option>
          <option value="marketing">Marketing</option>
          {user?.role === 'super_admin' && (
            <option value="super_admin">Super Admin</option>
          )}
        </select>
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary flex-1"
        >
          {loading ? 'Creating...' : 'Create User'}
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

