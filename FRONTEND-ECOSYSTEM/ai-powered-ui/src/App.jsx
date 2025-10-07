/**
 * 🌟 Main Application Component
 * Ultra Advanced AI Agent System Frontend
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Provider } from 'react-redux';
import { store } from './state-management/store';

// Components
import Dashboard from './pages/Dashboard';
import ChatInterface from './pages/ChatInterface';
import AgentOrchestrator from './pages/AgentOrchestrator';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import ModelTraining from './pages/ModelTraining';

// Layout
import Layout from './components/Layout';

// Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/chat" element={<ChatInterface />} />
              <Route path="/agents" element={<AgentOrchestrator />} />
              <Route path="/analytics" element={<AnalyticsDashboard />} />
              <Route path="/training" element={<ModelTraining />} />
            </Routes>
          </Layout>
        </Router>
      </QueryClientProvider>
    </Provider>
  );
}

export default App;