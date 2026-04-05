from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from app.schemas import ShipmentRead, ShipmentCreate, ShipmentStatus, ShipmentUpdate, ShipmentPatch
from .database import Database

app = FastAPI()

db = Database()

@app.get("/shipment", status_code=status.HTTP_200_OK, response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead(
        **shipment
    )

# @app.get("/shipment/latest")
# def get_latest_shipment():
#     id = max(shipments.keys())
#     return ShipmentRead(
#         **shipments[id]
#     )


@app.get("/shipment/{shipment_id}")
def get_shipment_by_id(shipment_id: int):
    shipment = db.get(shipment_id)
    
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Shipment not found"
        )
    return ShipmentRead(
        **shipment
    )


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )

@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
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
    
    new_id = db.create(shipment)
    return new_id


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
def update_shipment(shipment_id: int, shipment: ShipmentUpdate):
    updated_shipment = db.update(shipment_id, shipment)

    if updated_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )

    return ShipmentRead(
        **updated_shipment
    )

@app.patch("/shipment/{shipment_id}")
def patch_shipment(shipment_id: int, data: ShipmentPatch):
    updated_shipment = db.patch(shipment_id, data)

    if updated_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    return ShipmentRead( 
        **updated_shipment
    )

@app.delete("/shipment/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(shipment_id: int) -> None:
    return db.delete(shipment_id)
