from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from rich import panel, print
from starlette.responses import JSONResponse

from app.core.exceptions import InvalidTokenError, add_exception_handlers
from app.database.session import create_db_and_tables

from app.api.router import master_router as router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    await create_db_and_tables()
    yield
    print(panel.Panel("Server stopped...", border_style="red"))

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router=router)

add_exception_handlers(app=app)

# @app.get("/shipment/latest")
# def get_latest_shipment():
#     id = max(shipments.keys())
#     return ShipmentRead(
#         **shipments[id]
#     )

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )


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
