import redis.asyncio as redis
from app.core.config import settings

# Khởi tạo connection pool cho Redis
redis_client = redis.from_url(
    settings.REDIS_URL, 
    decode_responses=True,
    encoding="utf-8"
)