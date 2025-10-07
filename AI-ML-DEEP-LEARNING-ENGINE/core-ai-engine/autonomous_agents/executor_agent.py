"""
⚡ Executor Agent
Executes specific tasks with high efficiency
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ExecutorAgent:
    """
    Executor Agent - Performs actual task execution
    
    Specializations:
    - Code execution
    - Data processing
    - API calls
    - File operations
    """
    
    def __init__(self, agent_id: str, specialization: str = "general"):
        self.id = agent_id
        self.name = f"Executor-{specialization}-{agent_id}"
        self.specialization = specialization
        self.status = "idle"
        
        # Define capabilities based on specialization
        self.capabilities = self._get_capabilities(specialization)
        
        self.execution_count = 0
        self.success_count = 0
        self.total_execution_time = 0.0
        
        logger.info(f"⚡ Executor Agent {self.id} initialized (Specialization: {specialization})")
    
    def _get_capabilities(self, specialization: str) -> List[str]:
        """Get capabilities based on specialization"""
        capability_map = {
            "code": ["code_generation", "code_analysis", "refactoring"],
            "data": ["data_processing", "analysis", "transformation"],
            "api": ["api_calls", "integration", "webhook_handling"],
            "file": ["file_operations", "parsing", "formatting"],
            "general": ["execution", "processing", "general_tasks"]
        }
        return capability_map.get(specialization, capability_map["general"])
    
    async def execute(self, task: Any) -> Dict[str, Any]:
        """
        Execute a task
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        start_time = datetime.now()
        self.status = "executing"
        
        try:
            logger.info(f"⚡ Executing task: {task.id} (Type: {task.type})")
            
            # Simulate execution based on task type
            if task.type in self.capabilities:
                # Specialized execution
                result = await self._specialized_execution(task)
            else:
                # General execution
                result = await self._general_execution(task)
            
            # Update metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.execution_count += 1
            self.success_count += 1
            self.total_execution_time += duration
            
            logger.info(f"✅ Task {task.id} executed in {duration:.2f}s")
            
            return {
                "status": "success",
                "result": result,
                "duration": duration,
                "executor": self.id
            }
            
        except Exception as e:
            logger.error(f"❌ Execution failed for task {task.id}: {e}")
            
            self.execution_count += 1
            
            return {
                "status": "failed",
                "error": str(e),
                "executor": self.id
            }
        finally:
            self.status = "idle"
    
    async def _specialized_execution(self, task: Any) -> Any:
        """Perform specialized execution"""
        # Simulate specialized work
        await asyncio.sleep(0.1)
        
        return {
            "type": "specialized",
            "specialization": self.specialization,
            "result": f"Executed {task.type} with {self.specialization} specialization"
        }
    
    async def _general_execution(self, task: Any) -> Any:
        """Perform general execution"""
        # Simulate general work
        await asyncio.sleep(0.15)
        
        return {
            "type": "general",
            "result": f"Executed {task.type} task"
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        avg_execution_time = 0.0
        success_rate = 0.0
        
        if self.execution_count > 0:
            avg_execution_time = self.total_execution_time / self.execution_count
            success_rate = (self.success_count / self.execution_count) * 100
        
        return {
            "executions": self.execution_count,
            "successes": self.success_count,
            "success_rate": round(success_rate, 2),
            "avg_execution_time": round(avg_execution_time, 3),
            "specialization": self.specialization
        }
    
    def __repr__(self):
        return f"<ExecutorAgent {self.id} ({self.specialization}): {self.execution_count} executions>"