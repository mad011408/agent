/**
 * 🚀 API Gateway Service
 * Central entry point for all microservices with intelligent routing
 */

import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import morgan from 'morgan';
import dotenv from 'dotenv';
import { createProxyMiddleware } from 'http-proxy-middleware';
import rateLimit from 'express-rate-limit';

import { authMiddleware } from './middleware/AuthMiddleware.js';
import { loggingMiddleware } from './middleware/LoggingMiddleware.js';
import { CircuitBreaker } from './gateway/CircuitBreaker.js';
import { LoadBalancer } from './gateway/LoadBalancer.js';

dotenv.config();

const app = express();
const PORT = process.env.API_PORT || 8000;

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compression
app.use(compression());

// Logging
app.use(morgan('combined'));
app.use(loggingMiddleware);

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000'),
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100'),
  message: 'Too many requests from this IP, please try again later'
});
app.use('/api/', limiter);

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-gateway',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Root
app.get('/', (req, res) => {
  res.json({
    message: '🌟 Welcome to Ultra Advanced AI Agent System API Gateway',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      ai: '/api/ai/*',
      agents: '/api/agents/*',
      vectors: '/api/vectors/*',
      analytics: '/api/analytics/*'
    }
  });
});

// Initialize load balancers and circuit breakers
const aiEngineBalancer = new LoadBalancer([
  `http://localhost:${process.env.PYTHON_API_PORT || 8001}`
]);

const aiEngineCircuit = new CircuitBreaker({
  failureThreshold: 5,
  resetTimeout: 30000
});

// AI Engine proxy routes
app.use('/api/ai', async (req, res, next) => {
  try {
    // Check circuit breaker
    if (aiEngineCircuit.isOpen()) {
      return res.status(503).json({
        error: 'AI service temporarily unavailable',
        retryAfter: aiEngineCircuit.getResetTime()
      });
    }

    next();
  } catch (error) {
    next(error);
  }
}, createProxyMiddleware({
  target: aiEngineBalancer.getNextServer(),
  changeOrigin: true,
  pathRewrite: {
    '^/api/ai': '/v1'
  },
  onProxyReq: (proxyReq, req, res) => {
    aiEngineCircuit.recordRequest();
  },
  onProxyRes: (proxyRes, req, res) => {
    if (proxyRes.statusCode >= 500) {
      aiEngineCircuit.recordFailure();
    } else {
      aiEngineCircuit.recordSuccess();
    }
  },
  onError: (err, req, res) => {
    aiEngineCircuit.recordFailure();
    res.status(502).json({
      error: 'AI service error',
      message: err.message
    });
  }
}));

// Agent service routes (placeholder)
app.use('/api/agents', (req, res) => {
  res.json({
    message: 'Agent service endpoint',
    status: 'coming soon'
  });
});

// Vector service routes (placeholder)
app.use('/api/vectors', (req, res) => {
  res.json({
    message: 'Vector service endpoint',
    status: 'coming soon'
  });
});

// Analytics service routes (placeholder)
app.use('/api/analytics', (req, res) => {
  res.json({
    message: 'Analytics service endpoint',
    status: 'coming soon'
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Gateway Error:', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    path: req.path
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 API Gateway running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`🧠 AI Engine proxy: http://localhost:${PORT}/api/ai`);
});

export default app;