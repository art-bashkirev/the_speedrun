import json

from redis.asyncio import Redis
from typing import Any, Optional, List

class CacheManager():
    TTL_USER_DOCUMENTS = 5 * 60
    TTL_SHARED_DOCUMENTS = 2 * 60
    TTL_USER_DOCUMENT = 10 * 60
    TTL_PERMISSIONS = 15 * 60

    def __init__(self):
        self.client = Redis(decode_responses=True)

    def key_user_documents(self, user_id: int) -> str:
        return f"user:{user_id}:documents"

    def key_shared_documents(self) -> str:
        return "shared:documents"

    def key_user_document(self, user_id: int, doc_id: int) -> str:
        return f"user:{user_id}:document:{doc_id}"

    def key_document_permissions(self, doc_id: int) -> str:
        return f"document:{doc_id}:permissions"

    async def get(self, key: str) -> Optional[Any]:
        try:
            data = await self.client.get(key)
            if data:
                return json.loads(data)
            else:
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
    
    async def invalidate(self, keys: List[str]) -> List[str]:
        result = []
        for key in keys:
            deleted = await self.client.delete(key)
            if deleted:
                result.append(key)
        return result
    
    async def close(self):
        await self.client.aclose()