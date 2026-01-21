import React, { useState } from 'react';
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

interface CampaignFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

const CampaignForm: React.FC<CampaignFormProps> = ({ onSuccess, onCancel }) => {
  const { user } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    campaign_type: 'whatsapp',
    trigger_type: 'manual',
    message_template: '',
    subject: '',
    store_id: user?.store_id || 1,
    geo_location: '',
    start_date: '',
    end_date: '',
    send_time: '',
    days_before_trigger: 0,
    discount_code: '',
    discount_percentage: 0,
    target_customers: {}
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const token = localStorage.getItem('token');
      
      // Prepare data with proper formatting
      const campaignData = {
        name: formData.name,
        description: formData.description || null,
        campaign_type: formData.campaign_type,
        trigger_type: formData.trigger_type,
        message_template: formData.message_template,
        subject: formData.subject || null,
        store_id: formData.store_id,
        target_customers: formData.target_customers || null,
        geo_location: formData.geo_location || null,
        start_date: formData.start_date || null,
        end_date: formData.end_date || null,
        send_time: formData.send_time || null,
        days_before_trigger: formData.days_before_trigger || null,
        discount_code: formData.discount_code || null,
        discount_percentage: formData.discount_percentage ? parseFloat(formData.discount_percentage.toString()) : null
      };
      
      console.log('Sending campaign data:', campaignData);
      
      const response = await axios.post('/api/v1/campaigns/', campaignData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      console.log('Campaign created:', response.data);
      alert('Campaign created successfully!');
      onSuccess();
    } catch (error: any) {
      console.error('Error creating campaign:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to create campaign';
      alert(`Error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const messageTemplates = {
    birthday: "🎉 Happy Birthday {customer_name}! 🎂\n\nWe're celebrating YOU today! Get {discount}% OFF on your next purchase.\nUse code: {code}\n\nValid for 7 days. Visit us now! 🎁",
    warranty: "⚠️ Important: Warranty Expiring Soon!\n\nDear {customer_name},\n\nYour product warranty expires in {days} days. Get it serviced or upgrade now!\n\nCall: {store_phone}\n\n🔧 We're here to help!",
    festival: "✨ {festival} Special Offer! ✨\n\nHello {customer_name}!\n\nCelebrate with {discount}% OFF on all products!\nUse code: {code}\n\nOffer valid till {end_date}\n\n🎊 Shop Now!",
    abandoned_cart: "🛒 You left something behind!\n\nHi {customer_name},\n\nComplete your purchase now and get {discount}% OFF!\n\nCode: {code}\nValid for 24 hours only!\n\n💳 Checkout now!",
    referral: "👥 Refer & Earn!\n\nDear {customer_name},\n\nRefer a friend and both get {discount}% OFF!\n\nYour referral code: {code}\n\n💰 Start earning rewards today!",
    no_purchase: "💜 We Miss You!\n\nHi {customer_name},\n\nIt's been a while! Come back and get {discount}% OFF your next purchase.\n\nCode: {code}\nValid for 7 days!\n\n🛍️ See you soon!"
  };

  const loadTemplate = (trigger: string) => {
    const template = messageTemplates[trigger as keyof typeof messageTemplates];
    if (template) {
      setFormData(prev => ({ ...prev, message_template: template }));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Campaign Name */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Campaign Name *
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
            placeholder="e.g., Diwali Sale 2024"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Campaign Type *
          </label>
          <select
            name="campaign_type"
            value={formData.campaign_type}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
          >
            <option value="whatsapp">📱 WhatsApp</option>
            <option value="sms">💬 SMS</option>
            <option value="email">📧 Email</option>
            <option value="notification">🔔 Notification</option>
          </select>
        </div>
      </div>

      {/* Trigger Type */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Trigger Type *
        </label>
        <select
          name="trigger_type"
          value={formData.trigger_type}
          onChange={(e) => {
            handleChange(e);
            loadTemplate(e.target.value);
          }}
          required
          className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
        >
          <option value="manual">✋ Manual</option>
          <option value="birthday">🎂 Birthday</option>
          <option value="festival">🎉 Festival</option>
          <option value="warranty_expiry">⚠️ Warranty Expiry</option>
          <option value="cart_abandoned">🛒 Cart Abandoned</option>
          <option value="no_purchase_30_days">⏰ No Purchase (30 days)</option>
          <option value="purchase_anniversary">🎊 Purchase Anniversary</option>
          <option value="geo_targeted">📍 Geo-Targeted</option>
        </select>
      </div>

      {/* Description */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Description
        </label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows={2}
          className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
          placeholder="Brief description of your campaign..."
        />
      </div>

      {/* Message Template */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Message Template *
        </label>
        <div className="text-xs text-gray-500 mb-2">
          Use variables: {'{customer_name}'}, {'{discount}'}, {'{code}'}, {'{days}'}, {'{festival}'}, {'{end_date}'}
        </div>
        <textarea
          name="message_template"
          value={formData.message_template}
          onChange={handleChange}
          required
          rows={6}
          className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all font-mono text-sm"
          placeholder="Type your message here..."
        />
      </div>

      {/* Discount Settings */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Discount Code
          </label>
          <input
            type="text"
            name="discount_code"
            value={formData.discount_code}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
            placeholder="e.g., DIWALI24"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Discount %
          </label>
          <input
            type="number"
            name="discount_percentage"
            value={formData.discount_percentage}
            onChange={handleChange}
            min="0"
            max="100"
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
            placeholder="10"
          />
        </div>
      </div>

      {/* Scheduling */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Start Date
          </label>
          <input
            type="datetime-local"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            End Date
          </label>
          <input
            type="datetime-local"
            name="end_date"
            value={formData.end_date}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
          />
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Send Time (HH:MM)
          </label>
          <input
            type="time"
            name="send_time"
            value={formData.send_time}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
          />
        </div>
      </div>

      {/* Days Before Trigger */}
      {(formData.trigger_type === 'warranty_expiry' || formData.trigger_type === 'birthday') && (
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Days Before Trigger
          </label>
          <input
            type="number"
            name="days_before_trigger"
            value={formData.days_before_trigger}
            onChange={handleChange}
            min="0"
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
            placeholder="7"
          />
          <p className="text-xs text-gray-500 mt-1">Send message X days before the event</p>
        </div>
      )}

      {/* Geo Location */}
      {formData.trigger_type === 'geo_targeted' && (
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Geo Location
          </label>
          <input
            type="text"
            name="geo_location"
            value={formData.geo_location}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
            placeholder="City, State, or Pincode"
          />
        </div>
      )}

      {/* Buttons */}
      <div className="flex gap-4 pt-4">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          {loading ? '🔄 Creating...' : '🚀 Create Campaign'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold text-gray-700 hover:bg-gray-50 transition-all"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default CampaignForm;

