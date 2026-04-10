from uuid import UUID

import bcrypt

from fastapi import BackgroundTasks, HTTPException, status
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import app_settings
from app.database.models import User
from app.services.base import BaseService
from app.services.notification import NotificationService
from app.utils import (
    generate_token,
    decode_token,
    generate_url_safe_token,
    decode_url_safe_token,
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


class UserService(BaseService):
    def __init__(
        self, model: type[User], session: AsyncSession, tasks: BackgroundTasks
    ):
        super().__init__(model, session)
        self.notification_service = NotificationService(tasks=tasks)

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _add(self, data: dict, route_prefix: str):

        existing_user = await self._get_by_email(data["email"])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        new_user = self.model(**data, password_hash=hash_password(data["password"]))
        user = await self._create(new_user)
        token = generate_url_safe_token({"email": user.email, "id": str(user.id)})

        await self.notification_service.send_email_with_template(
            recipients=[user.email],
            subject="Verify your account with FastShip",
            template_name="mail_email_verify.html",
            context={
                "username": user.name,
                "verification_url": f"http://{app_settings.APP_DOMAIN}/{route_prefix}/verify?token={token}",
            },
        )

        return user

    async def _generate_token(self, email, password):
        user = await self._get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_401, detail="Email not verified"
            )

        token = generate_token({"user": {"name": user.name, "id": str(user.id)}})

        return token

    async def verify_email(self, token: str):
        token_data = decode_url_safe_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )

        user = await self._get(UUID(token_data["id"]))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user.email_verified = True
        await self._update(user)
