"""
👑 Master Agent
Top-level autonomous agent that coordinates all other agents
"""

import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Task definition"""
    id: str
    type: str
    description: str
    priority: int = 0
    status: str = "pending"
    assigned_to: Optional[str] = None
    result: Optional[Any] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class MasterAgent:
    """
    🎯 Master Agent - Top-level coordinator
    
    Capabilities:
    - Task decomposition
    - Agent orchestration
    - Resource allocation
    - Performance monitoring
    - Self-optimization
    """
    
    def __init__(self, agent_id: str = "master-001"):
        self.id = agent_id
        self.name = "Master Agent"
        self.status = "idle"
        self.subordinate_agents: Dict[str, Any] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        
        self.metrics = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "total_agents": 0,
            "avg_completion_time": 0.0
        }
        
        logger.info(f"🎯 Master Agent {self.id} initialized")
    
    def register_agent(self, agent: Any) -> None:
        """Register a subordinate agent"""
        self.subordinate_agents[agent.id] = agent
        self.metrics["total_agents"] = len(self.subordinate_agents)
        logger.info(f"✅ Registered agent: {agent.id} ({agent.name})")
    
    def decompose_task(self, task: Task) -> List[Task]:
        """
        Decompose a complex task into subtasks
        
        Args:
            task: Complex task to decompose
            
        Returns:
            List of subtasks
        """
        # Simple decomposition logic
        subtasks = []
        
        if task.type == "code_generation":
            subtasks = [
                Task(
                    id=f"{task.id}-1",
                    type="planning",
                    description="Plan code structure"
                ),
                Task(
                    id=f"{task.id}-2",
                    type="implementation",
                    description="Implement code"
                ),
                Task(
                    id=f"{task.id}-3",
                    type="testing",
                    description="Generate tests"
                )
            ]
        elif task.type == "research":
            subtasks = [
                Task(
                    id=f"{task.id}-1",
                    type="data_collection",
                    description="Collect information"
                ),
                Task(
                    id=f"{task.id}-2",
                    type="analysis",
                    description="Analyze data"
                ),
                Task(
                    id=f"{task.id}-3",
                    type="synthesis",
                    description="Synthesize findings"
                )
            ]
        else:
            # If can't decompose, return original task
            subtasks = [task]
        
        return subtasks
    
    def assign_task(self, task: Task) -> Optional[str]:
        """
        Assign task to most suitable agent
        
        Args:
            task: Task to assign
            
        Returns:
            Agent ID if assigned, None otherwise
        """
        # Find best agent for task
        best_agent = None
        best_score = -1
        
        for agent_id, agent in self.subordinate_agents.items():
            # Simple scoring based on agent capabilities
            score = 0
            
            if hasattr(agent, 'capabilities'):
                if task.type in agent.capabilities:
                    score += 10
            
            if hasattr(agent, 'status') and agent.status == 'idle':
                score += 5
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        if best_agent:
            task.assigned_to = best_agent.id
            logger.info(f"📋 Task {task.id} assigned to {best_agent.id}")
            return best_agent.id
        
        return None
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """
        Execute a task through the agent network
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        logger.info(f"⚙️ Executing task: {task.id} ({task.type})")
        
        self.status = "working"
        task.status = "in_progress"
        
        try:
            # Decompose if complex
            subtasks = self.decompose_task(task)
            
            # Execute subtasks
            results = []
            for subtask in subtasks:
                # Assign to agent
                agent_id = self.assign_task(subtask)
                
                if agent_id and agent_id in self.subordinate_agents:
                    agent = self.subordinate_agents[agent_id]
                    
                    # Execute through agent
                    if hasattr(agent, 'execute'):
                        result = await agent.execute(subtask)
                        results.append(result)
                    else:
                        # Simulate execution
                        await asyncio.sleep(0.1)
                        results.append({"status": "success", "result": f"Completed {subtask.type}"})
            
            # Mark as completed
            task.status = "completed"
            task.completed_at = datetime.now()
            task.result = results
            
            self.completed_tasks.append(task)
            self.metrics["tasks_processed"] += 1
            self.metrics["tasks_succeeded"] += 1
            
            logger.info(f"✅ Task {task.id} completed successfully")
            
            return {
                "task_id": task.id,
                "status": "success",
                "results": results
            }
            
        except Exception as e:
            logger.error(f"❌ Task {task.id} failed: {e}")
            
            task.status = "failed"
            task.result = {"error": str(e)}
            
            self.metrics["tasks_processed"] += 1
            self.metrics["tasks_failed"] += 1
            
            return {
                "task_id": task.id,
                "status": "failed",
                "error": str(e)
            }
        finally:
            self.status = "idle"
    
    async def process_queue(self) -> None:
        """Process all tasks in queue"""
        logger.info(f"🔄 Processing {len(self.task_queue)} tasks in queue")
        
        while self.task_queue:
            task = self.task_queue.pop(0)
            await self.execute_task(task)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        success_rate = 0
        if self.metrics["tasks_processed"] > 0:
            success_rate = (self.metrics["tasks_succeeded"] / self.metrics["tasks_processed"]) * 100
        
        return {
            **self.metrics,
            "success_rate": round(success_rate, 2),
            "queue_length": len(self.task_queue),
            "completed_count": len(self.completed_tasks)
        }
    
    def __repr__(self):
        return f"<MasterAgent {self.id}: {len(self.subordinate_agents)} agents, {len(self.task_queue)} queued>"