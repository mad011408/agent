"""
🌳 Tree of Thought Reasoning Engine
Explore multiple reasoning paths simultaneously
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThoughtNode:
    """Node in tree of thoughts"""
    id: str
    content: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    value: float = 0.0
    depth: int = 0


class TreeOfThoughtEngine:
    """
    Tree of Thought (ToT) Reasoning
    
    Explores multiple reasoning paths and evaluates them
    """
    
    def __init__(self, branching_factor: int = 3, max_depth: int = 4):
        self.branching_factor = branching_factor
        self.max_depth = max_depth
        self.nodes: Dict[str, ThoughtNode] = {}
        self.evaluation_count = 0
        
        logger.info(f"🌳 Tree of Thought Engine initialized (branching={branching_factor}, depth={max_depth})")
    
    async def reason(self, problem: str) -> Dict[str, Any]:
        """
        Apply tree of thought reasoning
        
        Args:
            problem: Problem to solve
            
        Returns:
            Best reasoning path and result
        """
        logger.info(f"🌳 Starting ToT reasoning for: {problem[:50]}...")
        
        # Reset tree
        self.nodes = {}
        self.evaluation_count = 0
        
        # Create root node
        root = ThoughtNode(
            id="root",
            content=f"Analyzing: {problem}",
            depth=0
        )
        self.nodes["root"] = root
        
        # Build thought tree
        await self._build_tree("root", problem)
        
        # Find best path
        best_path = self._find_best_path()
        
        result = {
            "problem": problem,
            "total_nodes": len(self.nodes),
            "evaluations": self.evaluation_count,
            "best_path": [
                {
                    "depth": node.depth,
                    "thought": node.content,
                    "value": node.value
                }
                for node in best_path
            ],
            "best_value": best_path[-1].value if best_path else 0.0
        }
        
        logger.info(f"✅ ToT reasoning complete. Best path has {len(best_path)} nodes")
        
        return result
    
    async def _build_tree(self, node_id: str, context: str, depth: int = 0) -> None:
        """Recursively build thought tree"""
        if depth >= self.max_depth:
            return
        
        node = self.nodes[node_id]
        
        # Generate child thoughts
        for i in range(self.branching_factor):
            child_id = f"{node_id}-{i}"
            
            child_content = await self._generate_thought(context, depth + 1, i)
            child_value = await self._evaluate_thought(child_content)
            
            child = ThoughtNode(
                id=child_id,
                content=child_content,
                parent_id=node_id,
                depth=depth + 1,
                value=child_value
            )
            
            self.nodes[child_id] = child
            node.children.append(child_id)
            
            # Recursively build subtree (prune low-value branches)
            if child_value > 0.5:
                await self._build_tree(child_id, child_content, depth + 1)
    
    async def _generate_thought(self, context: str, depth: int, branch: int) -> str:
        """Generate a thought at given depth and branch"""
        await asyncio.sleep(0.05)  # Simulate thinking
        
        thought_templates = [
            f"Approach {branch + 1}: Consider alternative perspective",
            f"Branch {branch + 1}: Explore different angle",
            f"Path {branch + 1}: Investigate related concept"
        ]
        
        return thought_templates[branch % len(thought_templates)]
    
    async def _evaluate_thought(self, thought: str) -> float:
        """Evaluate quality of a thought"""
        await asyncio.sleep(0.02)  # Simulate evaluation
        
        self.evaluation_count += 1
        
        # Simulate evaluation (in real system, use LLM)
        import random
        return random.uniform(0.3, 0.95)
    
    def _find_best_path(self) -> List[ThoughtNode]:
        """Find path with highest cumulative value"""
        if "root" not in self.nodes:
            return []
        
        def get_path_value(path: List[ThoughtNode]) -> float:
            return sum(node.value for node in path) / len(path) if path else 0.0
        
        def explore_paths(node_id: str, current_path: List[ThoughtNode]) -> List[ThoughtNode]:
            node = self.nodes[node_id]
            current_path = current_path + [node]
            
            if not node.children:
                return current_path
            
            # Explore all child paths
            paths = [
                explore_paths(child_id, current_path)
                for child_id in node.children
            ]
            
            # Return best path
            return max(paths, key=get_path_value)
        
        return explore_paths("root", [])
    
    def visualize_tree(self) -> str:
        """Create ASCII visualization of thought tree"""
        def build_viz(node_id: str, prefix: str = "", is_last: bool = True) -> List[str]:
            lines = []
            node = self.nodes[node_id]
            
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{node.content} (value: {node.value:.2f})")
            
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, child_id in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                lines.extend(build_viz(child_id, new_prefix, is_last_child))
            
            return lines
        
        if "root" not in self.nodes:
            return "Empty tree"
        
        return "\n".join(build_viz("root"))