from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# from random import randint
from typing import Optional

from app.database.models import Seller, ShipmentEvent, ShipmentStatus

# def random_destination():
#     return randint(11000, 11999)


class ShipmentBase(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, description="Weight must be less than 25 kg")
    destination: int


class ShipmentRead(ShipmentBase):
    id: UUID
    # status: ShipmentStatus
    estimated_delivery: datetime
    seller: Seller
    timeline: list[ShipmentEvent]

    model_config = {"from_attributes": True}


class ShipmentPage(BaseModel):
    items: list[ShipmentRead]
    next_cursor: Optional[UUID]


class ShipmentCreate(ShipmentBase):
    client_contact_email: EmailStr
    client_contact_phone: Optional[str] = Field(default=None)


class ShipmentUpdate(BaseModel):
    location: Optional[int] = Field(default=None)
    status: Optional[ShipmentStatus] = Field(default=None)
    description: Optional[str] = Field(default=None)
    estimated_delivery: Optional[datetime] = Field(default=None)
    verification_code: Optional[int] = Field(default=None)


class ShipmentPatch(BaseModel):
    content: Optional[str] = Field(default=None, max_length=30)
    weight: Optional[float] = Field(
        default=None, le=25, description="Weight must be less than 25 kg"
    )
    destination: Optional[int] = Field(default=None)
    status: Optional[ShipmentStatus] = Field(default=None)


class ShipmentReview(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None)
