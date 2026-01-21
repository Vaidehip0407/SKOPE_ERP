import { useState, useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { TrashIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline'

interface Product {
  id: number
  name: string
  sku: string
  unit_price: number
  current_stock: number
  gst_rate: number
}

interface Customer {
  id: number
  name: string
  phone: string
}

interface SaleItem {
  product_id: number
  product_name?: string
  quantity: number
  unit_price: number
  gst_rate: number
}

interface SaleFormProps {
  onSuccess: () => void
  onCancel: () => void
}

interface Store {
  id: number
  name: string
}

export default function SaleForm({ onSuccess, onCancel }: SaleFormProps) {
  const { user } = useAuthStore()
  const [products, setProducts] = useState<Product[]>([])
  const [customers, setCustomers] = useState<Customer[]>([])
  const [stores, setStores] = useState<Store[]>([])
  const [loading, setLoading] = useState(true)

  const [selectedStore, setSelectedStore] = useState<number>(user?.store_id || 0)
  const [selectedCustomer, setSelectedCustomer] = useState<number | null>(null)
  const [items, setItems] = useState<SaleItem[]>([])
  const [discount, setDiscount] = useState(0)
  const [paymentMode, setPaymentMode] = useState<'cash' | 'card' | 'upi' | 'qr_code'>('cash')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const requests = [
        api.get('/inventory/products'),
        api.get('/customers/')
      ]

      // Load stores if super admin
      if (user?.role === 'super_admin') {
        requests.push(api.get('/stores/'))
      }

      const responses = await Promise.all(requests)
      setProducts(responses[0].data.filter((p: Product) => p.current_stock > 0))
      setCustomers(responses[1].data)

      if (user?.role === 'super_admin' && responses[2]) {
        setStores(responses[2].data)
        if (responses[2].data.length > 0 && !selectedStore) {
          setSelectedStore(responses[2].data[0].id)
        }
      }
    } catch (error) {
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.sku.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const addItem = (product: Product) => {
    const existingItem = items.find(item => item.product_id === product.id)

    if (existingItem) {
      if (existingItem.quantity >= product.current_stock) {
        toast.error('Insufficient stock')
        return
      }
      setItems(items.map(item =>
        item.product_id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ))
    } else {
      setItems([...items, {
        product_id: product.id,
        product_name: product.name,
        quantity: 1,
        unit_price: product.unit_price,
        gst_rate: product.gst_rate
      }])
    }
    setSearchTerm('')
  }

  const updateQuantity = (productId: number, quantity: number) => {
    const product = products.find(p => p.id === productId)
    if (!product) return

    if (quantity > product.current_stock) {
      toast.error('Insufficient stock')
      return
    }

    if (quantity <= 0) {
      removeItem(productId)
      return
    }

    setItems(items.map(item =>
      item.product_id === productId
        ? { ...item, quantity }
        : item
    ))
  }

  const removeItem = (productId: number) => {
    setItems(items.filter(item => item.product_id !== productId))
  }

  const calculateTotals = () => {
    let subtotal = 0
    let gstAmount = 0

    items.forEach(item => {
      const itemTotal = item.unit_price * item.quantity
      const itemGst = (itemTotal * item.gst_rate) / 100
      subtotal += itemTotal
      gstAmount += itemGst
    })

    const total = subtotal + gstAmount - discount

    return { subtotal, gstAmount, total }
  }

  const { subtotal, gstAmount, total } = calculateTotals()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (items.length === 0) {
      toast.error('Please add at least one product')
      return
    }

    if (user?.role === 'super_admin' && !selectedStore) {
      toast.error('Please select a store')
      return
    }

    try {
      await api.post('/sales/', {
        customer_id: selectedCustomer,
        store_id: selectedStore || user?.store_id || 1,
        items: items.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          unit_price: item.unit_price
        })),
        discount,
        payment_mode: paymentMode
      })

      toast.success('Sale created successfully!')
      onSuccess()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create sale')
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Store Selection (Super Admin Only) */}
      {user?.role === 'super_admin' && (
        <div>
          <label className="label font-bold">🏪 Store *</label>
          <select
            value={selectedStore}
            onChange={(e) => setSelectedStore(parseInt(e.target.value))}
            className="input border-2 border-primary"
            required
          >
            <option value="">Select Store</option>
            {stores.map(store => (
              <option key={store.id} value={store.id}>
                {store.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Customer Selection */}
      <div>
        <label className="label">Customer (Optional)</label>
        <select
          value={selectedCustomer || ''}
          onChange={(e) => setSelectedCustomer(Number(e.target.value) || null)}
          className="input"
        >
          <option value="">Walk-in Customer</option>
          {customers.map(customer => (
            <option key={customer.id} value={customer.id}>
              {customer.name} - {customer.phone}
            </option>
          ))}
        </select>
      </div>

      {/* Product Search and Selection */}
      <div>
        <label className="label">Add Products</label>
        <div className="relative">
          <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-400" />
          <input
            type="text"
            placeholder="Search products by name or SKU..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input pl-10"
          />
        </div>

        {/* Product Search Results */}
        {searchTerm && filteredProducts.length > 0 && (
          <div className="mt-2 border border-neutral-200 rounded-lg max-h-48 overflow-y-auto">
            {filteredProducts.slice(0, 10).map(product => (
              <button
                key={product.id}
                type="button"
                onClick={() => addItem(product)}
                className="w-full text-left px-4 py-3 hover:bg-neutral-50 border-b border-neutral-100 last:border-b-0 transition-colors"
              >
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-medium text-primary">{product.name}</p>
                    <p className="text-sm text-neutral-500">{product.sku}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-green-600">₹{product.unit_price}</p>
                    <p className="text-xs text-neutral-500">Stock: {product.current_stock}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Selected Items */}
      {items.length > 0 && (
        <div>
          <label className="label">Selected Items</label>
          <div className="border border-neutral-200 rounded-lg divide-y">
            {items.map(item => (
              <div key={item.product_id} className="p-4 flex items-center gap-4">
                <div className="flex-1">
                  <p className="font-medium">{item.product_name}</p>
                  <p className="text-sm text-neutral-500">₹{item.unit_price} × {item.quantity}</p>
                </div>
                <div className="flex items-center gap-3">
                  <input
                    type="number"
                    min="1"
                    value={item.quantity}
                    onChange={(e) => updateQuantity(item.product_id, parseInt(e.target.value) || 0)}
                    className="input w-20 text-center"
                  />
                  <p className="font-bold text-primary w-24 text-right">
                    ₹{(item.unit_price * item.quantity).toFixed(2)}
                  </p>
                  <button
                    type="button"
                    onClick={() => removeItem(item.product_id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <TrashIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Payment Details */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Discount (₹)</label>
          <input
            type="number"
            min="0"
            step="0.01"
            value={discount}
            onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
            className="input"
          />
        </div>
        <div>
          <label className="label">Payment Mode *</label>
          <select
            value={paymentMode}
            onChange={(e) => setPaymentMode(e.target.value as any)}
            className="input"
            required
          >
            <option value="cash">Cash</option>
            <option value="card">Card</option>
            <option value="upi">UPI</option>
            <option value="qr_code">QR Code</option>
          </select>
        </div>
      </div>

      {/* Totals */}
      {items.length > 0 && (
        <div className="bg-neutral-50 p-4 rounded-lg space-y-2">
          <div className="flex justify-between text-neutral-700">
            <span>Subtotal:</span>
            <span className="font-medium">₹{subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-neutral-700">
            <span>GST:</span>
            <span className="font-medium">₹{gstAmount.toFixed(2)}</span>
          </div>
          {discount > 0 && (
            <div className="flex justify-between text-red-600">
              <span>Discount:</span>
              <span className="font-medium">-₹{discount.toFixed(2)}</span>
            </div>
          )}
          <div className="flex justify-between text-lg font-bold text-primary pt-2 border-t border-neutral-300">
            <span>Total:</span>
            <span>₹{total.toFixed(2)}</span>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3 justify-end pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="btn btn-secondary"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={items.length === 0}
          className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Complete Sale
        </button>
      </div>
    </form>
  )
}

