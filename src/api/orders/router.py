from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_current_user
from src.api.orders.schemas import OrderCreateSchema, OrderSchema
from src.api.orders.services import order_services
from src.models import UserModel
from src.settings import oauth2_scheme
from src.exceptions import OrderNotFoundError

from src.api.users.services import user_services


order_router = APIRouter(prefix='/orders', tags=['orders'])


@order_router.post('/')
async def create_order(
    form_data: OrderCreateSchema,
    current_user: UserModel = Depends(get_current_user)
) -> OrderSchema:
    order = await order_services.create_order(
        user_id=current_user.id,
        items=form_data.items
    )
    return OrderSchema.model_validate(order)


@order_router.get('/{order_id}')
async def get_order(
    order_id: str,
    current_user: UserModel = Depends(get_current_user)
) -> OrderSchema:
    order = await order_services.get_order(order_id=order_id)

    if not order or order.user_id != current_user.id:
        raise OrderNotFoundError(order_id)

    return OrderSchema.model_validate(order)
