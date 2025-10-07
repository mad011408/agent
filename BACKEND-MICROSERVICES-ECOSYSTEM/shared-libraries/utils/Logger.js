/**
 * 📝 Logger Utility
 * Centralized logging for all services
 */

import winston from 'winston';

const { combine, timestamp, printf, colorize, errors } = winston.format;

/**
 * Custom log format
 */
const customFormat = printf(({ level, message, timestamp, stack, ...metadata }) => {
  let msg = `${timestamp} [${level}]: ${message}`;
  
  if (Object.keys(metadata).length > 0) {
    msg += ` ${JSON.stringify(metadata)}`;
  }
  
  if (stack) {
    msg += `\n${stack}`;
  }
  
  return msg;
});

/**
 * Create logger instance
 */
const createLogger = (serviceName = 'ai-agent-system') => {
  return winston.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    format: combine(
      errors({ stack: true }),
      timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
      customFormat
    ),
    defaultMeta: { service: serviceName },
    transports: [
      // Console output
      new winston.transports.Console({
        format: combine(
          colorize(),
          customFormat
        )
      }),
      
      // Error log file
      new winston.transports.File({
        filename: 'logs/error.log',
        level: 'error',
        maxsize: 5242880, // 5MB
        maxFiles: 5
      }),
      
      // Combined log file
      new winston.transports.File({
        filename: 'logs/combined.log',
        maxsize: 5242880,
        maxFiles: 5
      })
    ]
  });
};

/**
 * Logger class with additional utilities
 */
export class Logger {
  constructor(serviceName) {
    this.logger = createLogger(serviceName);
    this.serviceName = serviceName;
  }

  /**
   * Log info message
   */
  info(message, metadata = {}) {
    this.logger.info(message, metadata);
  }

  /**
   * Log error message
   */
  error(message, error = null, metadata = {}) {
    if (error instanceof Error) {
      this.logger.error(message, {
        ...metadata,
        error: error.message,
        stack: error.stack
      });
    } else {
      this.logger.error(message, metadata);
    }
  }

  /**
   * Log warning message
   */
  warn(message, metadata = {}) {
    this.logger.warn(message, metadata);
  }

  /**
   * Log debug message
   */
  debug(message, metadata = {}) {
    this.logger.debug(message, metadata);
  }

  /**
   * Log API request
   */
  logRequest(req) {
    this.info('Incoming request', {
      method: req.method,
      path: req.path,
      query: req.query,
      ip: req.ip,
      userAgent: req.get('user-agent')
    });
  }

  /**
   * Log API response
   */
  logResponse(req, res, duration) {
    this.info('Outgoing response', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: `${duration}ms`
    });
  }

  /**
   * Log database operation
   */
  logDatabase(operation, table, duration = null) {
    const meta = { operation, table };
    if (duration) meta.duration = `${duration}ms`;
    
    this.debug('Database operation', meta);
  }

  /**
   * Log performance metric
   */
  logPerformance(operation, duration, metadata = {}) {
    this.info('Performance metric', {
      operation,
      duration: `${duration}ms`,
      ...metadata
    });
  }
}

export default Logger;