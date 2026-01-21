import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { LockClosedIcon, UserIcon } from '@heroicons/react/24/outline'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await api.post('/auth/login', { username, password })
      const { access_token, user } = response.data

      setAuth(user, access_token)
      toast.success('Welcome back! 🎉', {
        icon: '👋',
        style: {
          borderRadius: '10px',
          background: '#1D3557',
          color: '#fff',
        },
      })
      navigate('/')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed', {
        icon: '❌',
        style: {
          borderRadius: '10px',
          background: '#E63946',
          color: '#fff',
        },
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary via-primary-dark to-primary-light relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-accent/20 to-transparent rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-secondary/20 to-transparent rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md px-6">
        <div className="bg-white/95 backdrop-blur-2xl rounded-3xl shadow-2xl p-10 border-2 border-white/50 hover:shadow-3xl transition-all duration-500 slide-in">
          {/* Logo Section */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-2xl mb-4 floating">
              <span className="text-4xl font-black text-white">S</span>
            </div>
            <h1 className="text-4xl font-black gradient-text mb-2">SKOPE ERP</h1>
            <p className="text-neutral-600 font-medium">Business Management System</p>
            <div className="mt-2 h-1 w-20 bg-gradient-to-r from-primary via-accent to-primary-light rounded-full mx-auto"></div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="username" className="label flex items-center">
                <UserIcon className="w-4 h-4 mr-2 text-primary" />
                Username
              </label>
              <div className="relative">
                <input
                  id="username"
                  type="text"
                  required
                  className="input pl-12"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter your username"
                />
                <UserIcon className="w-5 h-5 absolute left-4 top-1/2 transform -translate-y-1/2 text-neutral-400" />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="label flex items-center">
                <LockClosedIcon className="w-4 h-4 mr-2 text-primary" />
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type="password"
                  required
                  className="input pl-12"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                />
                <LockClosedIcon className="w-5 h-5 absolute left-4 top-1/2 transform -translate-y-1/2 text-neutral-400" />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary w-full text-lg font-bold py-4 disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group"
            >
              <span className="relative z-10">
                {loading ? (
                  <span className="flex items-center justify-center">
                    <div className="loading-spinner w-5 h-5 mr-2"></div>
                    Logging in...
                  </span>
                ) : (
                  'Login to Dashboard'
                )}
              </span>
              {!loading && (
                <div className="absolute inset-0 bg-gradient-to-r from-accent to-accent-light opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-8 p-5 bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl border-2 border-blue-100">
            <p className="text-sm font-bold text-primary mb-3 flex items-center">
              <span className="w-2 h-2 bg-accent rounded-full mr-2 animate-pulse"></span>
              Demo Credentials:
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between items-center p-2 bg-white/70 rounded-lg">
                <span className="font-semibold text-neutral-700">Admin:</span>
                <code className="font-mono text-xs bg-primary/10 px-3 py-1 rounded">admin@store.com / admin123</code>
              </div>
              <div className="flex justify-between items-center p-2 bg-white/70 rounded-lg">
                <span className="font-semibold text-neutral-700">Manager:</span>
                <code className="font-mono text-xs bg-primary/10 px-3 py-1 rounded">manager@store.com / manager123</code>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-xs text-neutral-500">
              Secure Enterprise Grade Platform
            </p>
          </div>
        </div>

        {/* Version Badge */}
        <div className="text-center mt-6">
          <span className="inline-block px-4 py-2 bg-white/20 backdrop-blur-lg text-white text-xs font-semibold rounded-full border border-white/30">
            SKOPE ERP v1.0.0
          </span>
        </div>
      </div>
    </div>
  )
}
