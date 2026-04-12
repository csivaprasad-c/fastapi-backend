from typing import Any, Annotated

from fastapi import APIRouter, Request, status, HTTPException, Query, Form
from uuid import UUID

from fastapi.templating import Jinja2Templates

from app.api.dependencies import (
    CurrentDeliveryDep,
    CurrentSellerDep,
    DeliveryPartnerServiceDep,
    ShipmentServiceDep,
    SessionDep,
)
from app.api.schemas.shipment import (
    ShipmentCreate,
    ShipmentPage,
    ShipmentPatch,
    ShipmentRead,
    ShipmentUpdate,
    ShipmentReview,
)
from app.api.tag import APITag
from app.config import app_settings
from app.core.exceptions import EntityNotFoundError
from app.database.models import TagName
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix="/shipment", tags=[APITag.SHIPMENT])

templates = Jinja2Templates(TEMPLATE_DIR)


# @router.get("/all", status_code=status.HTTP_200_OK, response_model=ShipmentPage)
# async def get_all_shipments(
#     service: ShipmentServiceDep,
#     _: CurrentSellerDep,
#     cursor: UUID | None = Query(default=None, ge=1),
#     limit: int = Query(default=10, ge=1, le=100)
# ):
#     shipments, next_cursor = await service.get_all(cursor=cursor, limit=limit)
#     return ShipmentPage(items=[ShipmentRead(**s.model_dump()) for s in shipments], next_cursor=next_cursor)


@router.get("", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(
    id: UUID,
    service: ShipmentServiceDep,
    _: CurrentSellerDep,
):
    return await service.get(id)


@router.get("/track", include_in_schema=False)
async def get_tracking(request: Request, id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(id)

    context = shipment.model_dump()
    context["partner"] = shipment.delivery_partner.name
    context["status"] = shipment.status
    context["timeline"] = shipment.timeline

    return templates.TemplateResponse(
        request=request, name="track.html", context=context
    )


@router.get("/review")
async def get_review_page(request: Request, token: str):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"
        },
    )


@router.post("/review")
async def submit_review(
    token: str,
    rating: Annotated[
        int,
        Form(le=5, ge=1),
    ],
    comment: Annotated[str | None, Form()],
    service: ShipmentServiceDep,
):
    await service.rate(token, rating, comment)
    return {"detail": "Review submitted successfully"}


@router.get("/tagged", response_model=list[ShipmentRead])
async def get_tagged_shipments(tag_name: TagName, session: SessionDep):
    tag = await tag_name.tag(session)
    if tag is None:
        raise EntityNotFoundError()
    return tag.shipments


@router.get("/{shipment_id}", response_model=ShipmentRead)
async def get_shipment_by_id(
    shipment_id: UUID,
    service: ShipmentServiceDep,
    _: CurrentSellerDep,
):
    return await service.get(shipment_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ShipmentRead,
    name="Create Shipment",
    description="Submit and Create a new **shipment**",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Shipment created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "12345678-abcd-90ab-cdef-1234567890ab",
                        "status": "placed",
                    }
                }
            },
        },
        status.HTTP_406_NOT_ACCEPTABLE: {
            "description": "Delivery partner not available"
        },
    },
)
async def create_shipment(
    seller: CurrentSellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
) -> ShipmentRead:
    # weight = data.get("weight")
    # content = data.get("content")

    # if weight is None or not isinstance(weight, (int, float)):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Weight must be provided and must be a number"
    #     )

    # if weight > 25:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #         detail="Shipment weight exceeds the limit of 25 kg"
    #     )

    new_shipment = await service.add(shipment, seller)

    return ShipmentRead.model_validate(new_shipment)


@router.put("/{shipment_id}", response_model=ShipmentRead)
async def update_shipment(
    shipment_id: UUID,
    shipment_update: ShipmentUpdate,
    service: ShipmentServiceDep,
    partner: CurrentDeliveryDep,
):
    updated_shipment = await service.update(shipment_id, shipment_update, partner)

    return ShipmentRead.model_validate(updated_shipment)


@router.patch("/{shipment_id}")
async def patch_shipment(
    shipment_id: UUID,
    data: ShipmentPatch,
    partner: DeliveryPartnerServiceDep,
    service: ShipmentServiceDep,
    _: CurrentSellerDep,
):
    shipment_update = await service.patch(shipment_id, data)

    return ShipmentRead.model_validate(shipment_update)


@router.delete("/{shipment_id}")
async def delete_shipment(
    shipment_id: UUID,
    service: ShipmentServiceDep,
    _: CurrentSellerDep,
) -> dict[str, Any]:
    return await service.delete(shipment_id)


@router.get("/{shipment_id}/cancel", response_model=ShipmentRead)
async def cancel_shipment(
    shipment_id: UUID, seller: CurrentSellerDep, service: ShipmentServiceDep
):
    return await service.cancel(shipment_id, seller)


@router.get("/{shipment_id}/tag", response_model=ShipmentRead)
async def add_tag_to_shipment(
    shipment_id: UUID, tag_name: TagName, service: ShipmentServiceDep
):
    return await service.add_tag(shipment_id, tag_name)


@router.delete("/{shipment_id}/tag", response_model=ShipmentRead)
async def remove_tag_from_shipment(
    shipment_id: UUID, tag_name: TagName, service: ShipmentServiceDep
):
    return await service.remove_tag(shipment_id, tag_name)
