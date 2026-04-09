from typing import Optional

from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService


class ShipmentEventsService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)

    async def add(
        self,
        shipment: Shipment,
        location: Optional[int] = None,
        status: Optional[ShipmentStatus] = None,
        description: Optional[str] = None
    ) -> ShipmentEvent:
        if not status or not location:
            last_event = await self.get_latest_event(shipment)
            location = location if location else last_event.location
            status = status if status else last_event.status

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(
                status, location),
            shipment_id=shipment.id
        )
        return await self._create(new_event)

    async def get_latest_event(self, shipment: Shipment) -> ShipmentEvent | None:
        if not shipment.timeline:
            return None
        return sorted(shipment.timeline, key=lambda item: item.created_at)[-1]

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.cancelled:
                return "cancelled"
            case _:
                return f"scanned at ${location}"
