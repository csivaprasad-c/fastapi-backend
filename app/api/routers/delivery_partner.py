from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas.deivery_partner import (
    CreateDeliveryPartner,
    ReadDeliveryPartner,
    UpdateDeliveryPartner,
)
from app.api.dependencies import (
    DeliveryPartnerServiceDep,
    SellerServiceDep,
    get_partner_access_token,
    CurrentDeliveryDep,
)
from app.api.tag import APITag
from app.core.exceptions import NothingToUpdateError
from app.core.security import TokenData
from app.database.redis import add_jti_to_blacklist

router = APIRouter(prefix="/partners", tags=[APITag.PARTNER])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=ReadDeliveryPartner
)
async def register_delivery_partner(
    delivery_partner: CreateDeliveryPartner, service: DeliveryPartnerServiceDep
):
    return await service.add(delivery_partner)


@router.post("/token", response_model=TokenData)
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "jwt"}


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_delivery_partner(
    token: Annotated[dict, Depends(get_partner_access_token)],
):
    await add_jti_to_blacklist(token["jti"])
    return {"detail": "Successfully logged out"}


@router.put("", response_model=ReadDeliveryPartner)
async def update_delivery_partner(
    partner_update: UpdateDeliveryPartner,
    partner: CurrentDeliveryDep,
    service: DeliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)
    if not update:
        raise NothingToUpdateError()

    return await service.update(partner.sqlmodel_update(update))


@router.get("/verify")
async def verify_seller_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}
