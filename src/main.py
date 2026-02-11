from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.exceptions import UserAlreadyExistsError, InvalidCredentialsError, OrderNotFoundError
from src.api.auth.router import auth_router
from src.api.users.router import user_router
from src.api.orders.router import order_router


app = FastAPI()


@app.exception_handler(UserAlreadyExistsError)
async def user_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={
            'error': 'user_exists_handler',
            'field': exc.field,
            'value': exc.value
        }
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError
):
    return JSONResponse(
        status_code=401,
        content={
            'error': 'invalid_credentials_handler',
            'msg': 'Invalid credentials',
        }

    )


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(
    request: Request,
    exc: OrderNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            'error': 'order_not_found_handler',
            'msg': f"Order '{exc.order_id}' doesn't found",
        }

    )

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)
