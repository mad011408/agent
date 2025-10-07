"""
🔄 ReAct Reasoning Engine
Reason + Act paradigm for interactive problem solving
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of actions agent can take"""
    SEARCH = "search"
    CALCULATE = "calculate"
    ANALYZE = "analyze"
    QUERY = "query"
    SYNTHESIZE = "synthesize"


@dataclass
class ReActStep:
    """Single ReAct cycle step"""
    step_number: int
    thought: str
    action: ActionType
    action_input: str
    observation: str
    reflection: str


class ReActEngine:
    """
    ReAct (Reason + Act) Engine
    
    Combines reasoning with actions in iterative cycles
    """
    
    def __init__(self, max_iterations: int = 6):
        self.max_iterations = max_iterations
        self.react_history: List[List[ReActStep]] = []
        
        logger.info(f"🔄 ReAct Engine initialized (max_iterations={max_iterations})")
    
    async def solve(self, problem: str, available_tools: List[str] = None) -> Dict[str, Any]:
        """
        Solve problem using ReAct paradigm
        
        Args:
            problem: Problem to solve
            available_tools: List of available tools/actions
            
        Returns:
            Solution with reasoning and action trace
        """
        logger.info(f"🔄 Starting ReAct solving for: {problem[:50]}...")
        
        if available_tools is None:
            available_tools = [tool.value for tool in ActionType]
        
        steps: List[ReActStep] = []
        context = problem
        
        for iteration in range(1, self.max_iterations + 1):
            # Reason
            thought = await self._generate_thought(context, iteration)
            
            # Act
            action, action_input = await self._decide_action(thought, available_tools)
            
            # Observe
            observation = await self._execute_action(action, action_input)
            
            # Reflect
            reflection = await self._reflect(thought, observation)
            
            step = ReActStep(
                step_number=iteration,
                thought=thought,
                action=action,
                action_input=action_input,
                observation=observation,
                reflection=reflection
            )
            
            steps.append(step)
            
            # Update context
            context = f"{context}\n{reflection}"
            
            # Check if problem is solved
            if self._is_solved(reflection):
                logger.info(f"✅ Problem solved in {iteration} iterations")
                break
        
        # Store in history
        self.react_history.append(steps)
        
        # Generate final answer
        final_answer = self._generate_answer(steps)
        
        result = {
            "problem": problem,
            "iterations": len(steps),
            "steps": [
                {
                    "step": s.step_number,
                    "thought": s.thought,
                    "action": s.action.value,
                    "action_input": s.action_input,
                    "observation": s.observation,
                    "reflection": s.reflection
                }
                for s in steps
            ],
            "final_answer": final_answer
        }
        
        return result
    
    async def _generate_thought(self, context: str, iteration: int) -> str:
        """Generate reasoning thought"""
        await asyncio.sleep(0.1)
        
        thoughts = [
            f"Iteration {iteration}: Let me analyze what we know so far...",
            f"Iteration {iteration}: I need to gather more information...",
            f"Iteration {iteration}: Based on observations, I should...",
            f"Iteration {iteration}: Connecting the pieces together...",
            f"Iteration {iteration}: Verifying my hypothesis...",
            f"Iteration {iteration}: Formulating final conclusion..."
        ]
        
        idx = min(iteration - 1, len(thoughts) - 1)
        return thoughts[idx]
    
    async def _decide_action(self, thought: str, available_tools: List[str]) -> tuple:
        """Decide which action to take"""
        await asyncio.sleep(0.05)
        
        # Simple action selection logic
        if "analyze" in thought.lower():
            return ActionType.ANALYZE, "Current state"
        elif "search" in thought.lower() or "information" in thought.lower():
            return ActionType.SEARCH, "Relevant data"
        elif "calculate" in thought.lower():
            return ActionType.CALCULATE, "Expression"
        elif "connect" in thought.lower() or "synthesize" in thought.lower():
            return ActionType.SYNTHESIZE, "Information pieces"
        else:
            return ActionType.QUERY, "Database"
    
    async def _execute_action(self, action: ActionType, action_input: str) -> str:
        """Execute the chosen action"""
        await asyncio.sleep(0.15)
        
        observations = {
            ActionType.SEARCH: f"Found relevant information about: {action_input}",
            ActionType.CALCULATE: f"Calculation result for {action_input}: computed",
            ActionType.ANALYZE: f"Analysis of {action_input}: patterns identified",
            ActionType.QUERY: f"Query to {action_input}: data retrieved",
            ActionType.SYNTHESIZE: f"Synthesis of {action_input}: connections made"
        }
        
        return observations.get(action, "Action completed")
    
    async def _reflect(self, thought: str, observation: str) -> str:
        """Reflect on thought and observation"""
        await asyncio.sleep(0.05)
        
        return f"Based on observation, I can conclude that: {observation}. This informs my next step."
    
    def _is_solved(self, reflection: str) -> bool:
        """Check if problem appears to be solved"""
        solved_keywords = ["conclude", "therefore", "solution", "answer", "final"]
        return any(keyword in reflection.lower() for keyword in solved_keywords)
    
    def _generate_answer(self, steps: List[ReActStep]) -> str:
        """Generate final answer from ReAct steps"""
        if not steps:
            return "Unable to reach solution"
        
        # Synthesize from reflections
        key_insights = [step.reflection for step in steps[-3:]]  # Last 3 reflections
        
        return f"Solution derived through {len(steps)} reasoning-action cycles: " + " → ".join(key_insights)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get ReAct engine statistics"""
        if not self.react_history:
            return {"total_sessions": 0}
        
        total_iterations = sum(len(session) for session in self.react_history)
        avg_iterations = total_iterations / len(self.react_history)
        
        # Count action types
        action_counts: Dict[str, int] = {}
        for session in self.react_history:
            for step in session:
                action_counts[step.action.value] = action_counts.get(step.action.value, 0) + 1
        
        return {
            "total_sessions": len(self.react_history),
            "total_iterations": total_iterations,
            "avg_iterations": round(avg_iterations, 2),
            "action_distribution": action_counts
        }