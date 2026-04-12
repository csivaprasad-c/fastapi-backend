from datetime import datetime, timedelta, timezone
from json import dumps, JSONDecoder, JSONDecodeError
from pathlib import Path
from typing import Optional, Any, Mapping
from uuid import uuid4
from itsdangerous import BadSignature, SignatureExpired, URLSafeSerializer
import jwt

from app.config import security_settings

_serializer = URLSafeSerializer(security_settings.JWT_SECRET_KEY)

APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR.joinpath("templates")


def generate_token(data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    return jwt.encode(
        payload={
            **data,
            "jti": str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY,
    )


def decode_token(token: str):
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None


def generate_url_safe_token(data: dict, salt: Optional[str] = None) -> str:
    return _serializer.dumps(data, salt=salt)


def decode_url_safe_token(
    token: str, salt: Optional[str] = None, expiry: timedelta | None = None
) -> dict | None:
    try:
        return _serializer.loads(
            token, salt=salt, max_age=expiry.total_seconds() if expiry else None
        )
    except (BadSignature, SignatureExpired):
        return None


def print_label(data: Any, title: str | None = None):
    from rich import print
    from rich.panel import Panel

    try:
        data = dumps(data, indent=4) if isinstance(data, (dict, Mapping)) else data
    except JSONDecodeError:
        pass

    print()
    print(Panel(data, title=title), end="\n\n")
