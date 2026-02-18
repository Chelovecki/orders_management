import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.api.auth.router import auth_router
from src.api.orders.router import order_router
from src.api.users.router import user_router
from src.exception_handlers import (
    invalid_credentials_handler,
    invalid_order_handler,
    order_not_found_handler,
    user_exists_handler,
    user_not_found_handler,
)
from src.exceptions import (
    InvalidCredentialsError,
    InvalidOrderError,
    OrderNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.rabbit import close_rabbit, init_rabbit

# логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
    force=True,
)


# Запуск Rabbit
@asynccontextmanager
async def lifespan(app: FastAPI):
    channel = await init_rabbit()
    app.state.rabbit_channel = channel
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

# подключение обработчиков исключений
app.add_exception_handler(UserAlreadyExistsError, user_exists_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
app.add_exception_handler(OrderNotFoundError, order_not_found_handler)
app.add_exception_handler(InvalidOrderError, invalid_order_handler)

# подключение api-роутеров
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)
