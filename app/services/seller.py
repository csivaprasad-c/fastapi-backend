from datetime import datetime, timedelta

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import CreateSeller
from app.config import security_settings
from app.database.models import Seller
from app.services.user import UserService
from app.utils import generate_token, decode_token


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


class SellerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(Seller, session)

    async def add(self, seller: CreateSeller):
        user = await self._add(seller.model_dump())
        return user
    
    async def token(self, email, password) -> str:
        token = await self._generate_token(email, password)
        return token