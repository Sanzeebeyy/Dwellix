import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

async def init_rate_limiter():
    redis_url = "redis://localhost:6379"

    redis_connection = redis.from_url(
        redis_url,
        encoding = "utf-8",
        decode_responses = True
    )

    await FastAPILimiter.init(redis_connection)

login_limit = RateLimiter(times=5,seconds=60)
apply_limit = RateLimiter(times=10, seconds=3600)
create_room_limit = RateLimiter(times=10, seconds=3600)