import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.tests.conftest import test_id
from app.tests.example import SELLER
from app.utils import print_label


# @pytest.mark.asyncio
async def test_app(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastShip!"}


async def test_seller_login(client: AsyncClient):
    response = await client.post(
        "/sellers/token",
        data={
            "username": SELLER["email"],
            "password": SELLER["password"],
            "grant_type": "password",
        },
    )

    print_label(response.json())
