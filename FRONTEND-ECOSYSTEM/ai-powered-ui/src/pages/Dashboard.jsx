/**
 * 📊 Main Dashboard Component
 * Overview of entire AI Agent System
 */

import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Zap, 
  TrendingUp, 
  Activity, 
  Server,
  Database,
  Cpu,
  Network
} from 'lucide-react';
import AIService from '../ai-services/AIService';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalRequests: 0,
    activeAgents: 0,
    successRate: 0,
    avgResponseTime: 0
  });

  // Fetch metrics
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => AIService.getMetrics(),
    refetchInterval: 5000 // Refresh every 5 seconds
  });

  // Fetch providers
  const { data: providers } = useQuery({
    queryKey: ['providers'],
    queryFn: () => AIService.listProviders()
  });

  useEffect(() => {
    if (metrics) {
      setStats({
        totalRequests: metrics.requests_count || 0,
        activeAgents: metrics.provider_usage ? Object.keys(metrics.provider_usage).length : 0,
        successRate: metrics.success_count && metrics.requests_count 
          ? ((metrics.success_count / metrics.requests_count) * 100).toFixed(1)
          : 0,
        avgResponseTime: metrics.average_latency ? metrics.average_latency.toFixed(2) : 0
      });
    }
  }, [metrics]);

  const StatCard = ({ icon: Icon, title, value, subtitle, color }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-surface rounded-lg p-6 shadow-lg hover:shadow-xl transition-shadow"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg bg-${color}-500 bg-opacity-20`}>
          <Icon className={`text-${color}-500`} size={24} />
        </div>
        <span className="text-sm text-gray-400">{subtitle}</span>
      </div>
      <h3 className="text-2xl font-bold text-white mb-1">{value}</h3>
      <p className="text-gray-400 text-sm">{title}</p>
    </motion.div>
  );

  const ProviderCard = ({ name, available, models }) => (
    <div className="bg-surface rounded-lg p-4 border border-gray-700">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-semibold text-white capitalize">{name}</h4>
        <span className={`w-3 h-3 rounded-full ${available ? 'bg-green-500' : 'bg-red-500'}`} />
      </div>
      <p className="text-sm text-gray-400">
        {models?.length || 0} models available
      </p>
      <div className="mt-2 text-xs text-gray-500">
        {available ? '🟢 Online' : '🔴 Offline'}
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          🌟 AI Agent System Dashboard
        </h1>
        <p className="text-gray-400">
          Monitor and control your autonomous AI agents
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={Activity}
          title="Total Requests"
          value={stats.totalRequests.toLocaleString()}
          subtitle="Last 24h"
          color="blue"
        />
        <StatCard
          icon={Server}
          title="Active Providers"
          value={stats.activeAgents}
          subtitle="AI Models"
          color="green"
        />
        <StatCard
          icon={TrendingUp}
          title="Success Rate"
          value={`${stats.successRate}%`}
          subtitle="Performance"
          color="purple"
        />
        <StatCard
          icon={Zap}
          title="Avg Response"
          value={`${stats.avgResponseTime}s`}
          subtitle="Latency"
          color="yellow"
        />
      </div>

      {/* Providers Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-4">AI Providers</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {providers?.providers && Object.entries(providers.providers).map(([name, data]) => (
            <ProviderCard
              key={name}
              name={name}
              available={data.available}
              models={data.models}
            />
          ))}
        </div>
      </div>

      {/* System Health */}
      <div className="bg-surface rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-4">System Health</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center space-x-3">
            <Cpu className="text-blue-500" size={20} />
            <div>
              <p className="text-sm text-gray-400">CPU Usage</p>
              <p className="text-white font-semibold">45%</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Database className="text-green-500" size={20} />
            <div>
              <p className="text-sm text-gray-400">Memory</p>
              <p className="text-white font-semibold">2.4 GB</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Network className="text-purple-500" size={20} />
            <div>
              <p className="text-sm text-gray-400">Network</p>
              <p className="text-white font-semibold">Active</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="mt-8 bg-surface rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-4">Recent Activity</h2>
        <div className="space-y-3">
          {metrics?.provider_usage && Object.entries(metrics.provider_usage).map(([provider, count]) => (
            <div key={provider} className="flex items-center justify-between border-b border-gray-700 pb-2">
              <div className="flex items-center space-x-3">
                <Brain className="text-primary" size={20} />
                <span className="text-white capitalize">{provider}</span>
              </div>
              <span className="text-gray-400">{count} requests</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;