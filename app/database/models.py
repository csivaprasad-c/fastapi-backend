from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, INTEGER, select
from sqlmodel import Column, Field, Relationship, SQLModel
from uuid import uuid4, UUID

from sqlmodel.ext.asyncio.session import AsyncSession


class TagName(str, Enum):
    EXPRESS = "EXPRESS"
    STANDARD = "STANDARD"
    FRAGILE = "FRAGILE"
    HEAVY = "HEAVY"
    INTERNATIONAL = "INTERNATIONAL"
    DOMESTIC = "DOMESTIC"
    TEMPERATURE_CONTROLLED = "TEMPERATURE_CONTROLLED"
    GIFT = "GIFT"
    RETURN = "RETURN"
    DOCUMENTS = "DOCUMENTS"

    async def tag(self, session: AsyncSession) -> Tag | None:
        return await session.scalar(select(Tag).where(Tag.name == self.value))


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    delivered = "delivered"
    out_for_delivery = "out_for_delivery"
    cancelled = "cancelled"


class ShipmentTag(SQLModel, table=True):
    __tablename__ = "shipment_tags"

    shipment_id: UUID = Field(foreign_key="shipments.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    name: TagName
    instruction: str

    shipments: list["Shipment"] = Relationship(
        back_populates="tags",
        link_model=ShipmentTag,
        sa_relationship_kwargs={"lazy": "immediate"},
    )


class Shipment(SQLModel, table=True):
    __tablename__ = "shipments"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    client_contact_email: EmailStr
    client_contact_phone: Optional[str]

    content: str
    weight: float = Field(le=25)
    destination: int
    estimated_delivery: datetime

    timeline: list[ShipmentEvent] = Relationship(
        back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"}
    )

    seller_id: UUID = Field(foreign_key="sellers.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )

    delivery_partner_id: UUID = Field(foreign_key="delivery_partners.id")
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )

    review: "Review" = Relationship(
        back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"}
    )

    tags: list[Tag] = Relationship(
        back_populates="shipments",
        link_model=ShipmentTag,
        sa_relationship_kwargs={"lazy": "immediate"},
    )

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None


class User(SQLModel):
    name: str
    email: EmailStr
    email_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)


class Seller(User, table=True):
    __tablename__ = "sellers"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )

    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    address: str | None = Field(default=None)
    zip_code: int | None = Field(default=None)

    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )


class ServiceableLocation(SQLModel, table=True):
    __tablename__ = "serviceable_locations"

    partner_id: UUID = Field(foreign_key="delivery_partners.id", primary_key=True)
    location_id: int = Field(foreign_key="locations.zip_code", primary_key=True)


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partners"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    # serviceable_zip_codes: list[int] = Field(
    #     default_factory=list, sa_column=Column(ARRAY(INTEGER))
    # )
    serviceable_locations: list["Location"] = Relationship(
        back_populates="delivery_partners",
        link_model=ServiceableLocation,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    max_handling_capacity: int
    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner", sa_relationship_kwargs={"lazy": "selectin"}
    )

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
            or shipment.status != ShipmentStatus.cancelled
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)


## Event Models
class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_events"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )

    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    location: int
    status: ShipmentStatus
    description: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipments.id")
    shipment: Shipment = Relationship(
        back_populates="timeline", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID, primary_key=True),
    )

    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipments.id")
    shipment: Shipment = Relationship(
        back_populates="review", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Location(SQLModel, table=True):
    __tablename__ = "locations"

    zip_code: int = Field(primary_key=True)

    delivery_partners: list[DeliveryPartner] = Relationship(
        back_populates="serviceable_locations",
        link_model=ServiceableLocation,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
