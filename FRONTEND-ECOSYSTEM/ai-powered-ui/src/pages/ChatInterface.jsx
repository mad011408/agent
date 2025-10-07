/**
 * 💬 Advanced Chat Interface
 * Multi-provider AI chat with streaming support
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Loader, Bot, User, Sparkles, Copy, Check } from 'lucide-react';
import AIService from '../ai-services/AIService';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: '👋 Hello! I\'m your AI assistant powered by multiple providers. How can I help you today?',
      provider: 'system',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('nvidia');
  const [streamingContent, setStreamingContent] = useState('');
  const messagesEndRef = useRef(null);
  const [copiedId, setCopiedId] = useState(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setStreamingContent('');

    try {
      // Use streaming for better UX
      const stream = AIService.streamGenerate(input, {
        provider: selectedProvider,
        temperature: 0.7
      });

      let fullContent = '';
      
      for await (const chunk of stream) {
        fullContent += chunk;
        setStreamingContent(fullContent);
      }

      // Add complete message
      const assistantMessage = {
        id: Date.now(),
        role: 'assistant',
        content: fullContent,
        provider: selectedProvider,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setStreamingContent('');

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now(),
        role: 'assistant',
        content: '❌ Sorry, I encountered an error. Please try again.',
        provider: 'error',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const copyToClipboard = (content, id) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const MessageBubble = ({ message }) => {
    const isUser = message.role === 'user';
    const isSystem = message.provider === 'system';

    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div className={`flex items-start space-x-2 max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
          {/* Avatar */}
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? 'bg-primary' : isSystem ? 'bg-purple-600' : 'bg-green-600'
          }`}>
            {isUser ? <User size={16} /> : <Bot size={16} />}
          </div>

          {/* Message Content */}
          <div className={`rounded-lg p-4 ${
            isUser 
              ? 'bg-primary text-white' 
              : 'bg-surface text-gray-100 border border-gray-700'
          }`}>
            {!isUser && !isSystem && (
              <div className="flex items-center space-x-2 mb-2 text-xs text-gray-400">
                <Sparkles size={12} />
                <span className="capitalize">{message.provider}</span>
              </div>
            )}
            
            <div className="whitespace-pre-wrap break-words">
              {message.content}
            </div>

            {/* Copy button for assistant messages */}
            {!isUser && (
              <button
                onClick={() => copyToClipboard(message.content, message.id)}
                className="mt-2 text-xs text-gray-400 hover:text-white flex items-center space-x-1"
              >
                {copiedId === message.id ? (
                  <>
                    <Check size={12} />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy size={12} />
                    <span>Copy</span>
                  </>
                )}
              </button>
            )}

            <div className="mt-2 text-xs opacity-50">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        </div>
      </motion.div>
    );
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <div className="bg-surface border-b border-gray-700 p-4">
        <div className="flex items-center justify-between max-w-6xl mx-auto">
          <div>
            <h1 className="text-2xl font-bold text-white">💬 AI Chat</h1>
            <p className="text-sm text-gray-400">Powered by multiple AI providers</p>
          </div>
          
          {/* Provider Selector */}
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-400">Provider:</label>
            <select
              value={selectedProvider}
              onChange={(e) => setSelectedProvider(e.target.value)}
              className="bg-background text-white px-3 py-2 rounded border border-gray-700 focus:border-primary outline-none"
              disabled={isLoading}
            >
              <option value="nvidia">NVIDIA</option>
              <option value="sambanova">SambaNova</option>
              <option value="cerebras">Cerebras</option>
            </select>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 max-w-6xl w-full mx-auto">
        <AnimatePresence>
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </AnimatePresence>

        {/* Streaming Message */}
        {streamingContent && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start mb-4"
          >
            <div className="flex items-start space-x-2 max-w-3xl">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 flex items-center justify-center">
                <Bot size={16} />
              </div>
              <div className="bg-surface text-gray-100 border border-gray-700 rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-2 text-xs text-gray-400">
                  <Sparkles size={12} />
                  <span className="capitalize">{selectedProvider}</span>
                  <span className="animate-pulse">●</span>
                </div>
                <div className="whitespace-pre-wrap break-words">
                  {streamingContent}
                  <span className="animate-pulse">▊</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {isLoading && !streamingContent && (
          <div className="flex justify-start mb-4">
            <div className="flex items-center space-x-2 bg-surface rounded-lg p-4">
              <Loader className="animate-spin text-primary" size={20} />
              <span className="text-gray-400">Thinking...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-surface border-t border-gray-700 p-4">
        <div className="max-w-6xl mx-auto flex items-end space-x-2">
          <div className="flex-1">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message... (Shift+Enter for new line)"
              className="w-full bg-background text-white rounded-lg p-3 border border-gray-700 focus:border-primary outline-none resize-none"
              rows={3}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="bg-primary hover:bg-primary/80 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg p-3 transition-colors"
          >
            {isLoading ? (
              <Loader className="animate-spin" size={24} />
            ) : (
              <Send size={24} />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;