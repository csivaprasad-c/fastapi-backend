from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas.seller import CreateSeller, ReadSeller
from app.api.dependencies import SellerServiceDep, SessionDep
from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.utils import decode_token

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSeller)
async def register_seller(seller: CreateSeller, service: SellerServiceDep):
    print(seller)
    return await service.add(seller)


@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()], 
    service: SellerServiceDep
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}

# @router.get("/dashboard")
# async def get_dashboard(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     session: SessionDep
# ):
#     data = decode_token(token)

#     if data is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )
    
#     seller = await session.get(Seller, data["user"]["id"])

#     if seller is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Seller not found"
#         )
    
#     return {"message": f"Welcome to your dashboard, {seller.name}!"}
