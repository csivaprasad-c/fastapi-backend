from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, status, HTTPException

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep
from app.api.schemas.schemas import ShipmentCreate, ShipmentPatch, ShipmentRead, ShipmentUpdate

router = APIRouter()

@router.get("/shipment", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
async def get_shipment(id: int, session: SessionDep):
    shipment = await session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return shipment

@router.get("/shipment/{shipment_id}")
async def get_shipment_by_id(shipment_id: int, session: SessionDep):
    shipment = await session.get(Shipment, shipment_id)

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
    
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed.value,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )
    
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)

    return {"id": new_shipment.id}

@router.put("/shipment/{shipment_id}", response_model=ShipmentRead)
async def update_shipment(shipment_id: int, shipment: ShipmentUpdate, session: SessionDep):
    update = shipment.model_dump()
    
    shipment_update = await session.get(Shipment, shipment_id)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    shipment_update.sqlmodel_update(update)
    session.add(shipment_update)
    await session.commit()
    await session.refresh(shipment_update)

    return ShipmentRead(
        **shipment_update.model_dump()
    )

@router.patch("/shipment/{shipment_id}")
async def patch_shipment(shipment_id: int, data: ShipmentPatch, session: SessionDep):  
    shipment_update = await session.get(Shipment, shipment_id)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    updated_shipment = {
        "weight": data.weight or shipment_update.weight,
        "content": data.content or shipment_update.content,
        "status": data.status.value if data.status else shipment_update.status,
        "destination": data.destination or shipment_update.destination,
        "estimated_delivery": shipment_update.estimated_delivery
    }

    shipment_update.sqlmodel_update(updated_shipment)
    session.add(shipment_update)
    await session.commit()
    await session.refresh(shipment_update)

    return ShipmentRead(
        **shipment_update.model_dump()
    )

@router.delete("/shipment/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(shipment_id: int, session: SessionDep) -> None:
    existing_shipment = await session.get(Shipment, shipment_id)
    if existing_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    await session.delete(existing_shipment)
    await session.commit()
    return 
