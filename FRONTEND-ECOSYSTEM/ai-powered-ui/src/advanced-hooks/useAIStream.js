/**
 * 🌊 useAIStream Hook
 * Handle streaming AI responses
 */

import { useState, useCallback } from 'react';
import AIService from '../ai-services/AIService';

export const useAIStream = () => {
  const [content, setContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState(null);

  const startStream = useCallback(async (prompt, options = {}) => {
    setIsStreaming(true);
    setContent('');
    setError(null);

    try {
      const stream = AIService.streamGenerate(prompt, options);

      for await (const chunk of stream) {
        setContent(prev => prev + chunk);
      }
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsStreaming(false);
    }
  }, []);

  const reset = useCallback(() => {
    setContent('');
    setError(null);
  }, []);

  return {
    content,
    isStreaming,
    error,
    startStream,
    reset
  };
};

export default useAIStream;