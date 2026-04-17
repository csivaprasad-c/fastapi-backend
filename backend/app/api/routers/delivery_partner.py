from math import ceil
from typing import Annotated, Literal

from sqlalchemy import select
from sqlmodel import asc, col, desc

from app.config import app_settings
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.api.schemas.deivery_partner import (
    CreateDeliveryPartner,
    DeliveryPartnerShipment,
    PaginationParams,
    ReadDeliveryPartner,
    UpdateDeliveryPartner,
    get_pagination_params,
)
from app.api.dependencies import (
    DeliveryPartnerServiceDep,
    SellerServiceDep,
    SessionDep,
    get_partner_access_token,
    CurrentDeliveryDep,
)
from app.api.tag import APITag
from app.core.exceptions import (
    EntityNotFoundError,
    InvalidTokenError,
    NothingToUpdateError,
)
from app.core.security import TokenData
from app.database.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_DIR
from app.database.models import Shipment

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


@router.get("/me", response_model=ReadDeliveryPartner)
async def get_delivery_partner_profile(partner: CurrentDeliveryDep):
    return partner


@router.get("/shipments", response_model=DeliveryPartnerShipment)
async def get_partner_shipments(
    partner: CurrentDeliveryDep,
    session: SessionDep,
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
):
    result = await session.scalars(
        select(Shipment)
        .where(col(Shipment.delivery_partner_id) == partner.id)
        .limit(pagination.pageSize)
        .offset((pagination.page - 1) * pagination.pageSize)
        .order_by(
            asc(Shipment.created_at)
            if pagination.order == "asc"
            else desc(Shipment.created_at)
        )
    )
    return {
        "shipments": result.all(),
        "total_shipments": len(partner.shipments),
        "page": pagination.page,
        "total_pages": ceil(len(partner.shipments) / pagination.pageSize),
    }


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
async def verify_partner_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}


@router.get("/forgot_password")
async def partner_forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, route_prefix="sellers")
    return {"detail": "Check your email for password reset link"}


@router.post("/reset_password")
async def partner_reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: SellerServiceDep,
):
    password_reset = False
    try:
        await service.reset_password(token, password)
        password_reset = True
    except (InvalidTokenError, EntityNotFoundError) as e:
        logger.error(e)

    templates = Jinja2Templates(directory=TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name=(
            "password/reset_success.html"
            if password_reset
            else "password/reset_failed.html"
        ),
    )


@router.get("/reset_password_form")
async def partner_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(directory=TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )
