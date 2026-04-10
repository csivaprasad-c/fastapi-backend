from typing import Any

from fastapi import APIRouter, Request, status, HTTPException, Query
from uuid import UUID

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies import CurrentDeliveryDep, CurrentSellerDep, DeliveryPartnerServiceDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentPage, ShipmentPatch, ShipmentRead, ShipmentUpdate
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix="/shipment", tags=["Shipment"])

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
async def get_shipment(id: UUID, service: ShipmentServiceDep, _: CurrentSellerDep,):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return shipment


@router.get("/{shipment_id}")
async def get_shipment_by_id(shipment_id: UUID, service: ShipmentServiceDep, _: CurrentSellerDep,):
    shipment = await service.get(shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return shipment


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ShipmentRead)
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
    partner: CurrentDeliveryDep
):

    updated_shipment = await service.update(shipment_id, shipment_update, partner)

    if updated_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

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

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead.model_validate(shipment_update)


@router.delete("/{shipment_id}")
async def delete_shipment(shipment_id: UUID, service: ShipmentServiceDep, _: CurrentSellerDep,) -> dict[str, Any]:
    result = await service.delete(shipment_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return result


@router.get("/{shipment_id}/cancel", response_model=ShipmentRead)
async def cancel_shipment(
    shipment_id: UUID,
    seller: CurrentSellerDep,
    service: ShipmentServiceDep
):
    return await service.cancel(shipment_id, seller)

@router.get("/track/{shipment_id}")
async def get_tracking(request: Request, shipment_id: UUID, service: ShipmentServiceDep):
    shipment = await service.get(shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    context = shipment.model_dump()
    context["partner"] = shipment.delivery_partner.name
    context["status"] = shipment.status
    context["timeline"] = shipment.timeline

    print(context)

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context
    )