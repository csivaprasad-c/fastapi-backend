from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from random import randint
from typing import Optional

from app.database.models import ShipmentStatus

def random_destination():
    return randint(11000, 11999)

class ShipmentBase(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, description="Weight must be less than 25 kg")
    destination: int

class ShipmentRead(ShipmentBase):
    status: ShipmentStatus
    estimated_delivery: datetime

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(ShipmentBase):
    status: ShipmentStatus
    estimated_delivery: Optional[datetime] = Field(default=None)

class ShipmentPatch(BaseModel):
    content: Optional[str] = Field(default=None, max_length=30)
    weight: Optional[float] = Field(default=None, le=25, description="Weight must be less than 25 kg")
    destination: Optional[int] = Field(default=None)
    status: Optional[ShipmentStatus] = Field(default=None)