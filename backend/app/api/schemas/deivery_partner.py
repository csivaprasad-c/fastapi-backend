from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.api.schemas.shipment import ShipmentRead


class BaseDeliveryPartner(BaseModel):
    name: str = Field(max_length=30)
    email: EmailStr = Field(max_length=50)
    max_handling_capacity: int


class CreateDeliveryPartner(BaseDeliveryPartner):
    password: str
    serviceable_zip_codes: list[int]


class ReadDeliveryPartner(BaseDeliveryPartner):
    id: UUID


class UpdateDeliveryPartner(BaseModel):
    serviceable_zip_codes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)


class DeliveryPartnerShipment(BaseModel):
    shipments: list[ShipmentRead]
    total_shipments: int
    page: int
    total_pages: int


class PaginationParams(BaseModel):
    page: int = 1
    pageSize: int = 10
    order: Literal["asc", "desc"] = "asc"


def get_pagination_params(
    page: int = 1, pageSize: int = 10, order: Literal["asc", "desc"] = "asc"
) -> PaginationParams:
    return PaginationParams(page=page, pageSize=pageSize, order=order)
