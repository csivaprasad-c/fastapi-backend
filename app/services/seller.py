from datetime import datetime, timedelta

import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.seller import CreateSeller
from app.config import security_settings
from app.database.models import Seller
from app.utils import generate_token, decode_token


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, seller: CreateSeller):
        new_seller = Seller(
            **seller.model_dump(exclude={"password"}),
            password_hash=hash_password(seller.password)
        )
        print(new_seller)
        self.session.add(new_seller)
        await self.session.commit()
        await self.session.refresh(new_seller)

        return new_seller
    
    async def token(self, email, password) -> str:
        result = await self.session.execute(
            select(Seller).where(Seller.email == email)
        )
        seller = result.scalar_one_or_none()
        if not seller or not verify_password(password, seller.password_hash):
            raise ValueError("Invalid email or password")
        
        token = generate_token({
            "user": {
                "name": seller.name,
                "id": str(seller.id)
            }
        })

        return token