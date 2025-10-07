"""
🔧 Data Preprocessor
Data preprocessing utilities for AI/ML
"""

import numpy as np
from typing import List, Dict, Any, Optional, Union


class DataPreprocessor:
    """
    Data Preprocessing Utilities
    
    Common data preprocessing operations for ML
    """
    
    @staticmethod
    def normalize(data: np.ndarray, method: str = "minmax") -> np.ndarray:
        """
        Normalize data
        
        Args:
            data: Input data
            method: Normalization method (minmax, zscore)
            
        Returns:
            Normalized data
        """
        if method == "minmax":
            min_val = np.min(data)
            max_val = np.max(data)
            return (data - min_val) / (max_val - min_val + 1e-8)
        
        elif method == "zscore":
            mean = np.mean(data)
            std = np.std(data)
            return (data - mean) / (std + 1e-8)
        
        else:
            raise ValueError(f"Unknown normalization method: {method}")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text data
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters (keep alphanumeric and basic punctuation)
        import re
        text = re.sub(r'[^a-zA-Z0-9\s\.,!?-]', '', text)
        
        return text.strip()
    
    @staticmethod
    def tokenize(text: str, max_length: Optional[int] = None) -> List[str]:
        """
        Simple tokenization
        
        Args:
            text: Input text
            max_length: Maximum number of tokens
            
        Returns:
            List of tokens
        """
        tokens = text.lower().split()
        
        if max_length:
            tokens = tokens[:max_length]
        
        return tokens
    
    @staticmethod
    def encode_categorical(categories: List[str]) -> Dict[str, int]:
        """
        Encode categorical variables
        
        Args:
            categories: List of categories
            
        Returns:
            Category to index mapping
        """
        unique_categories = sorted(set(categories))
        return {cat: idx for idx, cat in enumerate(unique_categories)}
    
    @staticmethod
    def split_data(
        data: np.ndarray,
        train_ratio: float = 0.8,
        shuffle: bool = True
    ) -> tuple:
        """
        Split data into train/test sets
        
        Args:
            data: Input data
            train_ratio: Training data ratio
            shuffle: Whether to shuffle data
            
        Returns:
            (train_data, test_data)
        """
        if shuffle:
            np.random.shuffle(data)
        
        split_idx = int(len(data) * train_ratio)
        
        train_data = data[:split_idx]
        test_data = data[split_idx:]
        
        return train_data, test_data
    
    @staticmethod
    def batch_data(data: np.ndarray, batch_size: int) -> List[np.ndarray]:
        """
        Create batches from data
        
        Args:
            data: Input data
            batch_size: Batch size
            
        Returns:
            List of batches
        """
        batches = []
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            batches.append(batch)
        
        return batches
    
    @staticmethod
    def handle_missing_values(
        data: np.ndarray,
        strategy: str = "mean"
    ) -> np.ndarray:
        """
        Handle missing values in data
        
        Args:
            data: Input data with potential NaN values
            strategy: Strategy (mean, median, zero)
            
        Returns:
            Data with missing values handled
        """
        if strategy == "mean":
            fill_value = np.nanmean(data)
        elif strategy == "median":
            fill_value = np.nanmedian(data)
        elif strategy == "zero":
            fill_value = 0
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        return np.nan_to_num(data, nan=fill_value)