export enum UserRole {
  SUPER_ADMIN = 'super_admin',
  STORE_MANAGER = 'store_manager',
  SALES_STAFF = 'sales_staff',
  MARKETING = 'marketing',
  ACCOUNTS = 'accounts',
}

export enum PaymentMode {
  CASH = 'cash',
  CARD = 'card',
  UPI = 'upi',
  QR_CODE = 'qr_code',
}

export interface Product {
  id: number
  sku: string
  name: string
  description?: string
  category?: string
  brand?: string
  unit_price: number
  cost_price?: number
  gst_rate: number
  image_url?: string
  warranty_months: number
  current_stock: number
  minimum_stock: number
  store_id: number
  is_active: boolean
  created_at: string
}

export interface Customer {
  id: number
  name: string
  email?: string
  phone: string
  address?: string
  gst_number?: string
  store_id: number
  total_purchases: number
  created_at: string
}

export interface SaleItem {
  product_id: number
  quantity: number
  unit_price: number
  serial_number?: string
}

export interface Sale {
  id: number
  invoice_number: string
  customer_id?: number
  store_id: number
  subtotal: number
  gst_amount: number
  discount: number
  total_amount: number
  payment_mode: PaymentMode
  payment_status: string
  sale_date: string
  items: SaleItem[]
}

export interface Expense {
  id: number
  store_id: number
  category: string
  description: string
  amount: number
  payment_mode: PaymentMode
  vendor_name?: string
  receipt_number?: string
  expense_date: string
  created_at: string
}

export interface Store {
  id: number
  name: string
  address?: string
  phone?: string
  email?: string
  gst_number?: string
  is_active: boolean
  created_at: string
}

