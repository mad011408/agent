/**
 * 🎯 Master Orchestrator
 * Coordinates all autonomous agents and tasks
 */

export class MasterOrchestrator {
  constructor() {
    this.agents = new Map();
    this.tasks = new Map();
    this.activeWorkflows = new Map();
    
    this.metrics = {
      totalAgents: 0,
      activeAgents: 0,
      completedTasks: 0,
      failedTasks: 0,
      averageResponseTime: 0
    };
  }

  /**
   * Register a new agent
   */
  registerAgent(agent) {
    this.agents.set(agent.id, {
      ...agent,
      status: 'idle',
      lastActivity: Date.now(),
      tasksCompleted: 0,
      tasksActive: 0
    });
    
    this.metrics.totalAgents++;
    
    console.log(`✅ Agent registered: ${agent.id} (${agent.type})`);
    return agent.id;
  }

  /**
   * Assign task to best available agent
   */
  async assignTask(task) {
    const agent = this.findBestAgent(task.type, task.requirements);
    
    if (!agent) {
      throw new Error('No suitable agent available');
    }

    // Update agent status
    const agentData = this.agents.get(agent.id);
    agentData.status = 'busy';
    agentData.tasksActive++;

    // Store task
    this.tasks.set(task.id, {
      ...task,
      assignedAgent: agent.id,
      status: 'in_progress',
      startTime: Date.now()
    });

    console.log(`📋 Task ${task.id} assigned to agent ${agent.id}`);

    try {
      // Execute task
      const result = await this.executeTask(task, agent);
      
      // Mark task as completed
      this.completeTask(task.id, result);
      
      return result;
    } catch (error) {
      this.failTask(task.id, error);
      throw error;
    }
  }

  /**
   * Find the best agent for a task
   */
  findBestAgent(taskType, requirements = {}) {
    let bestAgent = null;
    let bestScore = -1;

    for (const [id, agent] of this.agents.entries()) {
      if (agent.status !== 'idle' && agent.tasksActive >= 3) continue;
      
      // Calculate agent suitability score
      let score = 0;
      
      // Type match
      if (agent.capabilities?.taskTypes?.includes(taskType)) {
        score += 10;
      }
      
      // Performance history
      score += agent.tasksCompleted * 0.1;
      
      // Current load (prefer less busy agents)
      score -= agent.tasksActive * 2;

      if (score > bestScore) {
        bestScore = score;
        bestAgent = agent;
      }
    }

    return bestAgent;
  }

  /**
   * Execute a task with an agent
   */
  async executeTask(task, agent) {
    console.log(`⚙️  Executing task ${task.id} with agent ${agent.id}`);
    
    // Simulate task execution
    // In real implementation, this would call the agent's execution endpoint
    await new Promise(resolve => setTimeout(resolve, 100));

    return {
      success: true,
      result: `Task ${task.id} completed by agent ${agent.id}`,
      executionTime: 100
    };
  }

  /**
   * Mark task as completed
   */
  completeTask(taskId, result) {
    const task = this.tasks.get(taskId);
    if (!task) return;

    task.status = 'completed';
    task.result = result;
    task.completedAt = Date.now();

    const agent = this.agents.get(task.assignedAgent);
    if (agent) {
      agent.status = 'idle';
      agent.tasksActive--;
      agent.tasksCompleted++;
      agent.lastActivity = Date.now();
    }

    this.metrics.completedTasks++;
    
    console.log(`✅ Task ${taskId} completed`);
  }

  /**
   * Mark task as failed
   */
  failTask(taskId, error) {
    const task = this.tasks.get(taskId);
    if (!task) return;

    task.status = 'failed';
    task.error = error.message;
    task.failedAt = Date.now();

    const agent = this.agents.get(task.assignedAgent);
    if (agent) {
      agent.status = 'idle';
      agent.tasksActive--;
    }

    this.metrics.failedTasks++;
    
    console.error(`❌ Task ${taskId} failed: ${error.message}`);
  }

  /**
   * Get orchestrator metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      activeAgents: Array.from(this.agents.values())
        .filter(a => a.status === 'busy').length,
      activeTasks: Array.from(this.tasks.values())
        .filter(t => t.status === 'in_progress').length
    };
  }

  /**
   * Get all agents
   */
  getAgents() {
    return Array.from(this.agents.values());
  }

  /**
   * Get all tasks
   */
  getTasks() {
    return Array.from(this.tasks.values());
  }
}