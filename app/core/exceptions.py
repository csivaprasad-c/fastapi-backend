from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse


class FastShipError(Exception):
    """Base exception for all exceptions in the FastShip application"""

    status_code = status.HTTP_400_BAD_REQUEST


class EntityNotFoundError(FastShipError):
    """Exception raised when an entity is not found"""

    status_code = status.HTTP_404_NOT_FOUND


class ClientNotAuthorizedError(FastShipError):
    """Exception raised when a client is not authorized to perform an action"""

    status_code = status.HTTP_401_UNAUTHORIZED


class ClientNotVerifiedError(FastShipError):
    """Exception raised when a client is not verified"""

    status_code = status.HTTP_403_FORBIDDEN


class BadCredentialsError(FastShipError):
    """Exception raised when the provided credentials are invalid"""

    status_code = status.HTTP_401_UNAUTHORIZED


class InvalidTokenError(FastShipError):
    """Exception raised when an invalid token is provided"""

    status_code = status.HTTP_401_UNAUTHORIZED


class DeliveryPartnerNotAvailableError(FastShipError):
    """Exception raised when a delivery partner is not available"""

    status_code = status.HTTP_406_NOT_ACCEPTABLE


class DeliveryPartnerCapacityExceededError(FastShipError):
    """Exception raised when a delivery partner's capacity is exceeded"""

    status_code = status.HTTP_406_NOT_ACCEPTABLE


class NothingToUpdateError(FastShipError):
    """Exception raised when nothing is provided to update"""

    status_code = status.HTTP_400_BAD_REQUEST


def _get_handler(status_code: int, detail: str):
    def handler(request: Request, exception: Exception) -> Response:
        from rich import print, panel

        print(panel.Panel(f"Handled: {exception.__class__.__name__}"))
        raise HTTPException(status_code=status_code, detail=detail)

    return handler


def add_exception_handlers(app: FastAPI):
    exception_classes = FastShipError.__subclasses__()
    for exception_class in exception_classes:
        app.add_exception_handler(
            exception_class,
            _get_handler(
                status_code=exception_class.status_code,
                detail=exception_class.__doc__ or "An error occurred",
            ),
        )

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_server_error_handler(request, exception):
        return JSONResponse(
            content={"detail": "Something went wrong. Please try again later."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={"X-Error": f"{exception}"},
        )
