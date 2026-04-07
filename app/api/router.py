from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, status, HTTPException

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep
from app.api.schemas.schemas import ShipmentCreate, ShipmentPatch, ShipmentRead, ShipmentUpdate
from app.services.shipment import ShipmentService

router = APIRouter()

@router.get("/shipment", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(id: int, session: SessionDep):
    shipment = await ShipmentService(session).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return shipment

@router.get("/shipment/{shipment_id}")
async def get_shipment_by_id(shipment_id: int, session: SessionDep):
    shipment = await ShipmentService(session).get(shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Shipment not found"
        )
    return shipment

@router.post("/shipment", status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
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
    
    new_shipment = await ShipmentService(session).add(shipment)

    return {"id": new_shipment.id}

@router.put("/shipment/{shipment_id}", response_model=ShipmentRead)
async def update_shipment(shipment_id: int, shipment: ShipmentUpdate, session: SessionDep):
    shipment_update = await ShipmentService(session).update(shipment_id, shipment)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead(
        **shipment_update.model_dump()
    )

@router.patch("/shipment/{shipment_id}")
async def patch_shipment(shipment_id: int, data: ShipmentPatch, session: SessionDep):  
    shipment_update = await ShipmentService(session).patch(shipment_id, data)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead(
        **shipment_update.model_dump()
    )

@router.delete("/shipment/{shipment_id}")
async def delete_shipment(shipment_id: int, session: SessionDep) -> dict[str, Any]:
    result = await ShipmentService(session).delete(shipment_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
   
    return result
