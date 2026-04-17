from typing import Sequence

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import select, any_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.api.schemas.deivery_partner import CreateDeliveryPartner
from app.database.models import DeliveryPartner, Shipment, Location
from app.services.user import UserService
from app.core.exceptions import DeliveryPartnerNotAvailableError


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: CreateDeliveryPartner):
        partner: DeliveryPartner = await self._add(
            delivery_partner.model_dump(
                exclude={"serviceable_zipcodes"}), "partners"
        )
        for zip_code in delivery_partner.serviceable_zip_codes:
            location = await self.session.get(Location, zip_code)
            partner.serviceable_locations.append(
                location if location else Location(zip_code=zip_code)
            )

        return await self._update(partner)

    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)

    async def token(self, email, password) -> str:
        token = await self._generate_token(email, password)
        return token

    async def get_delivery_partners_by_zipcode(
        self, zipcode: int
    ) -> Sequence[DeliveryPartner]:
        result = await self.session.scalars(
            select(DeliveryPartner)
            .join(col(DeliveryPartner.serviceable_locations))
            .where(col(Location.zip_code) == zipcode)
        )
        return result.all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_delivery_partners_by_zipcode(
            shipment.destination
        )
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        raise DeliveryPartnerNotAvailableError()
