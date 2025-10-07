"""
💬 Conversation Memory
Short-term conversational context management
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import logging

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Single conversation message"""
    role: str  # user, assistant, system
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationMemory:
    """
    Conversation Memory System
    
    Manages short-term conversational context with sliding window
    """
    
    def __init__(self, max_messages: int = 50, max_tokens: int = 4000):
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.messages: deque = deque(maxlen=max_messages)
        self.conversation_id: Optional[str] = None
        self.metadata: Dict[str, Any] = {}
        
        logger.info(f"💬 Conversation Memory initialized (max_messages={max_messages})")
    
    def add_message(self, role: str, content: str, metadata: Dict = None) -> None:
        """
        Add message to conversation memory
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Additional metadata
        """
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        
        logger.debug(f"Added {role} message to memory (total: {len(self.messages)})")
        
        # Trim if exceeds token limit
        self._trim_to_token_limit()
    
    def get_messages(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get conversation messages
        
        Args:
            last_n: Get only last N messages
            
        Returns:
            List of message dictionaries
        """
        messages = list(self.messages)
        
        if last_n:
            messages = messages[-last_n:]
        
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
    
    def get_context_window(self, max_tokens: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get messages within token limit
        
        Args:
            max_tokens: Maximum tokens (uses instance default if None)
            
        Returns:
            Messages within token limit
        """
        max_tokens = max_tokens or self.max_tokens
        
        # Simple token estimation (4 chars ≈ 1 token)
        messages = []
        total_tokens = 0
        
        for msg in reversed(self.messages):
            msg_tokens = len(msg.content) // 4
            
            if total_tokens + msg_tokens > max_tokens:
                break
            
            messages.insert(0, {
                "role": msg.role,
                "content": msg.content
            })
            total_tokens += msg_tokens
        
        return messages
    
    def _trim_to_token_limit(self) -> None:
        """Trim messages to stay within token limit"""
        total_tokens = sum(len(msg.content) // 4 for msg in self.messages)
        
        while total_tokens > self.max_tokens and len(self.messages) > 1:
            # Remove oldest message (except system message if first)
            if self.messages[0].role == "system" and len(self.messages) > 1:
                removed = self.messages.__getitem__(1)
                self.messages.remove(removed)
            else:
                self.messages.popleft()
            
            total_tokens = sum(len(msg.content) // 4 for msg in self.messages)
    
    def clear(self) -> None:
        """Clear all messages"""
        self.messages.clear()
        logger.info("Conversation memory cleared")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        if not self.messages:
            return {
                "total_messages": 0,
                "estimated_tokens": 0
            }
        
        messages_by_role = {}
        for msg in self.messages:
            messages_by_role[msg.role] = messages_by_role.get(msg.role, 0) + 1
        
        return {
            "total_messages": len(self.messages),
            "messages_by_role": messages_by_role,
            "estimated_tokens": sum(len(msg.content) // 4 for msg in self.messages),
            "first_message_time": self.messages[0].timestamp.isoformat(),
            "last_message_time": self.messages[-1].timestamp.isoformat()
        }