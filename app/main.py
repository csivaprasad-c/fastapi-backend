import uuid
from time import perf_counter
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, Request, Response, Depends
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from rich import panel, print
from fastapi.middleware.cors import CORSMiddleware

from app.api.tag import APITag
from app.core.exceptions import add_exception_handlers

from app.database.session import create_db_and_tables

from app.api.router import master_router as router
from app.workers.tasks import add_log

description = """
Delivery Management System for sellers and delivery agents

### Seller
- Submit shipments effortlessly
- Share tracking links with customers
- Receive notifications on shipment updates

### Delivery Agent
- Auto accept shipments
- Track and update shipment status
- Email and SMS notifications
"""


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    await create_db_and_tables()
    yield
    print(panel.Panel("Server stopped...", border_style="red"))


app = FastAPI(
    lifespan=lifespan_handler,
    title="FastShip",
    description=description,
    docs_url=None,
    redoc_url=None,
    version="0.1.0",
    terms_of_service="https://fastship.vercel.app/terms",
    contact={
        "name": "FastShip Support",
        "url": "https://fastship.vercel.app/support",
        "email": "support@fastship.com",
    },
    openapi_tags=[
        {"name": APITag.SHIPMENT, description: "Shipment related endpoints"},
        {"name": APITag.SELLER, "description": "Seller related endpoints"},
        {"name": APITag.PARTNER, "description": "Delivery Partner related endpoints"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router)

add_exception_handlers(app=app)


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start = perf_counter()
    response: Response = await call_next(request)
    end = perf_counter()
    time_taken = round(end - start, 2)
    add_log.delay(
        f"{request.method} {request.url} ({response.status_code}) {time_taken:.2f}s"
    )
    return response


# @app.get("/shipment/latest")
# def get_latest_shipment():
#     id = max(shipments.keys())
#     return ShipmentRead(
#         **shipments[id]
#     )


@app.get("/")
def get_root():
    return {"message": "Welcome to FastShip!"}


@app.get("/docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="FastShip API")


# @app.post("/shipment", status_code=status.HTTP_201_CREATED)
# def submit_shipment(content: str, weight: float) -> dict[str, Any]:
#     if weight > 25:
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE,
#             detail="Shipment weight exceeds the limit of 25 kg"
#         )

#     new_id = max(shipments.keys()) + 1
#     shipments[new_id] = {
#         "weight": weight,
#         "content": content,
#         "status": "placed"
#     }
#     return shipments[new_id]
