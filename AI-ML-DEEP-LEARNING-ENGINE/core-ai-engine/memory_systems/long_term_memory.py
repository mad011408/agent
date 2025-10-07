"""
📚 Long Term Memory
Persistent knowledge storage and retrieval
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """Single knowledge entry"""
    id: str
    category: str
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    accessed_count: int = 0
    last_accessed: Optional[datetime] = None
    relevance_score: float = 1.0


class LongTermMemory:
    """
    Long-Term Memory System
    
    Persistent storage of knowledge with decay and reinforcement
    """
    
    def __init__(self, decay_rate: float = 0.01):
        self.decay_rate = decay_rate
        self.knowledge_base: Dict[str, KnowledgeEntry] = {}
        self.category_index: Dict[str, List[str]] = {}
        self.tag_index: Dict[str, List[str]] = {}
        
        logger.info(f"📚 Long Term Memory initialized (decay_rate={decay_rate})")
    
    def store(
        self,
        category: str,
        title: str,
        content: str,
        tags: List[str] = None
    ) -> str:
        """
        Store knowledge in long-term memory
        
        Args:
            category: Knowledge category
            title: Knowledge title
            content: Knowledge content
            tags: Associated tags
            
        Returns:
            Knowledge entry ID
        """
        entry_id = f"{category}_{len(self.knowledge_base)}"
        tags = tags or []
        
        entry = KnowledgeEntry(
            id=entry_id,
            category=category,
            title=title,
            content=content,
            tags=tags
        )
        
        self.knowledge_base[entry_id] = entry
        
        # Update indexes
        if category not in self.category_index:
            self.category_index[category] = []
        self.category_index[category].append(entry_id)
        
        for tag in tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(entry_id)
        
        logger.info(f"Stored knowledge: {entry_id}")
        
        return entry_id
    
    def recall(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Recall knowledge by ID (reinforces memory)
        
        Args:
            entry_id: Knowledge entry ID
            
        Returns:
            Knowledge entry or None
        """
        if entry_id not in self.knowledge_base:
            return None
        
        entry = self.knowledge_base[entry_id]
        
        # Reinforce memory through access
        entry.accessed_count += 1
        entry.last_accessed = datetime.now()
        entry.relevance_score = min(1.0, entry.relevance_score + 0.1)
        
        return {
            "id": entry.id,
            "category": entry.category,
            "title": entry.title,
            "content": entry.content,
            "tags": entry.tags,
            "relevance": entry.relevance_score
        }
    
    def search_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Search knowledge by category"""
        if category not in self.category_index:
            return []
        
        results = []
        for entry_id in self.category_index[category]:
            entry = self.knowledge_base[entry_id]
            results.append({
                "id": entry.id,
                "title": entry.title,
                "content": entry.content,
                "relevance": entry.relevance_score
            })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return results
    
    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Search knowledge by tags"""
        matching_ids = set()
        
        for tag in tags:
            if tag in self.tag_index:
                matching_ids.update(self.tag_index[tag])
        
        results = []
        for entry_id in matching_ids:
            entry = self.knowledge_base[entry_id]
            
            # Calculate tag match score
            matched_tags = set(tags) & set(entry.tags)
            tag_score = len(matched_tags) / len(tags)
            
            results.append({
                "id": entry.id,
                "title": entry.title,
                "content": entry.content,
                "matched_tags": list(matched_tags),
                "score": tag_score * entry.relevance_score
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results
    
    def search_text(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Full-text search in knowledge base
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            Matching knowledge entries
        """
        query_lower = query.lower()
        results = []
        
        for entry in self.knowledge_base.values():
            score = 0.0
            
            # Check title match
            if query_lower in entry.title.lower():
                score += 2.0
            
            # Check content match
            if query_lower in entry.content.lower():
                score += 1.0
            
            # Check tag match
            for tag in entry.tags:
                if query_lower in tag.lower():
                    score += 0.5
            
            if score > 0:
                results.append({
                    "id": entry.id,
                    "title": entry.title,
                    "content": entry.content,
                    "category": entry.category,
                    "score": score * entry.relevance_score
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:top_k]
    
    def apply_decay(self) -> None:
        """Apply memory decay to all entries"""
        for entry in self.knowledge_base.values():
            if entry.last_accessed:
                # Calculate time since last access
                days_since_access = (datetime.now() - entry.last_accessed).days
                decay = self.decay_rate * days_since_access
                
                entry.relevance_score = max(0.1, entry.relevance_score - decay)
        
        logger.info("Applied memory decay to all entries")
    
    def consolidate_knowledge(self) -> None:
        """Remove low-relevance knowledge"""
        initial_count = len(self.knowledge_base)
        
        # Remove entries with very low relevance
        to_remove = [
            entry_id for entry_id, entry in self.knowledge_base.items()
            if entry.relevance_score < 0.2 and entry.accessed_count < 2
        ]
        
        for entry_id in to_remove:
            del self.knowledge_base[entry_id]
        
        # Rebuild indexes
        self._rebuild_indexes()
        
        logger.info(f"Consolidated knowledge: removed {len(to_remove)} entries")
    
    def _rebuild_indexes(self) -> None:
        """Rebuild category and tag indexes"""
        self.category_index = {}
        self.tag_index = {}
        
        for entry in self.knowledge_base.values():
            # Category index
            if entry.category not in self.category_index:
                self.category_index[entry.category] = []
            self.category_index[entry.category].append(entry.id)
            
            # Tag index
            for tag in entry.tags:
                if tag not in self.tag_index:
                    self.tag_index[tag] = []
                self.tag_index[tag].append(entry.id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if not self.knowledge_base:
            return {"total_entries": 0}
        
        return {
            "total_entries": len(self.knowledge_base),
            "categories": len(self.category_index),
            "tags": len(self.tag_index),
            "avg_relevance": sum(e.relevance_score for e in self.knowledge_base.values()) / len(self.knowledge_base),
            "total_accesses": sum(e.accessed_count for e in self.knowledge_base.values())
        }
    
    def export_knowledge(self) -> str:
        """Export knowledge base to JSON"""
        export_data = []
        
        for entry in self.knowledge_base.values():
            export_data.append({
                "id": entry.id,
                "category": entry.category,
                "title": entry.title,
                "content": entry.content,
                "tags": entry.tags,
                "relevance_score": entry.relevance_score
            })
        
        return json.dumps(export_data, indent=2)