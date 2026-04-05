from enum import Enum

from pydantic import BaseModel, Field
from random import randint
from typing import Optional

def random_destination():
    return randint(11000, 11999)

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"

class ShipmentBase(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, description="Weight must be less than 25 kg")
    destination: int

class ShipmentRead(ShipmentBase):
    status: ShipmentStatus

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(ShipmentBase):
    status: ShipmentStatus

class ShipmentPatch(BaseModel):
    content: Optional[str] = Field(default=None, max_length=30)
    weight: Optional[float] = Field(default=None, le=25, description="Weight must be less than 25 kg")
    destination: Optional[int] = Field(default=None)
    status: Optional[ShipmentStatus] = Field(default=None)