from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.exceptions import (
    InvalidCredentialsError,
    InvalidOrderError,
    OrderNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "user_exists_handler",
            "field": exc.field,
            "value": exc.value,
        },
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404, content={"error": "user_not_found", "user_id": exc.user_id}
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={
            "error": "invalid_credentials_handler",
            "msg": "Invalid credentials",
        },
    )


async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "order_not_found_handler",
            "msg": f"Order '{exc.order_id}' doesn't found",
        },
    )


async def invalid_order_handler(request: Request, exc: InvalidOrderError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "invalid_order_handler", "msg": exc.msg},
    )
