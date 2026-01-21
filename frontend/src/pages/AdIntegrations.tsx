import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../utils/api'
import toast from 'react-hot-toast'
import {
  LinkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
  ChartBarIcon,
  UsersIcon,
  PhotoIcon,
  MegaphoneIcon
} from '@heroicons/react/24/outline'

interface AdConnection {
  id: number
  platform: string
  meta_ad_account_id?: string
  google_customer_id?: string
  is_active: boolean
  token_expires_at: string
  created_at: string
}

interface AdCampaign {
  id: number
  campaign_name: string
  platform: string
  status: string
  budget_daily: number
  created_at: string
}

interface Audience {
  id: number
  name: string
  platform: string
  size: number
  last_synced_at: string
}

export default function AdIntegrations() {
  const navigate = useNavigate()
  const [connections, setConnections] = useState<AdConnection[]>([])
  const [campaigns, setCampaigns] = useState<AdCampaign[]>([])
  const [audiences, setAudiences] = useState<Audience[]>([])
  const [loading, setLoading] = useState(true)
  const [overview, setOverview] = useState<any>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setLoading(true)
    try {
      const [connRes, campRes, audRes, overviewRes] = await Promise.all([
        api.get('/ads/connections'),
        api.get('/ads/campaigns'),
        api.get('/ads/audiences'),
        api.get('/ads/analytics/overview')
      ])
      setConnections(connRes.data)
      setCampaigns(campRes.data)
      setAudiences(audRes.data)
      setOverview(overviewRes.data)
    } catch (error) {
      console.error('Failed to load ad data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleConnectMeta = async () => {
    try {
      await api.get('/ads/meta/auth-url')
      toast.success('Opening Meta Business Manager...')
      // In demo mode, show success
      toast.success('Demo: Meta account connected!')
    } catch (error) {
      toast.error('Failed to get auth URL')
    }
  }

  const handleConnectGoogle = async () => {
    try {
      await api.get('/ads/google/auth-url')
      toast.success('Opening Google Ads authorization...')
      // In demo mode, show success
      toast.success('Demo: Google Ads account connected!')
    } catch (error) {
      toast.error('Failed to get auth URL')
    }
  }

  const getMetaConnection = () => connections.find(c => c.platform === 'meta')
  const getGoogleConnection = () => connections.find(c => c.platform === 'google')

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
    return num.toString()
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl shadow-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <MegaphoneIcon className="w-10 h-10" />
              <h1 className="text-4xl font-black">Ad Integrations</h1>
            </div>
            <p className="text-xl text-white/90">
              Connect your Google Ads and Meta Business accounts for automated marketing
            </p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-black">{connections.length}</div>
            <div className="text-sm text-white/80 font-semibold">Connected Accounts</div>
          </div>
        </div>
      </div>

      {/* Overview Stats */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="bg-white rounded-xl shadow-lg p-6 border border-neutral-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-blue-100 rounded-lg">
                <MegaphoneIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <div className="text-sm text-neutral-500">Active Campaigns</div>
                <div className="text-2xl font-bold">{overview.active_campaigns}</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 border border-neutral-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-green-100 rounded-lg">
                <ChartBarIcon className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <div className="text-sm text-neutral-500">Total Spend</div>
                <div className="text-2xl font-bold">₹{formatNumber(overview.total_spend)}</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 border border-neutral-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-purple-100 rounded-lg">
                <UsersIcon className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <div className="text-sm text-neutral-500">Total Clicks</div>
                <div className="text-2xl font-bold">{formatNumber(overview.total_clicks)}</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 border border-neutral-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-orange-100 rounded-lg">
                <UsersIcon className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <div className="text-sm text-neutral-500">Total Leads</div>
                <div className="text-2xl font-bold">{formatNumber(overview.total_leads)}</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 border border-neutral-200">
            <div className="flex items-center gap-3">
              <div className="p-3 bg-pink-100 rounded-lg">
                <ChartBarIcon className="w-6 h-6 text-pink-600" />
              </div>
              <div>
                <div className="text-sm text-neutral-500">ROAS</div>
                <div className="text-2xl font-bold">{overview.roas}x</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Platform Connections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Meta (Facebook/Instagram) */}
        <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-blue-700 p-6 text-white">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-white rounded-xl flex items-center justify-center">
                <svg className="w-10 h-10" viewBox="0 0 24 24" fill="#1877F2">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold">Meta Business</h2>
                <p className="text-white/80">Facebook, Instagram & WhatsApp Ads</p>
              </div>
            </div>
          </div>
          <div className="p-6">
            {getMetaConnection() ? (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircleIcon className="w-6 h-6" />
                  <span className="font-semibold">Connected</span>
                </div>
                <div className="bg-neutral-50 rounded-lg p-4 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-neutral-500">Ad Account ID</span>
                    <span className="font-mono">{getMetaConnection()?.meta_ad_account_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-500">Status</span>
                    <span className="text-green-600 font-semibold">Active</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => navigate('/marketing')}
                    className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
                  >
                    View Campaigns
                  </button>
                  <button
                    onClick={loadData}
                    className="p-2 border border-neutral-300 rounded-lg hover:bg-neutral-50 transition"
                  >
                    <ArrowPathIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-neutral-500">
                  <ExclamationTriangleIcon className="w-6 h-6" />
                  <span>Not Connected</span>
                </div>
                <p className="text-sm text-neutral-600">
                  Connect your Meta Business account to create and manage Facebook, Instagram, and WhatsApp ads directly from SKOPE ERP.
                </p>
                <button
                  onClick={handleConnectMeta}
                  className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-blue-700 transition flex items-center justify-center gap-2"
                >
                  <LinkIcon className="w-5 h-5" />
                  Connect Meta Business
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Google Ads */}
        <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 overflow-hidden">
          <div className="bg-gradient-to-r from-green-500 to-green-700 p-6 text-white">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-white rounded-xl flex items-center justify-center">
                <svg className="w-10 h-10" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold">Google Ads</h2>
                <p className="text-white/80">Search, Display & YouTube Ads</p>
              </div>
            </div>
          </div>
          <div className="p-6">
            {getGoogleConnection() ? (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircleIcon className="w-6 h-6" />
                  <span className="font-semibold">Connected</span>
                </div>
                <div className="bg-neutral-50 rounded-lg p-4 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-neutral-500">Customer ID</span>
                    <span className="font-mono">{getGoogleConnection()?.google_customer_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-500">Status</span>
                    <span className="text-green-600 font-semibold">Active</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => navigate('/marketing')}
                    className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-green-700 transition"
                  >
                    View Campaigns
                  </button>
                  <button
                    onClick={loadData}
                    className="p-2 border border-neutral-300 rounded-lg hover:bg-neutral-50 transition"
                  >
                    <ArrowPathIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-neutral-500">
                  <ExclamationTriangleIcon className="w-6 h-6" />
                  <span>Not Connected</span>
                </div>
                <p className="text-sm text-neutral-600">
                  Connect your Google Ads account to run search, display, and YouTube campaigns targeting local customers.
                </p>
                <button
                  onClick={handleConnectGoogle}
                  className="w-full bg-green-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-green-700 transition flex items-center justify-center gap-2"
                >
                  <LinkIcon className="w-5 h-5" />
                  Connect Google Ads
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Active Campaigns */}
      <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold">Active Campaigns</h2>
          <button
            onClick={() => navigate('/marketing')}
            className="text-primary font-semibold hover:underline"
          >
            View All →
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-neutral-50">
              <tr>
                <th className="text-left py-3 px-4 font-semibold text-neutral-600">Campaign</th>
                <th className="text-left py-3 px-4 font-semibold text-neutral-600">Platform</th>
                <th className="text-left py-3 px-4 font-semibold text-neutral-600">Status</th>
                <th className="text-left py-3 px-4 font-semibold text-neutral-600">Daily Budget</th>
              </tr>
            </thead>
            <tbody>
              {campaigns.slice(0, 5).map((campaign) => (
                <tr key={campaign.id} className="border-t border-neutral-100 hover:bg-neutral-50">
                  <td className="py-3 px-4 font-medium">{campaign.campaign_name}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${campaign.platform === 'meta' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'
                      }`}>
                      {campaign.platform === 'meta' ? 'Meta' : 'Google'}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${campaign.status === 'active' ? 'bg-green-100 text-green-700' :
                      campaign.status === 'paused' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-neutral-100 text-neutral-700'
                      }`}>
                      {campaign.status}
                    </span>
                  </td>
                  <td className="py-3 px-4">₹{campaign.budget_daily?.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Custom Audiences */}
      <div className="bg-white rounded-2xl shadow-lg border border-neutral-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold">Custom Audiences</h2>
          <button className="bg-primary text-white px-4 py-2 rounded-lg font-semibold hover:bg-primary-dark transition">
            + Create Audience
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {audiences.map((audience) => (
            <div
              key={audience.id}
              className="bg-gradient-to-br from-neutral-50 to-neutral-100 rounded-xl p-4 border border-neutral-200"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <UsersIcon className="w-5 h-5 text-purple-600" />
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${audience.platform === 'meta' ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'
                  }`}>
                  {audience.platform}
                </span>
              </div>
              <h3 className="font-bold text-neutral-800">{audience.name}</h3>
              <div className="mt-2 flex items-center justify-between text-sm text-neutral-500">
                <span>{audience.size.toLocaleString()} customers</span>
                <span>Synced</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <button
          onClick={() => navigate('/marketing')}
          className="bg-white rounded-xl shadow-lg border border-neutral-200 p-6 hover:shadow-xl transition text-left"
        >
          <MegaphoneIcon className="w-8 h-8 text-primary mb-3" />
          <h3 className="font-bold text-lg">Create Campaign</h3>
          <p className="text-sm text-neutral-500">Launch a new ad campaign</p>
        </button>
        <button className="bg-white rounded-xl shadow-lg border border-neutral-200 p-6 hover:shadow-xl transition text-left">
          <PhotoIcon className="w-8 h-8 text-primary mb-3" />
          <h3 className="font-bold text-lg">Upload Creative</h3>
          <p className="text-sm text-neutral-500">Add images and videos</p>
        </button>
        <button className="bg-white rounded-xl shadow-lg border border-neutral-200 p-6 hover:shadow-xl transition text-left">
          <UsersIcon className="w-8 h-8 text-primary mb-3" />
          <h3 className="font-bold text-lg">Build Audience</h3>
          <p className="text-sm text-neutral-500">Create custom audiences</p>
        </button>
        <button className="bg-white rounded-xl shadow-lg border border-neutral-200 p-6 hover:shadow-xl transition text-left">
          <ChartBarIcon className="w-8 h-8 text-primary mb-3" />
          <h3 className="font-bold text-lg">View Analytics</h3>
          <p className="text-sm text-neutral-500">Performance insights</p>
        </button>
      </div>
    </div>
  )
}
