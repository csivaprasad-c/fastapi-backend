from typing import Any, Callable

routes: dict[str, Callable[[], Any]] = {}

def route(path: str):
    def register_route(func):
        routes[path] = func
        return func
    return register_route

@route("/shipment")
def get_shipment() -> dict[str, Any]:
    return {
        "content": "wooden table",
        "status": "in transit"
    }

request: str = ""

while request != "exit":
    request = input("Enter a path >: ")
    if request in routes:
        response = routes[request]()
        print(response, end="\n\n")
    else:
        print("404 Not Found") 