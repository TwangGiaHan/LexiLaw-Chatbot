import json
from time import time
from typing import List, Dict
import redis.asyncio as redis
from app.core.redis import redis_client

def get_redis():
    return redis_client

async def create_chat(rdb: redis.Redis, chat_id: str, created_at: int):
    await rdb.hset(f"chat:{chat_id}", "created", created_at)

async def chat_exists(rdb: redis.Redis, chat_id: str) -> bool:
    return await rdb.exists(f"chat:{chat_id}")

async def add_chat_messages(rdb: redis.Redis, chat_id: str, messages: List[Dict]):
    key = f"chat:{chat_id}:messages"
    for msg in messages:
        await rdb.rpush(key, json.dumps(msg))
    await rdb.expire(f"chat:{chat_id}", 86400)
    await rdb.expire(key, 86400)

async def get_chat_messages(rdb: redis.Redis, chat_id: str, last_n: int = 10) -> List[Dict]:
    key = f"chat:{chat_id}:messages"
    raw_messages = await rdb.lrange(key, -last_n, -1)
    return [json.loads(m) for m in raw_messages]


