from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Seller, DeliveryPartner, Location
from app.services.user import hash_password

SELLER = {
    "name": "RainForest",
    "email": "rainforest@xmailg.one",
    "password": "lovetrees",
    "zip_code": 11001,
}

DELIVERY_PARTNER = {
    "name": "FastShip",
    "email": "fastship@xmailg.one",
    "password": "fastdelivery",
    "zip_code": 11001,
    "max_handling_capacity": 4,
    "serviceable_zip_codes": [11001, 11002, 11003, 11004, 11005],
}

SHIPMENT = {
    "content": "Bananas",
    "weight": 1.25,
    "destination": 11004,
    "client_contact_email": "py@mailx.org",
}


async def create_test_data(session: AsyncSession):
    session.add(
        Seller(
            **SELLER,
            email_verified=True,
            password_hash=hash_password(SELLER["password"])
        )
    )

    session.add(
        DeliveryPartner(
            **DELIVERY_PARTNER,
            email_verified=True,
            password_hash=hash_password(DELIVERY_PARTNER["password"]),
            serviceable_locations=[
                Location(zip_code=zip_code)
                for zip_code in DELIVERY_PARTNER["serviceable_zip_codes"]
            ]
        )
    )

    await session.commit()
