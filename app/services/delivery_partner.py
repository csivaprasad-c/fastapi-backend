from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, any_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.deivery_partner import CreateDeliveryPartner
from app.database.models import DeliveryPartner, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner, session)
    
    async def add(self, delivery_partner: CreateDeliveryPartner):
        user = await self._add(delivery_partner.model_dump())
        return user

    async def update(self, partner: DeliveryPartner):
        return await self._update(partner)
    
    async def token(self, email, password) -> str:
        token = await self._generate_token(email, password)
        return token
    
    async def get_delivery_partners_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        result = await self.session.scalars(
            select(DeliveryPartner).where(
                zipcode == any_(DeliveryPartner.serviceable_zip_codes)
            )
        )
        return result.all()
    
    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_delivery_partners_by_zipcode(shipment.destination)
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner
        
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="No delivery partner available"
        )