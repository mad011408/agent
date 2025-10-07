/**
 * ⚖️ Load Balancer Implementation
 * Distributes requests across multiple service instances
 */

export class LoadBalancer {
  constructor(servers = [], strategy = 'round-robin') {
    this.servers = servers;
    this.strategy = strategy;
    this.currentIndex = 0;
    
    // Health tracking
    this.serverHealth = new Map();
    servers.forEach(server => {
      this.serverHealth.set(server, {
        healthy: true,
        failureCount: 0,
        lastCheck: Date.now(),
        responseTime: 0
      });
    });
    
    // Metrics
    this.metrics = {
      totalRequests: 0,
      serverRequests: new Map()
    };
    
    servers.forEach(server => {
      this.metrics.serverRequests.set(server, 0);
    });
  }
  
  /**
   * Get next server based on strategy
   */
  getNextServer() {
    const healthyServers = this.getHealthyServers();
    
    if (healthyServers.length === 0) {
      throw new Error('No healthy servers available');
    }
    
    let server;
    
    switch (this.strategy) {
      case 'round-robin':
        server = this.roundRobin(healthyServers);
        break;
      case 'least-connections':
        server = this.leastConnections(healthyServers);
        break;
      case 'random':
        server = this.random(healthyServers);
        break;
      default:
        server = this.roundRobin(healthyServers);
    }
    
    this.metrics.totalRequests++;
    this.metrics.serverRequests.set(
      server,
      (this.metrics.serverRequests.get(server) || 0) + 1
    );
    
    return server;
  }
  
  /**
   * Round-robin selection
   */
  roundRobin(servers) {
    const server = servers[this.currentIndex % servers.length];
    this.currentIndex++;
    return server;
  }
  
  /**
   * Least connections selection
   */
  leastConnections(servers) {
    return servers.reduce((min, server) => {
      const minCount = this.metrics.serverRequests.get(min) || 0;
      const serverCount = this.metrics.serverRequests.get(server) || 0;
      return serverCount < minCount ? server : min;
    }, servers[0]);
  }
  
  /**
   * Random selection
   */
  random(servers) {
    return servers[Math.floor(Math.random() * servers.length)];
  }
  
  /**
   * Get healthy servers
   */
  getHealthyServers() {
    return this.servers.filter(server => {
      const health = this.serverHealth.get(server);
      return health && health.healthy;
    });
  }
  
  /**
   * Mark server as unhealthy
   */
  markUnhealthy(server) {
    const health = this.serverHealth.get(server);
    if (health) {
      health.healthy = false;
      health.failureCount++;
      health.lastCheck = Date.now();
      
      console.warn(`❌ Server marked unhealthy: ${server}`);
      
      // Auto-recovery attempt after 30 seconds
      setTimeout(() => this.markHealthy(server), 30000);
    }
  }
  
  /**
   * Mark server as healthy
   */
  markHealthy(server) {
    const health = this.serverHealth.get(server);
    if (health) {
      health.healthy = true;
      health.failureCount = 0;
      health.lastCheck = Date.now();
      
      console.log(`✅ Server marked healthy: ${server}`);
    }
  }
  
  /**
   * Add server
   */
  addServer(server) {
    if (!this.servers.includes(server)) {
      this.servers.push(server);
      this.serverHealth.set(server, {
        healthy: true,
        failureCount: 0,
        lastCheck: Date.now(),
        responseTime: 0
      });
      this.metrics.serverRequests.set(server, 0);
      
      console.log(`➕ Server added: ${server}`);
    }
  }
  
  /**
   * Remove server
   */
  removeServer(server) {
    const index = this.servers.indexOf(server);
    if (index > -1) {
      this.servers.splice(index, 1);
      this.serverHealth.delete(server);
      this.metrics.serverRequests.delete(server);
      
      console.log(`➖ Server removed: ${server}`);
    }
  }
  
  /**
   * Get metrics
   */
  getMetrics() {
    return {
      totalServers: this.servers.length,
      healthyServers: this.getHealthyServers().length,
      totalRequests: this.metrics.totalRequests,
      serverDistribution: Object.fromEntries(this.metrics.serverRequests),
      serverHealth: Object.fromEntries(this.serverHealth)
    };
  }
}