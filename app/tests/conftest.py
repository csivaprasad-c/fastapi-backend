from uuid import uuid4

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.database.session import get_session
from app.main import app
from app.tests import example
from app.tests.example import SELLER

engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")
test_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session_override():
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def seller_token(client: AsyncClient):
    response = await client.post(
        "/sellers/token",
        data={
            "username": SELLER["email"],
            "password": SELLER["password"],
            "grant_type": "password",
        },
    )
    assert "access_token" in response.json()
    return response.json()["access_token"]


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client


test_id = uuid4()


def get_id_override():
    return test_id


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_and_teardown():
    print("🧪 Starting tests...")

    app.dependency_overrides[get_session] = get_session_override

    async with engine.begin() as connection:
        from app.database.models import (
            Shipment,
            Seller,
            DeliveryPartner,
            Tag,
            TagName,
            ShipmentEvent,
            ShipmentTag,
        )

        await connection.run_sync(SQLModel.metadata.create_all)

    async with test_session() as session:
        await example.create_test_data(session=session)

    yield

    async with engine.begin() as connection:
        from app.database.models import (
            Shipment,
            Seller,
            DeliveryPartner,
            Tag,
            TagName,
            ShipmentEvent,
            ShipmentTag,
        )

        await connection.run_sync(SQLModel.metadata.drop_all)

    app.dependency_overrides.clear()
    print("🧪 Tests completed.")
