from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette.templating import Jinja2Templates

import logging

from app.api.schemas.seller import CreateSeller, ReadSeller
from app.api.dependencies import SellerServiceDep, SessionDep, get_seller_access_token
from app.api.tag import APITag
from app.config import app_settings
from app.core.exceptions import InvalidTokenError, EntityNotFoundError
from app.core.security import TokenData
from app.database.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix="/sellers", tags=[APITag.SELLER])

logger = logging.getLogger(__name__)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSeller)
async def register_seller(seller: CreateSeller, service: SellerServiceDep):
    print(seller)
    return await service.add(seller)


@router.post("/token", response_model=TokenData)
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "jwt"}


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_seller(
    token: Annotated[dict, Depends(get_seller_access_token)],
):
    await add_jti_to_blacklist(token["jti"])
    return {"detail": "Successfully logged out"}


@router.get("/verify")
async def verify_seller_email(token: str, service: SellerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}


@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, route_prefix="sellers")
    return {"detail": "Check your email for password reset link"}


@router.post("/reset_password")
async def reset_password(
    request: Request,
    token: str,
    password: Annotated[str, Form()],
    service: SellerServiceDep,
):
    password_reset = False
    try:
        await service.reset_password(token, password)
        password_reset = True
    except InvalidTokenError | EntityNotFoundError as e:
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
async def reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(directory=TEMPLATE_DIR)
    return templates.TemplateResponse(
        request=request,
        name="password/reset.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )


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
