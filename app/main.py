from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from contextlib import asynccontextmanager
from rich import panel, print

from app.database.models import Shipment, ShipmentStatus
from app.schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate, ShipmentPatch
from app.database.session import create_db_and_tables, SessionDep

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    create_db_and_tables()
    yield
    print(panel.Panel("Server stopped...", border_style="red"))

app = FastAPI(lifespan=lifespan_handler)

@app.get("/shipment", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return shipment

# @app.get("/shipment/latest")
# def get_latest_shipment():
#     id = max(shipments.keys())
#     return ShipmentRead(
#         **shipments[id]
#     )


@app.get("/shipment/{shipment_id}")
def get_shipment_by_id(shipment_id: int, session: SessionDep):
    shipment = session.get(Shipment, shipment_id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Shipment not found"
        )
    return shipment


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )

@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, Any]:
    # weight = data.get("weight")
    # content = data.get("content")

    # if weight is None or not isinstance(weight, (int, float)):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Weight must be provided and must be a number"
    #     )

    # if weight > 25:
    #     raise HTTPException(
    #         status_code=status.HTTP_406_NOT_ACCEPTABLE,
    #         detail="Shipment weight exceeds the limit of 25 kg"
    #     )
    
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed.value,
        estimated_delivery=datetime.now() + timedelta(days=3)
    )
    
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return {"id": new_shipment.id}


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

@app.put("/shipment/{shipment_id}", response_model=ShipmentRead)
def update_shipment(shipment_id: int, shipment: ShipmentUpdate, session: SessionDep):
    update = shipment.model_dump()
    
    shipment_update = session.get(Shipment, shipment_id)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    shipment_update.sqlmodel_update(update)
    session.add(shipment_update)
    session.commit()
    session.refresh(shipment_update)

    return ShipmentRead(
        **shipment_update.model_dump()
    )

@app.patch("/shipment/{shipment_id}")
def patch_shipment(shipment_id: int, data: ShipmentPatch, session: SessionDep):  
    shipment_update = session.get(Shipment, shipment_id)

    if shipment_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    updated_shipment = {
        "weight": data.weight or shipment_update.weight,
        "content": data.content or shipment_update.content,
        "status": data.status.value if data.status else shipment_update.status,
        "destination": data.destination or shipment_update.destination,
        "estimated_delivery": shipment_update.estimated_delivery
    }

    shipment_update.sqlmodel_update(updated_shipment)
    session.add(shipment_update)
    session.commit()
    session.refresh(shipment_update)

    return ShipmentRead(
        **shipment_update.model_dump()
    )

@app.delete("/shipment/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: int, session: SessionDep) -> None:
    existing_shipment = session.get(Shipment, shipment_id)
    if existing_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return session.delete(existing_shipment)
