from rich import print, panel
import time
import asyncio

async def endpoint(route: str) -> str:
    print(f">> handling {route}")

    await asyncio.sleep(1)

    print(f"<< done handling {route}")
    return f"Response for {route}"

async def server():
    tests = (
        "GET /shipment",
        "GET /shipment/1",
        "POST /shipment",
    )

    start = time.perf_counter()

    for route in tests:
        result = await endpoint(route)
        print(f"Result for {route}: {result}")

    end = time.perf_counter()
    print(panel.Panel(f"Total time taken: {end - start:.2f} seconds", border_style="blue"))

asyncio.run(server())
