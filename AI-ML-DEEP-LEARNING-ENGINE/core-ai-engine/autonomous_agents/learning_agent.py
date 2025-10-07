"""
🧠 Learning Agent
Self-improving agent with learning capabilities
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime
from collections import deque
import logging

logger = logging.getLogger(__name__)


class LearningAgent:
    """
    Learning Agent - Improves performance through experience
    
    Learning Methods:
    - Experience replay
    - Performance tracking
    - Strategy adjustment
    - Pattern recognition
    """
    
    def __init__(self, agent_id: str, learning_rate: float = 0.01):
        self.id = agent_id
        self.name = f"Learner-{agent_id}"
        self.status = "idle"
        self.learning_rate = learning_rate
        
        # Learning components
        self.experience_buffer = deque(maxlen=1000)
        self.knowledge_base: Dict[str, Any] = {}
        self.strategy_weights: Dict[str, float] = {
            "speed": 0.33,
            "accuracy": 0.33,
            "efficiency": 0.34
        }
        
        # Performance tracking
        self.learning_iterations = 0
        self.performance_history: List[float] = []
        
        self.capabilities = ["learning", "adaptation", "optimization"]
        
        logger.info(f"🧠 Learning Agent {self.id} initialized")
    
    def add_experience(self, experience: Dict[str, Any]) -> None:
        """
        Add experience to learning buffer
        
        Args:
            experience: Experience data
        """
        self.experience_buffer.append({
            **experience,
            "timestamp": datetime.now()
        })
        
        logger.debug(f"📝 Added experience to buffer (size: {len(self.experience_buffer)})")
    
    async def learn(self) -> Dict[str, Any]:
        """
        Learn from accumulated experiences
        
        Returns:
            Learning results
        """
        if len(self.experience_buffer) < 10:
            return {
                "status": "insufficient_data",
                "message": "Need more experiences to learn"
            }
        
        logger.info(f"🧠 Learning from {len(self.experience_buffer)} experiences")
        
        self.status = "learning"
        
        try:
            # Simulate learning process
            await asyncio.sleep(0.3)
            
            # Analyze experiences
            successful_experiences = [
                exp for exp in self.experience_buffer 
                if exp.get("status") == "success"
            ]
            
            # Calculate performance
            success_rate = len(successful_experiences) / len(self.experience_buffer)
            
            # Update strategy weights based on performance
            if success_rate > 0.9:
                # High success - prioritize speed
                self.strategy_weights["speed"] += self.learning_rate
            elif success_rate < 0.7:
                # Low success - prioritize accuracy
                self.strategy_weights["accuracy"] += self.learning_rate
            else:
                # Balanced - prioritize efficiency
                self.strategy_weights["efficiency"] += self.learning_rate
            
            # Normalize weights
            total_weight = sum(self.strategy_weights.values())
            self.strategy_weights = {
                k: v / total_weight 
                for k, v in self.strategy_weights.items()
            }
            
            # Update metrics
            self.learning_iterations += 1
            self.performance_history.append(success_rate)
            
            logger.info(f"✅ Learning complete. Success rate: {success_rate:.2%}")
            
            return {
                "status": "success",
                "iterations": self.learning_iterations,
                "success_rate": success_rate,
                "strategy_weights": self.strategy_weights
            }
            
        finally:
            self.status = "idle"
    
    async def execute(self, task: Any) -> Dict[str, Any]:
        """
        Execute task with learned strategies
        
        Args:
            task: Task to execute
            
        Returns:
            Execution result
        """
        start_time = datetime.now()
        self.status = "working"
        
        try:
            logger.info(f"🧠 Executing task with learned strategies: {task.id}")
            
            # Apply learned strategies
            execution_strategy = self._select_strategy()
            
            # Simulate execution
            await asyncio.sleep(0.2)
            
            # Create result
            result = {
                "status": "success",
                "strategy": execution_strategy,
                "result": f"Executed {task.type} using {execution_strategy} strategy"
            }
            
            # Record experience
            self.add_experience({
                "task_id": task.id,
                "task_type": task.type,
                "strategy": execution_strategy,
                "status": "success",
                "duration": (datetime.now() - start_time).total_seconds()
            })
            
            logger.info(f"✅ Task {task.id} executed using {execution_strategy} strategy")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Execution failed: {e}")
            
            # Record failed experience
            self.add_experience({
                "task_id": task.id,
                "status": "failed",
                "error": str(e)
            })
            
            return {
                "status": "failed",
                "error": str(e)
            }
        finally:
            self.status = "idle"
    
    def _select_strategy(self) -> str:
        """Select best strategy based on learned weights"""
        return max(self.strategy_weights, key=self.strategy_weights.get)
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        avg_performance = 0.0
        if self.performance_history:
            avg_performance = sum(self.performance_history) / len(self.performance_history)
        
        return {
            "iterations": self.learning_iterations,
            "experiences": len(self.experience_buffer),
            "avg_performance": round(avg_performance, 4),
            "strategy_weights": self.strategy_weights,
            "performance_trend": self.performance_history[-10:] if self.performance_history else []
        }
    
    def __repr__(self):
        return f"<LearningAgent {self.id}: {self.learning_iterations} iterations, {len(self.experience_buffer)} experiences>"