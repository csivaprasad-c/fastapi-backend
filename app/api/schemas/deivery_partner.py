from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


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
