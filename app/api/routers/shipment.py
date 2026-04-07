from typing import Any

from fastapi import APIRouter, status, HTTPException, Query

from app.api.dependencies import CurrentUserDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentPage, ShipmentPatch, ShipmentRead, ShipmentUpdate

router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/all", status_code=status.HTTP_200_OK, response_model=ShipmentPage)
async def get_all_shipments(
    service: ShipmentServiceDep,
    _: CurrentUserDep,
    cursor: int | None = Query(default=None, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    shipments, next_cursor = await service.get_all(cursor=cursor, limit=limit)
    return ShipmentPage(items=[ShipmentRead(**s.model_dump()) for s in shipments], next_cursor=next_cursor)


@router.get("", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(id: int, service: ShipmentServiceDep, _: CurrentUserDep,):
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return shipment


@router.get("/{shipment_id}")
async def get_shipment_by_id(shipment_id: int, service: ShipmentServiceDep, _: CurrentUserDep,):
    shipment = await service.get(shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return shipment


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_shipment(
    seller: CurrentUserDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
    _: CurrentUserDep,
) -> dict[str, Any]:
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

    new_shipment = await service.add(shipment)

    return {"id": new_shipment.id}


@router.put("/{shipment_id}", response_model=ShipmentRead)
async def update_shipment(shipment_id: int, shipment: ShipmentUpdate, service: ShipmentServiceDep, _: CurrentUserDep,):
    shipment_update = await service.update(shipment_id, shipment)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead(
        **shipment_update.model_dump()
    )


@router.patch("/{shipment_id}")
async def patch_shipment(shipment_id: int, data: ShipmentPatch, service: ShipmentServiceDep, _ : CurrentUserDep,):
    shipment_update = await service.patch(shipment_id, data)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead(
        **shipment_update.model_dump()
    )


@router.delete("/{shipment_id}")
async def delete_shipment(shipment_id: int, service: ShipmentServiceDep, _ : CurrentUserDep,) -> dict[str, Any]:
    result = await service.delete(shipment_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return result
