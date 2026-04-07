from redis.asyncio import Redis
from app.config import db_settings

_token_blacklist = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=db_settings.REDIS_DB
)

async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")

async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.get(jti) is not None