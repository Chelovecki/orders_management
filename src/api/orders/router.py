import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_current_user
from src.api.orders.schemas import OrderCreateSchema, OrderSchema, OrderUpdateSchema
from src.api.orders.services import order_services
from src.models import UserModel
from src.redis import async_redis as redis

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("/")
async def create_order(
    form_data: OrderCreateSchema, current_user: UserModel = Depends(get_current_user)
) -> OrderSchema:
    order = await order_services.create_order(
        user_id=current_user.id, items=form_data.items
    )
    return OrderSchema.model_validate(order)


@order_router.get("/{order_id}")
async def get_order(
    order_id: uuid.UUID, current_user: UserModel = Depends(get_current_user)
) -> OrderSchema:
    print("Data in Redis:", bool(await redis.get(str(order_id))), f'\nExp at {await redis.ttl(str(order_id))}')

    lock_key = f"lock:{order_id}"  # для race conditions

    if data := await redis.get(str(order_id)):
        return OrderSchema.model_validate_json(data)

    async with redis.lock(lock_key, timeout=5):
        # Проверяем снова после получения lock
        if data := await redis.get(order_id):
            return OrderSchema.model_validate_json(data)
        
    order = await order_services.get_order(
        order_id=order_id, request_from_user_id=current_user.id
    )

    order_schema = OrderSchema.model_validate(order)

    await redis.set(name=str(order_id), value=order_schema.model_dump_json(), ex=300)

    return order_schema


@order_router.patch("/{order_id}")
async def change_order(
    order_id: uuid.UUID,
    form_data: OrderUpdateSchema,
    current_user: UserModel = Depends(get_current_user),
) -> OrderSchema:

    order = await order_services.update_status_order(
        order_id=order_id,
        request_from_user_id=current_user.id,
        new_status=form_data.status,
    )

    await redis.delete(str(order.id))

    return OrderSchema.model_validate(order)


@order_router.get("/user/{user_id}")
async def get_users_orders(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
) -> list[OrderSchema]:
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own orders",
        )

    user_orders = await order_services.get_users_orders(user_id=user_id)
    return [OrderSchema.model_validate(order) for order in user_orders]
