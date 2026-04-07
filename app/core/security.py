from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from app.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sellers/token")

class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):
        auth_credentials = await super().__call__(request)
        token = auth_credentials.credentials

        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token_data
    
access_token_bearer = AccessTokenBearer()

Annotated[dict, Depends(access_token_bearer)]

