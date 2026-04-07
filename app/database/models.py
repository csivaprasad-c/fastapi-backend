from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlmodel import Column, Field, Relationship, SQLModel
from uuid import uuid4, UUID


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    delivered = "delivered"
    out_for_delivery = "out_for_delivery"


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    
    seller_id: UUID = Field(foreign_key="sellers.id")
    seller: "Seller" = Relationship(
        back_populates="shipments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Seller(SQLModel, table=True):
    __tablename__ = "sellers"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    name: str
    address: str

    email: EmailStr
    password_hash: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"}
    )