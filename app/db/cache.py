import aioredis
from aioredis import Redis

from app.core.config import settings


async def get_cache() -> Redis:
    """
    The get_cache function creates a Redis connection pool using the REDIS_URL
    from the settings file.
    """
    redis = aioredis.from_url(
        settings.REDIS_URL,
        max_connections=10,
        encoding='utf8',
        decode_responses=True,
    )
    return redis
