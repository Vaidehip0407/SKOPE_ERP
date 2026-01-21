import { useState } from 'react'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { PaymentMode } from '../utils/types'

interface ExpenseFormProps {
  onSuccess: () => void
  onCancel: () => void
}

export default function ExpenseForm({ onSuccess, onCancel }: ExpenseFormProps) {
  const { user } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [uploadingFile, setUploadingFile] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [, setUploadedFilePath] = useState<string>('')
  const [formData, setFormData] = useState({
    category: 'petty_cash',
    description: '',
    amount: '',
    payment_mode: 'cash' as PaymentMode,
    vendor_name: '',
    receipt_number: '',
    voucher_file: '',
  })

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate file type
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'image/gif']
    if (!allowedTypes.includes(file.type)) {
      toast.error('Only PDF and image files are allowed')
      return
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size must be less than 5MB')
      return
    }

    setSelectedFile(file)

    // Upload file immediately
    setUploadingFile(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await api.post('/financial/expenses/upload-voucher', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setUploadedFilePath(response.data.file_path)
      setFormData(prev => ({ ...prev, voucher_file: response.data.file_path }))
      toast.success('Voucher uploaded successfully!', { icon: '📎' })
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to upload voucher')
      setSelectedFile(null)
    } finally {
      setUploadingFile(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/financial/expenses', {
        ...formData,
        amount: parseFloat(formData.amount),
        store_id: user?.store_id || 1,
      })
      toast.success('Expense recorded successfully!')
      onSuccess()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to record expense')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="label">Category *</label>
        <select
          required
          className="input"
          value={formData.category}
          onChange={(e) => setFormData({ ...formData, category: e.target.value })}
        >
          <option value="petty_cash">Petty Cash</option>
          <option value="vendor_payout">Vendor Payout</option>
          <option value="utilities">Utilities</option>
          <option value="rent">Rent</option>
          <option value="salary">Salary</option>
          <option value="maintenance">Maintenance</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label className="label">Description *</label>
        <textarea
          required
          className="input"
          rows={2}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Amount *</label>
          <input
            type="number"
            step="0.01"
            required
            className="input"
            value={formData.amount}
            onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Payment Mode *</label>
          <select
            required
            className="input"
            value={formData.payment_mode}
            onChange={(e) => setFormData({ ...formData, payment_mode: e.target.value as PaymentMode })}
          >
            <option value="cash">Cash</option>
            <option value="card">Card</option>
            <option value="upi">UPI</option>
            <option value="qr_code">QR Code</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">Vendor Name</label>
          <input
            type="text"
            className="input"
            value={formData.vendor_name}
            onChange={(e) => setFormData({ ...formData, vendor_name: e.target.value })}
          />
        </div>
        <div>
          <label className="label">Receipt Number</label>
          <input
            type="text"
            className="input"
            value={formData.receipt_number}
            onChange={(e) => setFormData({ ...formData, receipt_number: e.target.value })}
          />
        </div>
      </div>

      {/* Voucher Upload Section */}
      <div className="border-2 border-dashed border-primary/30 rounded-xl p-4 bg-primary/5">
        <label className="label flex items-center gap-2">
          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Upload Bill/Voucher (PDF or Image)
        </label>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg,.png,.gif"
          onChange={handleFileSelect}
          className="input mt-2"
          disabled={uploadingFile}
        />
        {uploadingFile && (
          <div className="mt-2 flex items-center gap-2 text-sm text-primary">
            <div className="loading-spinner w-4 h-4"></div>
            <span>Uploading voucher...</span>
          </div>
        )}
        {selectedFile && !uploadingFile && (
          <div className="mt-2 flex items-center gap-2 text-sm text-green-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="font-medium">{selectedFile.name}</span>
          </div>
        )}
        <p className="text-xs text-neutral-500 mt-2">
          Upload a copy of your expense bill for audit purposes. Max 5MB.
        </p>
      </div>

      <div className="flex gap-3 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="btn btn-primary flex-1"
        >
          {loading ? 'Recording...' : 'Record Expense'}
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

