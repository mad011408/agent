"""
🎯 Vector Memory
Semantic memory using vector embeddings
"""

import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """Single memory entry with embedding"""
    id: str
    content: str
    embedding: np.ndarray
    metadata: Dict[str, Any]
    importance: float = 0.5


class VectorMemory:
    """
    Vector-based Semantic Memory
    
    Stores and retrieves memories using vector similarity
    """
    
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        self.memories: List[MemoryEntry] = []
        self.memory_index: Dict[str, int] = {}
        
        logger.info(f"🎯 Vector Memory initialized (dim={embedding_dim})")
    
    def add_memory(
        self,
        content: str,
        embedding: Optional[np.ndarray] = None,
        metadata: Dict = None,
        importance: float = 0.5
    ) -> str:
        """
        Add memory with embedding
        
        Args:
            content: Memory content
            embedding: Vector embedding (generated if None)
            metadata: Additional metadata
            importance: Memory importance score
            
        Returns:
            Memory ID
        """
        memory_id = f"mem_{len(self.memories)}"
        
        if embedding is None:
            embedding = self._generate_embedding(content)
        
        memory = MemoryEntry(
            id=memory_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {},
            importance=importance
        )
        
        self.memories.append(memory)
        self.memory_index[memory_id] = len(self.memories) - 1
        
        logger.debug(f"Added memory {memory_id}")
        
        return memory_id
    
    def search(
        self,
        query: str,
        query_embedding: Optional[np.ndarray] = None,
        top_k: int = 5,
        threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search memories by semantic similarity
        
        Args:
            query: Search query
            query_embedding: Query embedding (generated if None)
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of matching memories with scores
        """
        if not self.memories:
            return []
        
        if query_embedding is None:
            query_embedding = self._generate_embedding(query)
        
        # Calculate similarities
        similarities = []
        for i, memory in enumerate(self.memories):
            similarity = self._cosine_similarity(query_embedding, memory.embedding)
            
            if similarity >= threshold:
                similarities.append({
                    "memory_id": memory.id,
                    "content": memory.content,
                    "similarity": float(similarity),
                    "importance": memory.importance,
                    "metadata": memory.metadata,
                    "score": float(similarity * memory.importance)  # Combined score
                })
        
        # Sort by combined score
        similarities.sort(key=lambda x: x["score"], reverse=True)
        
        return similarities[:top_k]
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text (simplified)"""
        # In production, use actual embedding model
        # This is a simplified hash-based approach
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(self.embedding_dim)
        return embedding / np.linalg.norm(embedding)
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between vectors"""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def update_importance(self, memory_id: str, importance: float) -> None:
        """Update memory importance score"""
        if memory_id in self.memory_index:
            idx = self.memory_index[memory_id]
            self.memories[idx].importance = importance
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Get memory by ID"""
        if memory_id in self.memory_index:
            idx = self.memory_index[memory_id]
            memory = self.memories[idx]
            return {
                "id": memory.id,
                "content": memory.content,
                "importance": memory.importance,
                "metadata": memory.metadata
            }
        return None
    
    def consolidate(self, similarity_threshold: float = 0.95) -> int:
        """
        Consolidate similar memories
        
        Args:
            similarity_threshold: Threshold for merging memories
            
        Returns:
            Number of memories consolidated
        """
        if len(self.memories) < 2:
            return 0
        
        consolidated_count = 0
        i = 0
        
        while i < len(self.memories):
            j = i + 1
            while j < len(self.memories):
                similarity = self._cosine_similarity(
                    self.memories[i].embedding,
                    self.memories[j].embedding
                )
                
                if similarity >= similarity_threshold:
                    # Merge memories
                    self.memories[i].importance = max(
                        self.memories[i].importance,
                        self.memories[j].importance
                    )
                    self.memories.pop(j)
                    consolidated_count += 1
                else:
                    j += 1
            i += 1
        
        # Rebuild index
        self.memory_index = {
            memory.id: idx 
            for idx, memory in enumerate(self.memories)
        }
        
        logger.info(f"Consolidated {consolidated_count} memories")
        
        return consolidated_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if not self.memories:
            return {"total_memories": 0}
        
        return {
            "total_memories": len(self.memories),
            "avg_importance": np.mean([m.importance for m in self.memories]),
            "embedding_dim": self.embedding_dim
        }