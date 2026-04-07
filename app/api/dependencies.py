from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import oauth2_scheme
from app.database.models import Seller
from app.database.session import get_session
from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.utils import decode_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)

def get_seller_service(session: SessionDep) -> SellerService:
    return SellerService(session)

# Access token dependency
def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return data

# Logged in user dependency
async def get_current_user(
        token_data: Annotated[dict, Depends(get_access_token)],
        session: SessionDep
):
    return await session.get(Seller, token_data["user"]["id"])
    

ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
CurrentUserDep = Annotated[Seller, Depends(get_current_user)]

