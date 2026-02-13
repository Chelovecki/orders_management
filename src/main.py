from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.auth.router import auth_router
from src.api.orders.router import order_router
from src.api.users.router import user_router
from src.exceptions import (
    InvalidCredentialsError,
    InvalidOrderError,
    OrderNotFoundError,
    UserAlreadyExistsError,
)
from src.rabbit import close_rabbit, init_rabbit


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_rabbit()
    yield
    await close_rabbit()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(UserAlreadyExistsError)
async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={
            "error": "user_exists_handler",
            "field": exc.field,
            "value": exc.value,
        },
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={
            "error": "invalid_credentials_handler",
            "msg": "Invalid credentials",
        },
    )


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "order_not_found_handler",
            "msg": f"Order '{exc.order_id}' doesn't found",
        },
    )


@app.exception_handler(InvalidOrderError)
async def invalid_order_handler(request: Request, exc: InvalidOrderError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "invalid_order_handler", "msg": exc.msg},
    )


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)
