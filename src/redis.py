import redis.asyncio as redis

from src.settings import RedisSettings as r

# Создаем клиент Redis
async_redis = redis.Redis(
    host=r.HOST,
    port=r.PORT,
    db=r.DB,
    decode_responses=True,  # строки, не байты
)
