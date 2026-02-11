from fastapi import APIRouter, Depends
from src.api.dependencies import get_current_user
from src.api.orders.schemas import OrderCreateSchema, OrderSchema
from src.api.orders.services import order_services
from src.models import UserModel
from src.settings import oauth2_scheme

from src.api.users.services import user_services


order_router = APIRouter(prefix='/orders')


@order_router.post('/create')
async def create_order(
    form_data: OrderCreateSchema,
    current_user: UserModel = Depends(get_current_user)
):
    order = await order_services.create_order(
        user_id=current_user.id,
        items=form_data.items
    )
    return OrderSchema.model_validate(order) 
