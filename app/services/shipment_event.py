from re import sub
from typing import Optional

from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService
from app.services.notification import NotificationService


class ShipmentEventsService(BaseService):
    def __init__(self, session, tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)

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
        await self._notify(shipment=shipment, status=status)
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
    
    async def _notify(self, shipment: Shipment, status: ShipmentStatus):

        if status == ShipmentStatus.in_transit:
            return

        subject: str
        context = {}
        template_name: str

        match status:
            case ShipmentStatus.placed:
                subject="Your order is shipped 🚚"
                context["seller"]=shipment.seller.name
                context["partner"]=shipment.delivery_partner.name
                template_name=f"mail_{status.value}.html"
            case ShipmentStatus.out_for_delivery:
                subject="Your order is arriving 🛵"
                template_name=f"mail_{status.value}.html"
            case ShipmentStatus.delivered:
                subject="Your order is delivered ✅"
                template_name=f"mail_{status.value}.html"
            case ShipmentStatus.cancelled:
                subject="Your order is cancelled ❌"
                template_name=f"mail_{status.value}.html"
        
        await self.notification_service.send_email_with_template(
            recipients=[shipment.client_contact_email],
            subject=subject,
            context=context,
            template_name=template_name
        )