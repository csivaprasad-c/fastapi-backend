from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc

from app.api.schemas.shipment import ShipmentCreate, ShipmentPatch, ShipmentUpdate
from app.database.models import Seller, Shipment, ShipmentStatus


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: UUID) -> Shipment | None:
        return await self.session.get(Shipment, id)

    async def get_all(self, cursor: UUID | None = None, limit: int = 10) -> tuple[list[Shipment], UUID | None]:
        stmt = select(Shipment).order_by(Shipment.id).limit(limit + 1)
        if cursor is not None:
            stmt = stmt.where(Shipment.id > cursor)
        result = await self.session.execute(stmt)
        shipments = list(result.scalars().all())

        next_cursor = None
        if len(shipments) > limit:
            next_cursor = shipments[limit - 1].id
            shipments = shipments[:limit]

        return shipments, next_cursor

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed.value,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id
        )
    
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update(self, id: UUID, shipment_update: ShipmentUpdate) -> Shipment | None:
        update = shipment_update.model_dump(exclude_unset=True)
    
        shipment_to_update = await self.get(id)

        if shipment_to_update is None:
            return None
        
        shipment_to_update.sqlmodel_update(update)
        self.session.add(shipment_to_update)
        await self.session.commit()
        await self.session.refresh(shipment_to_update)

        return shipment_to_update

    async def patch(self, id: UUID, shipment_patch: ShipmentPatch) -> Shipment | None:
        shipment_update = await self.get(id)
    
        if shipment_update is None:
            return None

        updated_shipment = {
            "weight": shipment_patch.weight or shipment_update.weight,
            "content": shipment_patch.content or shipment_update.content,
            "status": shipment_patch.status.value if shipment_patch.status else shipment_update.status,
            "destination": shipment_patch.destination or shipment_update.destination,
            "estimated_delivery": shipment_update.estimated_delivery
        }

        shipment_update.sqlmodel_update(updated_shipment)
        self.session.add(shipment_update)
        await self.session.commit()
        await self.session.refresh(shipment_update)

        return shipment_update

    async def delete(self, id: UUID) -> dict[str, Any] | None:
        existing_shipment = await self.get(id)
        if existing_shipment is None:
            return None
        await self.session.delete(existing_shipment)
        await self.session.commit()
        return {"message": "Shipment deleted successfully"}