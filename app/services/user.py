import bcrypt

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import User
from app.services.base import BaseService
from app.utils import generate_token, decode_token

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

class UserService(BaseService):
    def __init__(self, model: type[User], session: AsyncSession):
        super().__init__(model, session)
    
    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
    
    async def _add(self, data: dict):
        new_user = self.model(
            **data,
            password_hash=hash_password(data["password"])
        )
        user = await self._create(new_user)
        return user
    
    async def _generate_token(self, email, password):
        user = await self._get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        token = generate_token({
            "user": {
                "name": user.name,
                "id": str(user.id)
            }
        })

        return token