from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme_seller = OAuth2PasswordBearer(
    tokenUrl="/sellers/token", scheme_name="Seller"
)
oauth2_scheme_partner = OAuth2PasswordBearer(
    tokenUrl="/partners/token", scheme_name="Delivery Partner"
)


class TokenData(BaseModel):
    access_token: str
    token_type: str


# class AccessTokenBearer(HTTPBearer):
#     async def __call__(self, request):
#         auth_credentials = await super().__call__(request)
#         token = auth_credentials.credentials
#
#         token_data = decode_token(token)
#
#         if token_data is None:
#             raise HTTPException(
#                 status_code=401,
#                 detail="Invalid authentication credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#
#         return token_data
#
# access_token_bearer = AccessTokenBearer()
#
# Annotated[dict, Depends(access_token_bearer)]
