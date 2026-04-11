from uuid import UUID

from redis.asyncio import Redis
from app.config import db_settings

_token_blacklist = Redis(
    host=db_settings.REDIS_HOST, port=db_settings.REDIS_PORT, db=db_settings.REDIS_DB
)

_shipment_verification_codes = Redis(
    host=db_settings.REDIS_HOST,
    port=db_settings.REDIS_PORT,
    db=db_settings.REDIS_DB + 1,
    decode_responses=True,
)


async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.get(jti) is not None


async def add_shipment_verification_code(shipment_id: UUID, code: int) -> str:
    return await _shipment_verification_codes.set(str(shipment_id), code)


async def get_shipment_verification_code(shipment_id: UUID) -> str | None:
    return await _shipment_verification_codes.get(str(shipment_id))
