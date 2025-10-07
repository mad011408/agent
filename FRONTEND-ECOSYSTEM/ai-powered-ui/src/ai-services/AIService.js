/**
 * 🧠 AI Service
 * Communication with AI backend services
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class AIService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 300000, // 5 minutes for AI operations
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth interceptor
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('AI Service Error:', error);
        return Promise.reject(error);
      }
    );
  }

  /**
   * Generate AI response
   */
  async generate(prompt, options = {}) {
    const response = await this.client.post('/ai/generate', {
      prompt,
      provider: options.provider,
      model: options.model,
      system_prompt: options.systemPrompt,
      temperature: options.temperature || 0.7,
      max_tokens: options.maxTokens || 4096,
      stream: false,
    });

    return response.data;
  }

  /**
   * Stream AI response
   */
  async *streamGenerate(prompt, options = {}) {
    const response = await fetch(`${API_BASE_URL}/ai/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        prompt,
        provider: options.provider,
        model: options.model,
        system_prompt: options.systemPrompt,
        temperature: options.temperature || 0.7,
        max_tokens: options.maxTokens || 4096,
        stream: true,
      }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      yield chunk;
    }
  }

  /**
   * Chat completion
   */
  async chat(messages, options = {}) {
    const response = await this.client.post('/ai/chat/completions', {
      messages,
      provider: options.provider,
      model: options.model,
      temperature: options.temperature || 0.7,
      max_tokens: options.maxTokens || 4096,
      stream: false,
    });

    return response.data;
  }

  /**
   * Smart routing
   */
  async smartRoute(prompt, taskType = 'general', options = {}) {
    const response = await this.client.post('/ai/smart-route', {
      prompt,
      task_type: taskType,
      system_prompt: options.systemPrompt,
    });

    return response.data;
  }

  /**
   * Multi-provider generation
   */
  async multiProvider(prompt, providers = null, options = {}) {
    const response = await this.client.post('/ai/multi-provider', {
      prompt,
      providers,
      system_prompt: options.systemPrompt,
    });

    return response.data;
  }

  /**
   * List available providers
   */
  async listProviders() {
    const response = await this.client.get('/ai/providers');
    return response.data;
  }

  /**
   * Get metrics
   */
  async getMetrics() {
    const response = await this.client.get('/ai/metrics');
    return response.data;
  }
}

export default new AIService();