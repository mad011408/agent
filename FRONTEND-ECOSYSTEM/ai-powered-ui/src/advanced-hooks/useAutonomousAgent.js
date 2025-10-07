/**
 * 🤖 useAutonomousAgent Hook
 * Manage autonomous agent interactions
 */

import { useState, useCallback } from 'react';
import AIService from '../ai-services/AIService';

export const useAutonomousAgent = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const executeTask = useCallback(async (task, options = {}) => {
    setIsRunning(true);
    setError(null);
    
    try {
      const response = await AIService.smartRoute(task, options.taskType || 'general', {
        systemPrompt: options.systemPrompt
      });
      
      setResult(response);
      return response;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsRunning(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return {
    isRunning,
    result,
    error,
    executeTask,
    reset
  };
};

export default useAutonomousAgent;