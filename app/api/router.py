from fastapi import APIRouter

from app.api.routers.shipment import router as shipment_router
from app.api.routers.sellers import router as sellers_router

master_router = APIRouter()

master_router.include_router(shipment_router)
master_router.include_router(sellers_router)
