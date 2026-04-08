from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER   
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
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
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

    delivery_partner_id: UUID = Field(foreign_key="delivery_partners.id")
    delivery_partner: "DeliveryPartner" = Relationship(
       back_populates="shipments",
       sa_relationship_kwargs={"lazy":"selectin"}
    )

class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str = Field(exclude=True)

class Seller(User, table=True):
    __tablename__ = "sellers"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )

    shipments: list[Shipment] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partners"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now
        )
    )
    serviceable_zip_codes: list[int] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(INTEGER))
    )
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
        ]
    
    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)