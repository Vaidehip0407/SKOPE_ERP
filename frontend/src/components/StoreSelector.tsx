import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'

interface Store {
  id: number
  name: string
}

interface StoreSelectorProps {
  selectedStoreId: number | 'all'
  onStoreChange: (storeId: number | 'all') => void
  showAllOption?: boolean
  label?: string
  className?: string
}

export default function StoreSelector({
  selectedStoreId,
  onStoreChange,
  showAllOption = true,
  label = 'Store:',
  className = ''
}: StoreSelectorProps) {
  const { user } = useAuthStore()
  const [stores, setStores] = useState<Store[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user?.role === 'super_admin') {
      loadStores()
    } else {
      setLoading(false)
    }
  }, [user])

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

  // Don't show selector if not super admin
  if (user?.role !== 'super_admin') {
    return null
  }

  if (loading) {
    return <div className="text-sm text-neutral-500">Loading stores...</div>
  }

  if (stores.length === 0) {
    return null
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {label && <label className="text-sm font-medium text-neutral-700">{label}</label>}
      <select
        value={selectedStoreId}
        onChange={(e) => onStoreChange(e.target.value === 'all' ? 'all' : parseInt(e.target.value))}
        className="input w-64"
      >
        {showAllOption && <option value="all">📊 All Stores</option>}
        {stores.map((store) => (
          <option key={store.id} value={store.id}>
            🏪 {store.name}
          </option>
        ))}
      </select>
    </div>
  )
}

