from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc

from app.api.schemas.shipment import (
    ShipmentCreate,
    ShipmentPatch,
    ShipmentUpdate,
    ShipmentReview,
)
from app.core.exceptions import EntityNotFoundError, ClientNotAuthorizedError, InvalidTokenError
from app.database.models import (
    DeliveryPartner,
    Seller,
    Shipment,
    ShipmentStatus,
    Review,
    TagName,
)
from app.database.redis import get_shipment_verification_code
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService
from app.services.shipment_event import ShipmentEventsService
from app.utils import decode_url_safe_token


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventsService,
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service

    async def get(self, id: UUID) -> Shipment:
        shipment = await self._get(id)
        if shipment is None:
            raise EntityNotFoundError()
        return shipment

    # async def get_all(self, cursor: UUID | None = None, limit: int = 10) -> tuple[list[Shipment], UUID | None]:
    #     stmt = select(Shipment).order_by(Shipment.id).limit(limit + 1)
    #     if cursor is not None:
    #         stmt = stmt.where(Shipment.id > cursor)
    #     result = await self.session.execute(stmt)
    #     shipments = list(result.scalars().all())

    #     next_cursor = None
    #     if len(shipments) > limit:
    #         next_cursor = shipments[limit - 1].id
    #         shipments = shipments[:limit]

    #     return shipments, next_cursor

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed.value,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._create(new_shipment)

        event = await self.event_service.add(
            shipment=new_shipment,
            location=seller.zip_code,
            status=ShipmentStatus.placed,
            description=f"assigned to {partner.name}",
        )

        shipment.timeline.append(event)

        return shipment

    async def update(
        self, id: UUID, shipment_update: ShipmentUpdate, partner: DeliveryPartner
    ) -> Shipment | None:

        shipment_to_update = await self.get(id)

        if shipment_to_update.delivery_partner_id != partner.id:
            raise ClientNotAuthorizedError()

        if shipment_update.status == ShipmentStatus.delivered:
            code = await get_shipment_verification_code(shipment_to_update.id)
            if code is None:
                raise ClientNotAuthorizedError()
            if int(code) != shipment_update.verification_code:
                raise ClientNotAuthorizedError()

        update = shipment_update.model_dump(
            exclude_none=True, exclude={"verification_code"}
        )

        if shipment_update.estimated_delivery:
            shipment_to_update.estimated_delivery = shipment_update.estimated_delivery

        if len(update) > 1 or not shipment_update.estimated_delivery:
            await self.event_service.add(shipment=shipment_to_update, **update)

        shipment_to_update.sqlmodel_update(update)

        shipment = await self._update(shipment_to_update)

        return shipment

    async def patch(self, id: UUID, shipment_patch: ShipmentPatch) -> Shipment:
        shipment_update = await self.get(id)

        updated_shipment = {
            "weight": shipment_patch.weight or shipment_update.weight,
            "content": shipment_patch.content or shipment_update.content,
            # "status": shipment_patch.status.value if shipment_patch.status else shipment_update.status,
            "destination": shipment_patch.destination or shipment_update.destination,
            "estimated_delivery": shipment_update.estimated_delivery,
        }

        shipment_update.sqlmodel_update(updated_shipment)
        shipment = await self._update(shipment_update)

        return shipment

    async def delete(self, id: UUID) -> dict[str, Any]:
        existing_shipment = await self.get(id)
        await self._delete(existing_shipment)
        return {"message": "Shipment deleted successfully"}

    async def cancel(self, id: UUID, seller: Seller):
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise ClientNotAuthorizedError()

        event = await self.event_service.add(
            shipment=shipment, status=ShipmentStatus.cancelled
        )

        shipment.timeline.append(event)

        return shipment

    async def rate(self, token: str, rating: int, comments: str | None):
        token_data = decode_url_safe_token(token)
        if token_data is None:
            raise InvalidTokenError()

        shipment = await self.get(UUID(token_data["id"]))

        new_review = Review(
            rating=rating,
            comment=comments if comments else None,
            shipment_id=shipment.id,
        )
        self.session.add(new_review)
        await self.session.commit()
        return new_review

    async def add_tag(self, shipment_id: UUID, tag_name: TagName):
        shipment = await self.get(shipment_id)

        tag = await tag_name.tag(self.session)
        if tag is None:
            raise EntityNotFoundError()

        shipment.tags.append(tag)
        return await self._update(shipment)

    async def remove_tag(self, shipment_id: UUID, tag_name: TagName):
        shipment = await self.get(shipment_id)

        tag = await tag_name.tag(self.session)
        if tag is None:
            raise EntityNotFoundError()
        try:
            shipment.tags.remove(tag)
            return await self._update(shipment)
        except ValueError:
            raise EntityNotFoundError()
