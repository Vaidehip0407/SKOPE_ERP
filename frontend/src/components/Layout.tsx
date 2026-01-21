import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import {
  HomeIcon,
  CubeIcon,
  ShoppingCartIcon,
  UsersIcon,
  CurrencyDollarIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  MegaphoneIcon,
  BuildingStorefrontIcon,
  ChartBarIcon,
  RocketLaunchIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline'
import { useState } from 'react'
import Chatbot from './Chatbot'

const navigation = [
  {
    name: 'Dashboard',
    href: '/',
    icon: HomeIcon,
    roles: ['super_admin', 'store_manager', 'sales_staff', 'marketing', 'accounts']
  },
  {
    name: 'Stores',
    href: '/stores',
    icon: BuildingStorefrontIcon,
    roles: ['super_admin']
  },
  {
    name: 'Inventory',
    href: '/inventory',
    icon: CubeIcon,
    roles: ['super_admin', 'store_manager', 'sales_staff', 'accounts']
  },
  {
    name: 'Sales',
    href: '/sales',
    icon: ShoppingCartIcon,
    roles: ['super_admin', 'store_manager', 'sales_staff', 'accounts']
  },
  {
    name: 'Customers',
    href: '/customers',
    icon: UsersIcon,
    roles: ['super_admin', 'store_manager', 'sales_staff', 'marketing', 'accounts']
  },
  {
    name: 'Financial',
    href: '/financial',
    icon: CurrencyDollarIcon,
    roles: ['super_admin', 'store_manager', 'accounts']
  },
  {
    name: 'Marketing',
    href: '/marketing',
    icon: MegaphoneIcon,
    roles: ['super_admin', 'store_manager', 'marketing']
  },
  {
    name: 'Ad Integrations',
    href: '/ad-integrations',
    icon: RocketLaunchIcon,
    roles: ['super_admin', 'store_manager', 'marketing']
  },
  {
    name: 'AI Insights',
    href: '/ai-insights',
    icon: SparklesIcon,
    roles: ['super_admin', 'store_manager', 'marketing', 'accounts']
  },
  {
    name: 'Reports',
    href: '/reports',
    icon: DocumentTextIcon,
    roles: ['super_admin', 'store_manager', 'accounts']
  },
  {
    name: 'Advanced Reports',
    href: '/advanced-reports',
    icon: ChartBarIcon,
    roles: ['super_admin', 'store_manager', 'accounts']
  },
  {
    name: 'Users',
    href: '/users',
    icon: UserGroupIcon,
    roles: ['super_admin', 'store_manager']
  },
]

export default function Layout() {
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  const filteredNavigation = navigation.filter(
    (item) => !item.roles || item.roles.includes(user?.role || '')
  )

  return (
    <div className="flex h-screen bg-gradient-to-br from-neutral-50 via-blue-50 to-neutral-100">
      {/* Sidebar for desktop */}
      <div className="hidden lg:flex lg:flex-col lg:w-72 bg-gradient-to-b from-primary via-primary-dark to-primary text-white shadow-2xl">
        {/* Logo Section */}
        <div className="p-8 border-b border-white/10 bg-white/5 backdrop-blur-sm">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg floating">
              <span className="text-2xl font-black text-white">S</span>
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight">SKOPE ERP</h1>
              <p className="text-xs text-secondary-light font-medium">Business Management</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {filteredNavigation.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-5 py-4 rounded-xl transition-all duration-300 group relative overflow-hidden ${isActive
                  ? 'bg-white/20 text-white shadow-xl scale-105'
                  : 'text-secondary-light hover:bg-white/10 hover:text-white hover:scale-102'
                  }`}
              >
                {isActive && (
                  <div className="absolute inset-0 bg-gradient-to-r from-accent/30 to-transparent rounded-xl"></div>
                )}
                <Icon className={`w-6 h-6 mr-4 relative z-10 ${isActive ? 'animate-pulse' : 'group-hover:scale-110 transition-transform'}`} />
                <span className="font-semibold relative z-10">{item.name}</span>
                {isActive && (
                  <div className="absolute right-0 top-1/2 transform -translate-y-1/2 w-1 h-8 bg-accent rounded-l-full"></div>
                )}
              </Link>
            )
          })}
        </nav>

        {/* User Profile Section */}
        <div className="p-4 border-t border-white/10 bg-white/5 backdrop-blur-sm">
          <div className="mb-4 p-4 rounded-xl bg-white/10 backdrop-blur-lg border border-white/20">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-12 h-12 bg-gradient-to-br from-accent to-accent-light rounded-full flex items-center justify-center shadow-lg font-bold text-lg">
                {(user?.full_name || user?.username || 'U').charAt(0).toUpperCase()}
              </div>
              <div className="flex-1">
                <p className="font-semibold text-white">{user?.full_name || user?.username}</p>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${user?.role === 'super_admin' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30' :
                    user?.role === 'store_manager' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' :
                      'bg-gray-500/20 text-gray-300 border border-gray-500/30'
                    }`}>
                    {user?.role === 'super_admin' ? '👑 Admin' :
                      user?.role === 'store_manager' ? '📊 Manager' :
                        user?.role === 'sales_staff' ? '🛒 Sales' :
                          user?.role === 'marketing' ? '📢 Marketing' :
                            user?.role === 'accounts' ? '💰 Accounts' :
                              user?.role?.replace('_', ' ')}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center w-full px-5 py-3 rounded-xl text-secondary-light hover:bg-accent hover:text-white transition-all duration-300 font-semibold group"
          >
            <ArrowRightOnRectangleIcon className="w-5 h-5 mr-3 group-hover:translate-x-1 transition-transform" />
            Logout
          </button>
        </div>
      </div>

      {/* Mobile sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setSidebarOpen(false)}></div>
          <div className="fixed inset-y-0 left-0 w-72 bg-gradient-to-b from-primary via-primary-dark to-primary text-white shadow-2xl slide-in">
            <div className="p-6 flex justify-between items-center border-b border-white/10">
              <h1 className="text-2xl font-black">SKOPE ERP</h1>
              <button onClick={() => setSidebarOpen(false)}>
                <XMarkIcon className="w-6 h-6" />
              </button>
            </div>
            <nav className="p-4 space-y-2">
              {filteredNavigation.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setSidebarOpen(false)}
                    className="flex items-center px-5 py-4 rounded-xl hover:bg-white/10 transition-all"
                  >
                    <Icon className="w-6 h-6 mr-4" />
                    {item.name}
                  </Link>
                )
              })}
            </nav>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Mobile header */}
        <div className="lg:hidden bg-white/80 backdrop-blur-xl shadow-lg p-4 sticky top-0 z-40 border-b border-neutral-200">
          <div className="flex items-center justify-between">
            <button onClick={() => setSidebarOpen(true)}>
              <Bars3Icon className="w-6 h-6 text-primary" />
            </button>
            <h1 className="text-xl font-black gradient-text">SKOPE ERP</h1>
            <div className="w-6"></div>
          </div>
        </div>

        {/* Page Content */}
        <div className="p-6 lg:p-10 fade-in">
          <Outlet />
        </div>
      </div>

      {/* AI Chatbot */}
      <Chatbot />
    </div>
  )
}
