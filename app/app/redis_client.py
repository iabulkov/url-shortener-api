import redis
import os
import json
from typing import Optional, Any
from datetime import timedelta

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class RedisCache:
    @staticmethod
    def get(key: str) -> Optional[Any]:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 3600):
        redis_client.setex(key, timedelta(seconds=expire), json.dumps(value, default=str))
    
    @staticmethod
    def delete(key: str):
        redis_client.delete(key)
    
    @staticmethod
    def delete_pattern(pattern: str):
        for key in redis_client.scan_iter(pattern):
            redis_client.delete(key)
    
    @staticmethod
    def increment(key: str, amount: int = 1):
        return redis_client.incrby(key, amount)
    
    @staticmethod
    def set_expire(key: str, expire: int):
        redis_client.expire(key, expire)

CACHE_KEYS = {
    "link": "link:{short_code}",
    "stats": "stats:{short_code}",
    "search": "search:{original_url}",
    "user_links": "user:{user_id}:links",
    "popular": "popular_links",
}