from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4
import jwt

from app.config import security_settings

APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR.joinpath("templates")

def generate_token(data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    return jwt.encode(
            payload={
                **data,
                "jti": str(uuid4()),
                "exp": datetime.now(timezone.utc) + expiry
            },  
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET_KEY
        )

def decode_token(token: str):
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None


