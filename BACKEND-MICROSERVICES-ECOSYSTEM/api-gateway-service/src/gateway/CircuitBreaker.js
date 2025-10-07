/**
 * 🔌 Circuit Breaker Pattern Implementation
 * Prevents cascading failures in microservices
 */

export class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 60000; // 1 minute
    this.monitoringPeriod = options.monitoringPeriod || 10000; // 10 seconds
    
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.nextAttempt = null;
    
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      circuitOpenCount: 0
    };
  }
  
  /**
   * Record a successful request
   */
  recordSuccess() {
    this.successCount++;
    this.metrics.successfulRequests++;
    this.metrics.totalRequests++;
    
    if (this.state === 'HALF_OPEN') {
      // Reset circuit if successful in half-open state
      this.reset();
    }
  }
  
  /**
   * Record a failed request
   */
  recordFailure() {
    this.failureCount++;
    this.metrics.failedRequests++;
    this.metrics.totalRequests++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.failureThreshold) {
      this.trip();
    }
  }
  
  /**
   * Record a request attempt
   */
  recordRequest() {
    if (this.state === 'OPEN' && Date.now() >= this.nextAttempt) {
      this.state = 'HALF_OPEN';
      this.failureCount = 0;
    }
  }
  
  /**
   * Trip the circuit breaker (open it)
   */
  trip() {
    this.state = 'OPEN';
    this.nextAttempt = Date.now() + this.resetTimeout;
    this.metrics.circuitOpenCount++;
    
    console.warn(`🔴 Circuit breaker OPEN - too many failures (${this.failureCount})`);
    
    // Auto-reset after timeout
    setTimeout(() => {
      if (this.state === 'OPEN') {
        this.state = 'HALF_OPEN';
        console.log('🟡 Circuit breaker HALF_OPEN - testing service');
      }
    }, this.resetTimeout);
  }
  
  /**
   * Reset the circuit breaker
   */
  reset() {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.nextAttempt = null;
    
    console.log('🟢 Circuit breaker CLOSED - service recovered');
  }
  
  /**
   * Check if circuit is open
   */
  isOpen() {
    return this.state === 'OPEN';
  }
  
  /**
   * Get current state
   */
  getState() {
    return this.state;
  }
  
  /**
   * Get time until reset
   */
  getResetTime() {
    if (this.state !== 'OPEN') return 0;
    return Math.max(0, this.nextAttempt - Date.now());
  }
  
  /**
   * Get metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount,
      failureRate: this.metrics.totalRequests > 0
        ? this.metrics.failedRequests / this.metrics.totalRequests
        : 0
    };
  }
}