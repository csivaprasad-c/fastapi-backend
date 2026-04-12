from datetime import timedelta
from uuid import UUID

import bcrypt

from fastapi import BackgroundTasks, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import app_settings
from app.core.exceptions import (
    BadPasswordError,
    InvalidTokenError,
    EntityNotFoundError,
    ClientNotAuthorizedError,
    ClientNotVerifiedError,
    BadCredentialsError,
)
from app.database.models import User
from app.services.base import BaseService
from app.utils import (
    generate_token,
    generate_url_safe_token,
    decode_url_safe_token,
)
from app.workers.tasks import send_sms, send_email_with_template


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


class UserService(BaseService):
    def __init__(
        self,
        model: type[User],
        session: AsyncSession,
    ):
        super().__init__(model, session)

    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _add(self, data: dict, route_prefix: str):

        existing_user = await self._get_by_email(data["email"])
        if existing_user:
            raise BadCredentialsError()

        try:
            new_user = self.model(**data, password_hash=hash_password(data["password"]))
        except ValueError:
            raise BadPasswordError()

        user = await self._create(new_user)
        token = generate_url_safe_token({"email": user.email, "id": str(user.id)})

        send_email_with_template.delay(
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
            raise ClientNotAuthorizedError()

        if not user.email_verified:
            raise ClientNotVerifiedError()

        token = generate_token({"user": {"name": user.name, "id": str(user.id)}})

        return token

    async def verify_email(self, token: str):
        token_data = decode_url_safe_token(token)

        if token_data is None:
            raise InvalidTokenError()

        user = await self._get(UUID(token_data["id"]))
        if not user:
            raise EntityNotFoundError()

        user.email_verified = True
        await self._update(user)

    async def send_password_reset_link(self, email: EmailStr, route_prefix: str):
        user = await self._get_by_email(email)
        if not user:
            raise EntityNotFoundError()

        token = generate_url_safe_token(
            {"id": str(user.id), "email": user.email}, salt="password-reset"
        )

        send_email_with_template.delay(
            recipients=[user.email],
            subject="FastShip Account Password Reset",
            template_name="mail_password_reset.html",
            context={
                "username": user.name,
                "reset_url": f"http://{app_settings.APP_DOMAIN}/{route_prefix}/reset_password_form?token={token}",
            },
        )

    async def reset_password(self, token: str, password: str):
        token_data = decode_url_safe_token(
            token, salt="password-reset", expiry=timedelta(days=1)
        )
        if token_data is None:
            raise InvalidTokenError()

        user = await self._get(UUID(token_data["id"]))
        if not user:
            raise EntityNotFoundError()

        user.password_hash = hash_password(password)
        await self._update(user)
