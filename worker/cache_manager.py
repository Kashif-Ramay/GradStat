"""
Simple in-memory cache for analysis results
Reduces computation time for repeated analyses
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from logger_config import logger


class AnalysisCache:
    """
    In-memory cache for analysis results
    
    Features:
    - Hash-based cache keys (file content + analysis options)
    - TTL (Time To Live) expiration
    - Automatic cleanup of expired entries
    - Memory-efficient (stores only results, not raw data)
    """
    
    def __init__(self, ttl_seconds: int = 3600, max_entries: int = 100):
        """
        Initialize cache
        
        Args:
            ttl_seconds: Time to live for cache entries (default: 1 hour)
            max_entries: Maximum number of entries to store (default: 100)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        logger.info(f"Analysis cache initialized (TTL: {ttl_seconds}s, Max: {max_entries} entries)")
    
    def _generate_key(self, file_content: bytes, options: Dict[str, Any]) -> str:
        """
        Generate cache key from file content and analysis options
        
        Args:
            file_content: Raw file bytes
            options: Analysis options dictionary
            
        Returns:
            str: SHA256 hash as cache key
        """
        # Create a deterministic string from options
        options_str = json.dumps(options, sort_keys=True)
        
        # Combine file content hash and options
        combined = hashlib.sha256(file_content).hexdigest() + options_str
        
        # Generate final cache key
        cache_key = hashlib.sha256(combined.encode()).hexdigest()
        
        return cache_key
    
    def get(self, file_content: bytes, options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis result
        
        Args:
            file_content: Raw file bytes
            options: Analysis options
            
        Returns:
            Cached result if found and not expired, None otherwise
        """
        cache_key = self._generate_key(file_content, options)
        
        # Check if key exists
        if cache_key not in self.cache:
            logger.debug(f"Cache MISS: {cache_key[:16]}...")
            return None
        
        entry = self.cache[cache_key]
        
        # Check if expired
        if time.time() - entry['timestamp'] > self.ttl_seconds:
            logger.debug(f"Cache EXPIRED: {cache_key[:16]}...")
            del self.cache[cache_key]
            return None
        
        # Cache hit!
        logger.info(f"Cache HIT: {cache_key[:16]}... (age: {int(time.time() - entry['timestamp'])}s)")
        entry['hits'] += 1
        
        return entry['result']
    
    def set(self, file_content: bytes, options: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Store analysis result in cache
        
        Args:
            file_content: Raw file bytes
            options: Analysis options
            result: Analysis result to cache
        """
        cache_key = self._generate_key(file_content, options)
        
        # Check if we need to evict old entries
        if len(self.cache) >= self.max_entries:
            self._evict_oldest()
        
        # Store result
        self.cache[cache_key] = {
            'result': result,
            'timestamp': time.time(),
            'hits': 0,
            'analysis_type': options.get('analysisType', 'unknown')
        }
        
        logger.info(f"Cache SET: {cache_key[:16]}... (type: {options.get('analysisType')})")
    
    def _evict_oldest(self) -> None:
        """Evict oldest cache entry to make room for new one"""
        if not self.cache:
            return
        
        # Find oldest entry
        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
        
        logger.debug(f"Cache EVICT: {oldest_key[:16]}... (age: {int(time.time() - self.cache[oldest_key]['timestamp'])}s)")
        del self.cache[oldest_key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        count = len(self.cache)
        self.cache.clear()
        logger.info(f"Cache CLEARED: {count} entries removed")
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries
        
        Returns:
            Number of entries removed
        """
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time - entry['timestamp'] > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.info(f"Cache CLEANUP: {len(expired_keys)} expired entries removed")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            dict: Cache statistics including size, hit rate, etc.
        """
        total_hits = sum(entry['hits'] for entry in self.cache.values())
        
        return {
            'entries': len(self.cache),
            'max_entries': self.max_entries,
            'total_hits': total_hits,
            'ttl_seconds': self.ttl_seconds,
            'oldest_entry_age': int(time.time() - min(
                (entry['timestamp'] for entry in self.cache.values()),
                default=time.time()
            )) if self.cache else 0
        }
    
    def invalidate_by_type(self, analysis_type: str) -> int:
        """
        Invalidate all cache entries of a specific analysis type
        
        Args:
            analysis_type: Type of analysis to invalidate
            
        Returns:
            Number of entries invalidated
        """
        keys_to_remove = [
            key for key, entry in self.cache.items()
            if entry['analysis_type'] == analysis_type
        ]
        
        for key in keys_to_remove:
            del self.cache[key]
        
        if keys_to_remove:
            logger.info(f"Cache INVALIDATE: {len(keys_to_remove)} {analysis_type} entries removed")
        
        return len(keys_to_remove)


# Global cache instance
analysis_cache = AnalysisCache(ttl_seconds=3600, max_entries=100)


# Convenience functions
def get_cached_result(file_content: bytes, options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get cached analysis result"""
    return analysis_cache.get(file_content, options)


def cache_result(file_content: bytes, options: Dict[str, Any], result: Dict[str, Any]) -> None:
    """Cache analysis result"""
    analysis_cache.set(file_content, options, result)


def clear_cache() -> None:
    """Clear all cached results"""
    analysis_cache.clear()


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    return analysis_cache.get_stats()


# Example usage
if __name__ == '__main__':
    # Test cache
    cache = AnalysisCache(ttl_seconds=10, max_entries=5)
    
    # Simulate file content and options
    file1 = b"test,data,1\n2,3,4"
    options1 = {"analysisType": "descriptive"}
    result1 = {"test": "result1"}
    
    # Set cache
    cache.set(file1, options1, result1)
    
    # Get cache (should hit)
    cached = cache.get(file1, options1)
    print(f"Cached result: {cached}")
    
    # Different options (should miss)
    options2 = {"analysisType": "regression"}
    cached2 = cache.get(file1, options2)
    print(f"Cached result 2: {cached2}")
    
    # Stats
    print(f"Cache stats: {cache.get_stats()}")
