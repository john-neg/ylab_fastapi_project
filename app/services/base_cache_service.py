import json
from dataclasses import dataclass
from typing import Any

from aioredis import Redis
from fastapi.encoders import jsonable_encoder

from app.core.config import settings


@dataclass
class BaseCacheService:
    """Base service for a Redis-based cache."""

    cache: Redis

    async def set(self, key: str, value: Any):
        """Sets an object to the cache."""
        value = json.dumps(jsonable_encoder(value))
        await self.cache.set(key, value, ex=settings.REDIS_CACHE_TIME)

    async def get(self, key: str):
        """Gets an object from the cache."""
        data = await self.cache.get(key)
        return json.loads(data) if data else None

    async def delete(self, key: str):
        """Removes an object from the cache."""
        return await self.cache.delete(key)
