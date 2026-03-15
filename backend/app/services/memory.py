import json
import hashlib
from typing import List, Dict, Any, Optional
from app.core.redis import redis_client

class MemoryService:
    def __init__(self, ttl: int = 3600): 
        self.ttl = ttl

    def _get_cache_key(self, query: str) -> str:
        return f"cache:query:{hashlib.md5(query.encode()).hexdigest()}"

    async def get_cached_result(self, query: str) -> Optional[List[Dict[str, Any]]]:
        key = self._get_cache_key(query)
        cached = await redis_client.get(key)
        if cached:
            return json.loads(cached)
        return None

    async def set_cached_result(self, query: str, result: List[Dict[str, Any]]):
        key = self._get_cache_key(query)
        await redis_client.setex(key, self.ttl, json.dumps(result))

    async def invalidate_cache(self, query: str):
        key = self._get_cache_key(query)
        await redis_client.delete(key)

memory_service = MemoryService()