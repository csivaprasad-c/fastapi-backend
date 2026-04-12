from time import perf_counter

from fastapi import FastAPI, Request, Response
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from rich import panel, print
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import add_exception_handlers
from app.database.session import create_db_and_tables

from app.api.router import master_router as router
from app.workers.tasks import add_log


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    await create_db_and_tables()
    yield
    print(panel.Panel("Server stopped...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)

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


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")


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
