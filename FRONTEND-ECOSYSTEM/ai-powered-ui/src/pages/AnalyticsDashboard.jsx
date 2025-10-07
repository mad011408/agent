/**
 * 📊 Analytics Dashboard
 * Real-time analytics and insights
 */

import React, { useState, useEffect } from 'react';
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend,
  ResponsiveContainer 
} from 'recharts';
import { TrendingUp, TrendingDown, Activity, DollarSign } from 'lucide-react';

const AnalyticsDashboard = () => {
  const [timeRange, setTimeRange] = useState('7d');

  // Sample data
  const requestsData = [
    { date: 'Mon', requests: 245, successful: 240, failed: 5 },
    { date: 'Tue', requests: 312, successful: 305, failed: 7 },
    { date: 'Wed', requests: 289, successful: 285, failed: 4 },
    { date: 'Thu', requests: 356, successful: 348, failed: 8 },
    { date: 'Fri', requests: 423, successful: 415, failed: 8 },
    { date: 'Sat', requests: 198, successful: 195, failed: 3 },
    { date: 'Sun', requests: 234, successful: 230, failed: 4 }
  ];

  const providerData = [
    { name: 'NVIDIA', value: 650, color: '#76D7C4' },
    { name: 'SambaNova', value: 425, color: '#AF7AC5' },
    { name: 'Cerebras', value: 423, color: '#5DADE2' }
  ];

  const responseTimeData = [
    { hour: '00:00', avgTime: 1.2 },
    { hour: '04:00', avgTime: 0.9 },
    { hour: '08:00', avgTime: 1.5 },
    { hour: '12:00', avgTime: 2.1 },
    { hour: '16:00', avgTime: 1.8 },
    { hour: '20:00', avgTime: 1.4 }
  ];

  const MetricCard = ({ title, value, change, icon: Icon, trend }) => (
    <div className="bg-surface rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <span className="text-gray-400 text-sm">{title}</span>
        <Icon className="text-primary" size={20} />
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-3xl font-bold text-white mb-1">{value}</p>
          <div className={`flex items-center space-x-1 text-sm ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
            {trend === 'up' ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
            <span>{change}</span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">
            📊 Analytics Dashboard
          </h1>
          <p className="text-gray-400">
            Real-time insights and performance metrics
          </p>
        </div>
        
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value)}
          className="bg-surface text-white px-4 py-2 rounded border border-gray-700 focus:border-primary outline-none"
        >
          <option value="24h">Last 24 Hours</option>
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
        </select>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Total Requests"
          value="2,057"
          change="+12.5%"
          icon={Activity}
          trend="up"
        />
        <MetricCard
          title="Success Rate"
          value="98.7%"
          change="+2.3%"
          icon={TrendingUp}
          trend="up"
        />
        <MetricCard
          title="Avg Response Time"
          value="1.4s"
          change="-8.2%"
          icon={Activity}
          trend="up"
        />
        <MetricCard
          title="API Cost"
          value="$156"
          change="+5.4%"
          icon={DollarSign}
          trend="down"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Requests Over Time */}
        <div className="bg-surface rounded-lg p-6 border border-gray-700">
          <h2 className="text-xl font-bold text-white mb-4">Requests Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={requestsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #374151',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Bar dataKey="successful" fill="#10B981" name="Successful" />
              <Bar dataKey="failed" fill="#EF4444" name="Failed" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Provider Distribution */}
        <div className="bg-surface rounded-lg p-6 border border-gray-700">
          <h2 className="text-xl font-bold text-white mb-4">Provider Usage</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={providerData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {providerData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #374151',
                  borderRadius: '8px'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {providerData.map((provider, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: provider.color }}
                  />
                  <span className="text-sm text-gray-400">{provider.name}</span>
                </div>
                <span className="text-sm text-white font-semibold">{provider.value} req</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Response Time Chart */}
      <div className="bg-surface rounded-lg p-6 border border-gray-700">
        <h2 className="text-xl font-bold text-white mb-4">Average Response Time</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={responseTimeData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="hour" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#1e293b', 
                border: '1px solid #374151',
                borderRadius: '8px'
              }}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="avgTime" 
              stroke="#6366f1" 
              strokeWidth={2}
              name="Response Time (s)"
              dot={{ fill: '#6366f1', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;