import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Modal from '../components/Modal';
import CampaignForm from '../components/CampaignForm';
import StoreSelector from '../components/StoreSelector';
import { useAuthStore } from '../store/authStore';

interface Campaign {
  id: number;
  name: string;
  description: string;
  campaign_type: string;
  trigger_type: string;
  status: string;
  total_sent: number;
  total_opened: number;
  total_clicked: number;
  total_converted: number;
  created_at: string;
}

interface DashboardStats {
  total_campaigns: number;
  active_campaigns: number;
  total_messages_sent: number;
  total_conversions: number;
  average_conversion_rate: number;
}

const Marketing: React.FC = () => {
  const navigate = useNavigate();
  const { logout, user } = useAuthStore();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [filter, setFilter] = useState('all');
  const [selectedStoreId, setSelectedStoreId] = useState<number | 'all'>(user?.role === 'super_admin' ? 'all' : (user?.store_id || 'all'));

  const loadCampaigns = async () => {
    try {
      const token = localStorage.getItem('token');
      console.log('Token:', token ? 'EXISTS' : 'MISSING');
      console.log('Fetching campaigns from:', '/api/v1/campaigns/');
      
      const params: any = {};
      if (selectedStoreId !== 'all') {
        params.store_id = selectedStoreId;
      }
      
      const response = await axios.get('/api/v1/campaigns/', {
        headers: { Authorization: `Bearer ${token}` },
        params
      });
      
      console.log('Campaigns loaded:', response.data.length, 'campaigns');
      setCampaigns(response.data);
    } catch (error: any) {
      console.error('Error loading campaigns:', error);
      console.error('Error details:', error.response?.data);
      console.error('Status code:', error.response?.status);
      
      if (error.response?.status === 401) {
        console.log('401 Unauthorized - Logging out and redirecting to login');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        logout();
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadDashboardStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/v1/campaigns/dashboard/stats', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDashboardStats(response.data);
    } catch (error: any) {
      console.error('Error loading dashboard stats:', error);
      
      if (error.response?.status === 401) {
        console.log('401 on dashboard stats - Redirecting to login');
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        logout();
        navigate('/login');
      }
    }
  };

  useEffect(() => {
    loadCampaigns();
    loadDashboardStats();
  }, [selectedStoreId]);

  const handleActivate = async (id: number) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/v1/campaigns/${id}/activate`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadCampaigns();
    } catch (error: any) {
      console.error('Error activating campaign:', error);
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        logout();
        navigate('/login');
      }
    }
  };

  const handlePause = async (id: number) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/v1/campaigns/${id}/pause`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadCampaigns();
    } catch (error: any) {
      console.error('Error pausing campaign:', error);
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        logout();
        navigate('/login');
      }
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this campaign?')) return;
    
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/v1/campaigns/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadCampaigns();
      loadDashboardStats();
    } catch (error: any) {
      console.error('Error deleting campaign:', error);
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        logout();
        navigate('/login');
      }
    }
  };

  const getStatusBadge = (status: string) => {
    const badges = {
      draft: 'bg-gray-100 text-gray-700 border-gray-300',
      scheduled: 'bg-blue-100 text-blue-700 border-blue-300',
      active: 'bg-green-100 text-green-700 border-green-300',
      paused: 'bg-yellow-100 text-yellow-700 border-yellow-300',
      completed: 'bg-purple-100 text-purple-700 border-purple-300'
    };
    return badges[status as keyof typeof badges] || badges.draft;
  };

  const getTypeIcon = (type: string) => {
    const icons = {
      whatsapp: '📱',
      sms: '💬',
      email: '📧',
      notification: '🔔'
    };
    return icons[type as keyof typeof icons] || '📢';
  };

  const getTriggerIcon = (trigger: string) => {
    const icons = {
      manual: '✋',
      birthday: '🎂',
      festival: '🎉',
      warranty_expiry: '⚠️',
      cart_abandoned: '🛒',
      no_purchase_30_days: '⏰',
      purchase_anniversary: '🎊',
      geo_targeted: '📍'
    };
    return icons[trigger as keyof typeof icons] || '🚀';
  };

  const filteredCampaigns = filter === 'all' 
    ? campaigns 
    : campaigns.filter(c => c.status === filter);

  console.log('Marketing State:', { campaigns: campaigns.length, filter, filtered: filteredCampaigns.length });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Debug */}
      {campaigns.length === 0 && (
        <div className="bg-red-100 border-2 border-red-400 p-4 rounded-lg mb-4">
          <p><strong>⚠️ No campaigns loaded from API!</strong></p>
          <p>Check browser console for errors. You may need to logout and login again.</p>
        </div>
      )}
      
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            🚀 Marketing Automation
          </h1>
          <p className="text-gray-600 mt-2">
            Automated campaigns that work 24/7 to boost your sales
          </p>
        </div>
        <div className="flex items-center gap-4">
          <StoreSelector
            selectedStoreId={selectedStoreId}
            onStoreChange={setSelectedStoreId}
            showAllOption={true}
          />
          <button
            onClick={() => setShowModal(true)}
            className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 shadow-lg"
          >
            ✨ Create Campaign
          </button>
        </div>
      </div>

      {/* Dashboard Stats */}
      {dashboardStats && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
          <div className="bg-gradient-to-br from-purple-500 to-purple-700 rounded-2xl p-6 text-white shadow-xl hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm font-medium">Total Campaigns</p>
                <p className="text-3xl font-bold mt-2">{dashboardStats.total_campaigns}</p>
              </div>
              <div className="text-5xl opacity-20">📊</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-700 rounded-2xl p-6 text-white shadow-xl hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100 text-sm font-medium">Active Now</p>
                <p className="text-3xl font-bold mt-2">{dashboardStats.active_campaigns}</p>
              </div>
              <div className="text-5xl opacity-20">🟢</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl p-6 text-white shadow-xl hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm font-medium">Messages Sent</p>
                <p className="text-3xl font-bold mt-2">{dashboardStats.total_messages_sent.toLocaleString()}</p>
              </div>
              <div className="text-5xl opacity-20">📨</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-700 rounded-2xl p-6 text-white shadow-xl hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100 text-sm font-medium">Conversions</p>
                <p className="text-3xl font-bold mt-2">{dashboardStats.total_conversions}</p>
              </div>
              <div className="text-5xl opacity-20">💰</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-pink-500 to-pink-700 rounded-2xl p-6 text-white shadow-xl hover:scale-105 transition-all">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-pink-100 text-sm font-medium">Conversion Rate</p>
                <p className="text-3xl font-bold mt-2">{dashboardStats.average_conversion_rate.toFixed(1)}%</p>
              </div>
              <div className="text-5xl opacity-20">📈</div>
            </div>
          </div>
        </div>
      )}

      {/* Marketing Integrations */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border-2 border-purple-200 shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <span className="text-3xl">🔗</span>
              API Integrations
            </h2>
            <p className="text-gray-600 mt-1">Connect your Google Ads and Meta (Facebook/Instagram) accounts</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Google Ads Integration */}
          <div className="bg-white rounded-xl p-6 shadow-md border-2 border-gray-200 hover:border-blue-400 transition-all">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-3">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.5 2C7.8 2 4 5.8 4 10.5c0 4.6 7 11.7 7.7 12.4.4.4 1 .4 1.4 0 .7-.7 7.7-7.8 7.7-12.4C20.8 5.8 17 2 12.5 2zm0 14c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4-1.8 4-4 4z"/>
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-800">Google Ads</h3>
                  <p className="text-sm text-gray-600">Sync your ad campaigns</p>
                </div>
              </div>
              <span className="bg-yellow-100 text-yellow-700 text-xs font-bold px-3 py-1 rounded-full">
                Coming Soon
              </span>
            </div>
            <div className="mt-4 space-y-2">
              <p className="text-sm text-gray-600">
                • Auto-sync campaign performance<br/>
                • Track ROI and conversions<br/>
                • Manage budgets from dashboard
              </p>
            </div>
            <button 
              disabled
              className="mt-4 w-full bg-gray-200 text-gray-500 px-4 py-2 rounded-lg font-medium cursor-not-allowed"
            >
              🔒 OAuth Integration Pending
            </button>
          </div>

          {/* Meta Ads Integration */}
          <div className="bg-white rounded-xl p-6 shadow-md border-2 border-gray-200 hover:border-pink-400 transition-all">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="bg-gradient-to-br from-pink-500 to-purple-600 rounded-lg p-3">
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-800">Meta Ads</h3>
                  <p className="text-sm text-gray-600">Facebook & Instagram ads</p>
                </div>
              </div>
              <span className="bg-yellow-100 text-yellow-700 text-xs font-bold px-3 py-1 rounded-full">
                Coming Soon
              </span>
            </div>
            <div className="mt-4 space-y-2">
              <p className="text-sm text-gray-600">
                • Unified campaign management<br/>
                • Real-time performance metrics<br/>
                • Audience targeting insights
              </p>
            </div>
            <button 
              disabled
              className="mt-4 w-full bg-gray-200 text-gray-500 px-4 py-2 rounded-lg font-medium cursor-not-allowed"
            >
              🔒 Business Manager Setup Required
            </button>
          </div>
        </div>

        <div className="mt-6 bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>📋 Next Steps:</strong> To enable API integrations, you'll need:
          </p>
          <ul className="mt-2 text-sm text-blue-700 space-y-1 ml-4">
            <li>• Google Ads API credentials and OAuth 2.0 setup</li>
            <li>• Meta (Facebook) App ID and Business Manager access</li>
            <li>• API keys configured in backend settings</li>
          </ul>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {['all', 'active', 'scheduled', 'draft', 'paused', 'completed'].map(status => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              filter === status
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg scale-105'
                : 'bg-white text-gray-700 border-2 border-gray-200 hover:border-purple-300'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      {/* Campaigns Grid */}
      {filteredCampaigns.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center shadow-lg">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">No Campaigns Yet</h3>
          <p className="text-gray-600 mb-6">Start creating automated campaigns to boost your sales!</p>
          <button
            onClick={() => setShowModal(true)}
            className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105 shadow-lg"
          >
            Create Your First Campaign
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCampaigns.map((campaign) => (
            <div
              key={campaign.id}
              className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all border-2 border-gray-100 hover:border-purple-300"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{getTypeIcon(campaign.campaign_type)}</div>
                  <div>
                    <h3 className="font-bold text-lg text-gray-800">{campaign.name}</h3>
                    <p className="text-sm text-gray-500">{getTriggerIcon(campaign.trigger_type)} {campaign.trigger_type.replace(/_/g, ' ')}</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold border-2 ${getStatusBadge(campaign.status)}`}>
                  {campaign.status}
                </span>
              </div>

              {/* Description */}
              {campaign.description && (
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">{campaign.description}</p>
              )}

              {/* Stats */}
              <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-xs text-blue-600 font-medium">Sent</p>
                  <p className="text-xl font-bold text-blue-700">{campaign.total_sent}</p>
                </div>
                <div className="bg-green-50 rounded-lg p-3">
                  <p className="text-xs text-green-600 font-medium">Opened</p>
                  <p className="text-xl font-bold text-green-700">{campaign.total_opened}</p>
                </div>
                <div className="bg-purple-50 rounded-lg p-3">
                  <p className="text-xs text-purple-600 font-medium">Clicked</p>
                  <p className="text-xl font-bold text-purple-700">{campaign.total_clicked}</p>
                </div>
                <div className="bg-orange-50 rounded-lg p-3">
                  <p className="text-xs text-orange-600 font-medium">Converted</p>
                  <p className="text-xl font-bold text-orange-700">{campaign.total_converted}</p>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                {campaign.status === 'draft' || campaign.status === 'paused' ? (
                  <button
                    onClick={() => handleActivate(campaign.id)}
                    className="flex-1 bg-green-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-600 transition-all"
                  >
                    ▶️ Activate
                  </button>
                ) : campaign.status === 'active' ? (
                  <button
                    onClick={() => handlePause(campaign.id)}
                    className="flex-1 bg-yellow-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-yellow-600 transition-all"
                  >
                    ⏸️ Pause
                  </button>
                ) : null}
                <button
                  onClick={() => handleDelete(campaign.id)}
                  className="bg-red-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-red-600 transition-all"
                >
                  🗑️
                </button>
              </div>

              {/* Created Date */}
              <p className="text-xs text-gray-400 mt-3 text-center">
                Created: {new Date(campaign.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="✨ Create New Campaign">
        <CampaignForm
          onSuccess={() => {
            setShowModal(false);
            loadCampaigns();
            loadDashboardStats();
          }}
          onCancel={() => setShowModal(false)}
        />
      </Modal>
    </div>
  );
};

export default Marketing;

