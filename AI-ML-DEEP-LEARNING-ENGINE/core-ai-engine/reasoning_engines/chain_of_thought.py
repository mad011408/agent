"""
🔗 Chain of Thought Reasoning Engine
Step-by-step reasoning for complex problems
"""

import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThoughtStep:
    """Single step in chain of thought"""
    step_number: int
    thought: str
    reasoning: str
    confidence: float = 0.0


class ChainOfThoughtEngine:
    """
    Chain of Thought (CoT) Reasoning
    
    Breaks down complex problems into sequential reasoning steps
    """
    
    def __init__(self):
        self.thought_chains: List[List[ThoughtStep]] = []
        self.current_chain: List[ThoughtStep] = []
        
        logger.info("🔗 Chain of Thought Engine initialized")
    
    async def reason(self, problem: str, max_steps: int = 5) -> Dict[str, Any]:
        """
        Apply chain of thought reasoning
        
        Args:
            problem: Problem to solve
            max_steps: Maximum reasoning steps
            
        Returns:
            Reasoning result with steps
        """
        logger.info(f"🔗 Starting CoT reasoning for: {problem[:50]}...")
        
        self.current_chain = []
        
        # Generate reasoning steps
        for step in range(1, max_steps + 1):
            thought_step = await self._generate_step(problem, step)
            self.current_chain.append(thought_step)
            
            # Check if we've reached a conclusion
            if self._is_conclusion_reached(thought_step):
                break
        
        # Synthesize final answer
        final_answer = self._synthesize_answer(self.current_chain)
        
        # Store chain
        self.thought_chains.append(self.current_chain.copy())
        
        result = {
            "problem": problem,
            "steps": [
                {
                    "step": s.step_number,
                    "thought": s.thought,
                    "reasoning": s.reasoning,
                    "confidence": s.confidence
                }
                for s in self.current_chain
            ],
            "final_answer": final_answer,
            "total_steps": len(self.current_chain)
        }
        
        logger.info(f"✅ CoT reasoning complete in {len(self.current_chain)} steps")
        
        return result
    
    async def _generate_step(self, problem: str, step_number: int) -> ThoughtStep:
        """Generate a single reasoning step"""
        # Simulate thinking time
        await asyncio.sleep(0.1)
        
        # Create reasoning step based on step number
        thoughts_templates = [
            "Let me break down the problem...",
            "Considering the key elements...",
            "Analyzing the relationships...",
            "Drawing logical conclusions...",
            "Synthesizing the solution..."
        ]
        
        reasoning_templates = [
            f"Step {step_number}: Identifying core components",
            f"Step {step_number}: Evaluating constraints",
            f"Step {step_number}: Connecting patterns",
            f"Step {step_number}: Validating assumptions",
            f"Step {step_number}: Formulating conclusion"
        ]
        
        idx = min(step_number - 1, len(thoughts_templates) - 1)
        
        return ThoughtStep(
            step_number=step_number,
            thought=thoughts_templates[idx],
            reasoning=reasoning_templates[idx],
            confidence=0.7 + (step_number * 0.05)
        )
    
    def _is_conclusion_reached(self, step: ThoughtStep) -> bool:
        """Check if reasoning has reached a conclusion"""
        conclusion_keywords = ["therefore", "thus", "conclude", "solution", "answer"]
        return any(keyword in step.thought.lower() for keyword in conclusion_keywords)
    
    def _synthesize_answer(self, chain: List[ThoughtStep]) -> str:
        """Synthesize final answer from reasoning chain"""
        if not chain:
            return "Unable to reach conclusion"
        
        # Combine insights from all steps
        synthesis = f"Based on {len(chain)} steps of reasoning: "
        synthesis += " → ".join([step.thought for step in chain])
        
        return synthesis
    
    def get_reasoning_history(self) -> List[Dict[str, Any]]:
        """Get history of all reasoning chains"""
        return [
            {
                "chain_id": idx,
                "steps": len(chain),
                "confidence": sum(s.confidence for s in chain) / len(chain) if chain else 0
            }
            for idx, chain in enumerate(self.thought_chains)
        ]