import json

from redis.asyncio import Redis
from typing import Any, Optional

class CacheManager():
    def __init__(self):
        self.client = Redis(decode_responses=True)
        self.metrics = {
            "hits": 0,
            "misses": 0,
            "invalidations": 0
        }

    def get_ttl_for_category(self, category_type: str) -> int:
        ttl_map = {
            "sale": 120,
            "popular": 300, 
            "regular": 900
        }
        return ttl_map.get(category_type, 300)
    
    def get_ttl_for_endpoint(self, endpoint: str) -> int:
        ttl_map = {
            "sales_summary": 180,
            "inventory_alerts": 60,
        }
        return ttl_map.get(endpoint, 300)
    
    def generate_key(self, endpoint: str, **params) -> str:
        if endpoint == "categories_list":
            return "categories:list"
        elif endpoint == "category_detail":
            return f"categories:detail:{params['category_id']}"
        elif endpoint == "sales_summary":
            return "sales:summary"
        elif endpoint == "inventory_alerts":
            return "inventory:alerts"
        else:
            return f"cache:{endpoint}:{params}"


    async def get(self, key: str) -> Optional[Any]:
        try:
            data = await self.client.get(key)
            if data:
                self.metrics["hits"] += 1
                return json.loads(data)
            else:
                self.metrics["misses"] += 1
                return None
        except:
            return None
    
    async def set(self, key: str, data: Any, ttl: int) -> bool:
        try:
            serialized_data = json.dumps(data, default=str)
            await self.client.set(key, serialized_data, ex=ttl)
            return True
        except:
            return False
    
    async def invalidate_key(self, key: str, reason: str = "") -> bool:
        try:
            result = await self.client.delete(key)
            if result:
                self.metrics['invalidations'] += 1
            return bool(result)
        except Exception as e:
            return False
    
    async def get_metrics(self) -> dict:
        total = self.metrics['hits'] + self.metrics['misses']
        return {
            'hits': self.metrics['hits'],
            'misses': self.metrics['misses'], 
            'invalidations': self.metrics['invalidations'],
            'hit_ratio': self.metrics['hits'] / total if total > 0 else 0
        }
    
    async def close(self):
        await self.client.aclose()