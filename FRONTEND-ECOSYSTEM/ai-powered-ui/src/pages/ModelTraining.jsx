/**
 * 🧠 Model Training Interface
 * Monitor and manage AI model training
 */

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Play, Pause, Square, Settings, Upload, Download } from 'lucide-react';

const ModelTraining = () => {
  const [trainingJobs, setTrainingJobs] = useState([
    {
      id: 1,
      name: 'GPT Fine-tuning',
      status: 'running',
      progress: 65,
      epoch: 13,
      totalEpochs: 20,
      loss: 0.234,
      accuracy: 94.5,
      startedAt: '2 hours ago'
    },
    {
      id: 2,
      name: 'Code Generation Model',
      status: 'completed',
      progress: 100,
      epoch: 50,
      totalEpochs: 50,
      loss: 0.156,
      accuracy: 97.2,
      startedAt: '1 day ago'
    },
    {
      id: 3,
      name: 'Sentiment Analysis',
      status: 'pending',
      progress: 0,
      epoch: 0,
      totalEpochs: 30,
      loss: 0,
      accuracy: 0,
      startedAt: 'Not started'
    }
  ]);

  const getStatusColor = (status) => {
    const colors = {
      running: 'bg-blue-500',
      completed: 'bg-green-500',
      pending: 'bg-gray-500',
      failed: 'bg-red-500'
    };
    return colors[status] || colors.pending;
  };

  const TrainingJobCard = ({ job }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-surface rounded-lg p-6 border border-gray-700"
    >
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white mb-1">{job.name}</h3>
          <p className="text-sm text-gray-400">Started {job.startedAt}</p>
        </div>
        <div className={`w-3 h-3 rounded-full ${getStatusColor(job.status)}`} />
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Progress</span>
          <span className="text-sm text-white font-semibold">{job.progress}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div 
            className="bg-primary h-2 rounded-full transition-all duration-500"
            style={{ width: `${job.progress}%` }}
          />
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className="text-xs text-gray-400">Epoch</p>
          <p className="text-lg font-semibold text-white">
            {job.epoch} / {job.totalEpochs}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Loss</p>
          <p className="text-lg font-semibold text-white">{job.loss.toFixed(3)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Accuracy</p>
          <p className="text-lg font-semibold text-green-500">{job.accuracy}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Status</p>
          <p className="text-sm font-semibold text-white capitalize">{job.status}</p>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center space-x-2">
        {job.status === 'running' ? (
          <button className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded flex items-center justify-center space-x-2">
            <Pause size={16} />
            <span>Pause</span>
          </button>
        ) : job.status === 'pending' ? (
          <button className="flex-1 bg-primary hover:bg-primary/80 text-white px-4 py-2 rounded flex items-center justify-center space-x-2">
            <Play size={16} />
            <span>Start</span>
          </button>
        ) : (
          <button className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded flex items-center justify-center space-x-2">
            <Download size={16} />
            <span>Download</span>
          </button>
        )}
        <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded">
          <Settings size={16} />
        </button>
        {job.status === 'running' && (
          <button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">
            <Square size={16} />
          </button>
        )}
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">
            🧠 Model Training
          </h1>
          <p className="text-gray-400">
            Monitor and manage your AI model training jobs
          </p>
        </div>
        
        <button className="bg-primary hover:bg-primary/80 text-white px-6 py-3 rounded-lg flex items-center space-x-2">
          <Upload size={20} />
          <span>New Training Job</span>
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Total Jobs</p>
          <p className="text-3xl font-bold text-white">{trainingJobs.length}</p>
        </div>
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Running</p>
          <p className="text-3xl font-bold text-blue-500">
            {trainingJobs.filter(j => j.status === 'running').length}
          </p>
        </div>
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Completed</p>
          <p className="text-3xl font-bold text-green-500">
            {trainingJobs.filter(j => j.status === 'completed').length}
          </p>
        </div>
        <div className="bg-surface rounded-lg p-4 border border-gray-700">
          <p className="text-sm text-gray-400 mb-2">Pending</p>
          <p className="text-3xl font-bold text-gray-500">
            {trainingJobs.filter(j => j.status === 'pending').length}
          </p>
        </div>
      </div>

      {/* Training Jobs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {trainingJobs.map(job => (
          <TrainingJobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
};

export default ModelTraining;