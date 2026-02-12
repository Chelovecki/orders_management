import uuid
from uuid import UUID

from sqlalchemy import select

from src.api.orders.schemas import OrderItemSchema
from src.exceptions import OrderNotFoundError, UserNotFoundError
from src.models import OrderModel, UserModel
from src.services import BaseService
from src.settings import PostgresSettings


class OrderServices(BaseService):
    def __init__(self, session):
        super().__init__(session)

    async def create_order(
        self, user_id: int, items: list[OrderItemSchema]
    ) -> OrderModel:

        items_data = [
            {**item.model_dump(), "price": float(item.price)} for item in items
        ]

        total_sum = sum(item.price * item.quantity for item in items)

        order = OrderModel(user_id=user_id, items=items_data, total_price=total_sum)

        async with self.session_factory() as session:
            session.add(order)
            await session.commit()
            await session.refresh(order, ["user"])
            return order

    async def get_order(self, order_id: str) -> OrderModel:
        try:
            order_uuid = uuid.UUID(order_id)
        except ValueError:  # 'badly formed hexadecimal UUID string'
            raise OrderNotFoundError(order_id)

        async with self.session_factory() as session:
            order = await session.get(OrderModel, order_uuid)

            if not order:
                raise OrderNotFoundError(order_id)

            return order

    async def update_status_order(self, order_id: UUID, new_status: str) -> OrderModel:
        async with self.session_factory() as session:
            order = await session.get(OrderModel, order_id)

            if not order:
                raise OrderNotFoundError(order_id)

            order.status = new_status

            session.add(order)
            await session.commit()
            return order

    async def get_users_orders(self, user_id: int) -> list[OrderModel]:
        async with self.session_factory() as session:
            user = await session.get(UserModel, user_id)

            if not user:
                raise UserNotFoundError

            stmt = select(OrderModel).where(OrderModel.user_id == user_id)
            res = await session.execute(statement=stmt)
            orders = res.scalars().all()
            print(type(orders), orders)
            return orders

            # todo добавить limit и offset


order_services = OrderServices(PostgresSettings.get_session())
