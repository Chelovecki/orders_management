from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

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


# Запуск Rabbit
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_rabbit()
    yield
    await close_rabbit()


app = FastAPI(lifespan=lifespan)

# CORS-защита
origins = [
    "http://localhost:8000",  # API проекта
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # разрешить отправку куки/авторизации
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["50/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


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
