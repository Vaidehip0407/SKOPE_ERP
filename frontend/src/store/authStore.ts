import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface User {
  id: number
  email: string
  username: string
  full_name: string | null
  role: string
  store_id: number | null
  is_active: boolean
  created_at: string
}

interface AuthState {
  user: User | null
  token: string | null
  setAuth: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, token) => {
        // Save to zustand store
        set({ user, token })
        // Also save to localStorage for compatibility
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
      },
      logout: () => {
        // Clear zustand store
        set({ user: null, token: null })
        // Also clear localStorage
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)

