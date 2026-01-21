import { useState, useEffect } from 'react'
import { SparklesIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon, LightBulbIcon, ChartBarIcon } from '@heroicons/react/24/outline'

interface Insight {
  id: string
  title: string
  description: string
  type: 'opportunity' | 'warning' | 'recommendation'
  impact: 'high' | 'medium' | 'low'
  metric?: string
  change?: number
}

export default function AIInsights() {
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate AI-generated insights
    const sampleInsights: Insight[] = [
      {
        id: '1',
        title: 'Peak Sales Hours Identified',
        description: 'Your store experiences highest sales between 2 PM - 5 PM. Consider scheduling more staff during these hours.',
        type: 'opportunity',
        impact: 'high',
        metric: 'Sales Volume',
        change: 34
      },
      {
        id: '2',
        title: 'Inventory Turnover Rate Improving',
        description: 'Electronics category inventory turnover has increased by 15% this month. Stock levels are optimal.',
        type: 'opportunity',
        impact: 'medium',
        metric: 'Inventory Turnover',
        change: 15
      },
      {
        id: '3',
        title: 'Low Stock Alert - Popular Items',
        description: '3 bestselling products are running low. Restock "Wireless Earbuds", "Smart Watch", and "Phone Cases" to avoid lost sales.',
        type: 'warning',
        impact: 'high',
        metric: 'Stock Levels',
        change: -35
      },
      {
        id: '4',
        title: 'Customer Retention Opportunity',
        description: '25 customers haven\'t purchased in 30 days. Launch a re-engagement campaign with personalized offers.',
        type: 'recommendation',
        impact: 'medium',
        metric: 'Customer Retention',
        change: -12
      },
      {
        id: '5',
        title: 'Product Bundle Recommendation',
        description: 'Customers buying "Laptop" often purchase "Mouse" and "Laptop Bag". Create a bundle offer to increase average order value.',
        type: 'opportunity',
        impact: 'high',
        metric: 'Average Order Value',
        change: 28
      },
      {
        id: '6',
        title: 'Seasonal Demand Forecast',
        description: 'Based on historical data, Fashion category sales typically increase by 40% next month. Plan inventory accordingly.',
        type: 'recommendation',
        impact: 'high',
        metric: 'Seasonal Forecast',
        change: 40
      }
    ]

    setTimeout(() => {
      setInsights(sampleInsights)
      setLoading(false)
    }, 800)
  }, [])

  const getInsightColor = (type: string) => {
    switch (type) {
      case 'opportunity':
        return 'from-green-500 to-emerald-600'
      case 'warning':
        return 'from-red-500 to-orange-600'
      case 'recommendation':
        return 'from-blue-500 to-indigo-600'
      default:
        return 'from-gray-500 to-gray-600'
    }
  }

  const getImpactBadge = (impact: string) => {
    switch (impact) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 rounded-2xl shadow-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <SparklesIcon className="w-10 h-10" />
              <h1 className="text-4xl font-black">AI Insights</h1>
            </div>
            <p className="text-xl text-white/90">
              Intelligent business recommendations powered by data analysis
            </p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-black">{insights.length}</div>
            <div className="text-sm text-white/80 font-semibold">Active Insights</div>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl p-6 text-white shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <ArrowTrendingUpIcon className="w-8 h-8" />
            <span className="text-3xl font-black">
              {insights.filter(i => i.type === 'opportunity').length}
            </span>
          </div>
          <div className="font-bold text-lg">Opportunities</div>
          <div className="text-sm text-white/80 mt-1">Growth potential identified</div>
        </div>

        <div className="bg-gradient-to-br from-red-500 to-orange-600 rounded-xl p-6 text-white shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <ArrowTrendingDownIcon className="w-8 h-8" />
            <span className="text-3xl font-black">
              {insights.filter(i => i.type === 'warning').length}
            </span>
          </div>
          <div className="font-bold text-lg">Warnings</div>
          <div className="text-sm text-white/80 mt-1">Issues requiring attention</div>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl p-6 text-white shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <LightBulbIcon className="w-8 h-8" />
            <span className="text-3xl font-black">
              {insights.filter(i => i.type === 'recommendation').length}
            </span>
          </div>
          <div className="font-bold text-lg">Recommendations</div>
          <div className="text-sm text-white/80 mt-1">Actionable suggestions</div>
        </div>
      </div>

      {/* Insights List */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl border border-neutral-200 overflow-hidden">
        <div className="p-6 border-b border-neutral-200 bg-gradient-to-r from-neutral-50 to-white">
          <h2 className="text-2xl font-bold text-neutral-800 flex items-center gap-3">
            <ChartBarIcon className="w-7 h-7 text-primary" />
            Generated Insights
          </h2>
          <p className="text-neutral-600 mt-1">AI-powered analysis of your business data</p>
        </div>

        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              <span className="ml-4 text-neutral-600 font-semibold">Analyzing data...</span>
            </div>
          ) : insights.length === 0 ? (
            <div className="text-center py-12">
              <SparklesIcon className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
              <p className="text-neutral-500 font-semibold">No insights available yet</p>
              <p className="text-neutral-400 text-sm mt-2">
                AI will analyze your data and generate insights automatically
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {insights.map((insight) => (
                <div
                  key={insight.id}
                  className="group bg-gradient-to-r from-white to-neutral-50 rounded-xl p-6 border border-neutral-200 hover:shadow-xl hover:scale-102 transition-all duration-300"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${getInsightColor(insight.type)}`}></div>
                        <h3 className="text-lg font-bold text-neutral-800 group-hover:text-primary transition-colors">
                          {insight.title}
                        </h3>
                        <span className={`text-xs px-3 py-1 rounded-full font-bold border ${getImpactBadge(insight.impact)}`}>
                          {insight.impact.toUpperCase()} IMPACT
                        </span>
                      </div>
                      <p className="text-neutral-600 leading-relaxed">
                        {insight.description}
                      </p>
                      {insight.metric && (
                        <div className="flex items-center gap-4 mt-4">
                          <div className="text-sm font-semibold text-neutral-500">
                            📊 {insight.metric}
                          </div>
                          {insight.change && (
                            <div className={`flex items-center gap-1 text-sm font-bold ${insight.change > 0 ? 'text-green-600' : 'text-red-600'
                              }`}>
                              {insight.change > 0 ? (
                                <ArrowTrendingUpIcon className="w-4 h-4" />
                              ) : (
                                <ArrowTrendingDownIcon className="w-4 h-4" />
                              )}
                              {Math.abs(insight.change)}%
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Info Banner */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-200">
        <div className="flex items-start gap-4">
          <SparklesIcon className="w-6 h-6 text-indigo-600 flex-shrink-0 mt-1" />
          <div>
            <h3 className="font-bold text-indigo-900 mb-2">How AI Insights Work</h3>
            <p className="text-indigo-700 text-sm leading-relaxed">
              Our AI engine continuously analyzes your sales patterns, inventory levels, customer behavior, and market trends
              to generate actionable insights. These recommendations help you make data-driven decisions to grow your business.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
