/**
 * 🤖 Agent Orchestrator Page
 * Manage and monitor autonomous agents
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Bot, 
  Play, 
  Pause, 
  Trash2, 
  Plus,
  Activity,
  CheckCircle,
  XCircle,
  Clock
} from 'lucide-react';

const AgentOrchestrator = () => {
  const [agents, setAgents] = useState([
    {
      id: 1,
      name: 'Code Generator',
      type: 'specialized',
      status: 'active',
      tasksCompleted: 156,
      successRate: 98.5,
      lastActivity: '2 min ago'
    },
    {
      id: 2,
      name: 'Data Analyzer',
      type: 'specialized',
      status: 'idle',
      tasksCompleted: 89,
      successRate: 97.2,
      lastActivity: '5 min ago'
    },
    {
      id: 3,
      name: 'Bug Fixer',
      type: 'specialized',
      status: 'busy',
      tasksCompleted: 234,
      successRate: 96.8,
      lastActivity: 'Just now'
    },
    {
      id: 4,
      name: 'Research Assistant',
      type: 'autonomous',
      status: 'active',
      tasksCompleted: 78,
      successRate: 99.1,
      lastActivity: '1 min ago'
    }
  ]);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    type: 'specialized'
  });

  const getStatusColor = (status) => {
    const colors = {
      active: 'text-green-500 bg-green-500/20',
      idle: 'text-yellow-500 bg-yellow-500/20',
      busy: 'text-blue-500 bg-blue-500/20',
      error: 'text-red-500 bg-red-500/20'
    };
    return colors[status] || colors.idle;
  };

  const getStatusIcon = (status) => {
    const icons = {
      active: <Activity size={16} />,
      idle: <Clock size={16} />,
      busy: <Activity size={16} className="animate-pulse" />,
      error: <XCircle size={16} />
    };
    return icons[status] || icons.idle;
  };

  const handleCreateAgent = () => {
    if (!newAgent.name) return;

    const agent = {
      id: Date.now(),
      name: newAgent.name,
      type: newAgent.type,
      status: 'idle',
      tasksCompleted: 0,
      successRate: 100,
      lastActivity: 'Just created'
    };

    setAgents([...agents, agent]);
    setShowCreateModal(false);
    setNewAgent({ name: '', type: 'specialized' });
  };

  const handleToggleAgent = (id) => {
    setAgents(agents.map(agent => {
      if (agent.id === id) {
        return {
          ...agent,
          status: agent.status === 'active' ? 'idle' : 'active'
        };
      }
      return agent;
    }));
  };

  const handleDeleteAgent = (id) => {
    setAgents(agents.filter(agent => agent.id !== id));
  };

  const AgentCard = ({ agent }) => (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="bg-surface rounded-lg p-6 border border-gray-700 hover:border-primary transition-colors"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center">
            <Bot className="text-primary" size={24} />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">{agent.name}</h3>
            <p className="text-sm text-gray-400 capitalize">{agent.type}</p>
          </div>
        </div>
        
        <div className={`px-3 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getStatusColor(agent.status)}`}>
          {getStatusIcon(agent.status)}
          <span className="capitalize">{agent.status}</span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <p className="text-xs text-gray-400">Tasks</p>
          <p className="text-lg font-semibold text-white">{agent.tasksCompleted}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Success</p>
          <p className="text-lg font-semibold text-green-500">{agent.successRate}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Last Active</p>
          <p className="text-xs text-white">{agent.lastActivity}</p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center space-x-2">
        <button
          onClick={() => handleToggleAgent(agent.id)}
          className="flex-1 bg-primary hover:bg-primary/80 text-white px-4 py-2 rounded flex items-center justify-center space-x-2 transition-colors"
        >
          {agent.status === 'active' ? (
            <>
              <Pause size={16} />
              <span>Pause</span>
            </>
          ) : (
            <>
              <Play size={16} />
              <span>Start</span>
            </>
          )}
        </button>
        <button
          onClick={() => handleDeleteAgent(agent.id)}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
        >
          <Trash2 size={16} />
        </button>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">
            🤖 Agent Orchestrator
          </h1>
          <p className="text-gray-400">
            Manage your autonomous AI agents
          </p>
        </div>
        
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-primary hover:bg-primary/80 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors"
        >
          <Plus size={20} />
          <span>Create Agent</span>
        </button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Total Agents</p>
          <p className="text-3xl font-bold text-white">{agents.length}</p>
        </div>
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Active</p>
          <p className="text-3xl font-bold text-green-500">
            {agents.filter(a => a.status === 'active').length}
          </p>
        </div>
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Total Tasks</p>
          <p className="text-3xl font-bold text-blue-500">
            {agents.reduce((sum, a) => sum + a.tasksCompleted, 0)}
          </p>
        </div>
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Avg Success</p>
          <p className="text-3xl font-bold text-purple-500">
            {(agents.reduce((sum, a) => sum + a.successRate, 0) / agents.length).toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map(agent => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>

      {/* Create Agent Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-surface rounded-lg p-6 max-w-md w-full border border-gray-700"
          >
            <h2 className="text-2xl font-bold text-white mb-4">Create New Agent</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Agent Name</label>
                <input
                  type="text"
                  value={newAgent.name}
                  onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                  placeholder="e.g., Code Generator"
                  className="w-full bg-background text-white px-4 py-2 rounded border border-gray-700 focus:border-primary outline-none"
                />
              </div>
              
              <div>
                <label className="block text-sm text-gray-400 mb-2">Agent Type</label>
                <select
                  value={newAgent.type}
                  onChange={(e) => setNewAgent({ ...newAgent, type: e.target.value })}
                  className="w-full bg-background text-white px-4 py-2 rounded border border-gray-700 focus:border-primary outline-none"
                >
                  <option value="specialized">Specialized</option>
                  <option value="autonomous">Autonomous</option>
                  <option value="coordinator">Coordinator</option>
                </select>
              </div>
            </div>

            <div className="flex items-center space-x-3 mt-6">
              <button
                onClick={handleCreateAgent}
                className="flex-1 bg-primary hover:bg-primary/80 text-white px-4 py-2 rounded transition-colors"
              >
                Create
              </button>
              <button
                onClick={() => setShowCreateModal(false)}
                className="flex-1 bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded transition-colors"
              >
                Cancel
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default AgentOrchestrator;