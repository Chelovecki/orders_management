import uuid
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select

from src.api.orders.schemas import OrderItemSchema
from src.exceptions import InvalidOrderError, OrderNotFoundError, UserNotFoundError
from src.models import OrderModel, UserModel
from src.services import BaseService
from src.settings import PostgresSettings


class OrderServices(BaseService):
    def __init__(self, session):
        super().__init__(session)

    async def create_order(
        self, user_id: int, items: list[OrderItemSchema]
    ) -> OrderModel:
        if not items:
            raise InvalidOrderError("Order must contain at least one item")

        items_data = []
        for item in items:
            values = item.model_dump()
            if values["price"] <= Decimal("0.00"):
                raise InvalidOrderError(
                    f"Item '{values['name']}' should have positive price (0>)"
                )

            if values["quantity"] <= 0:
                raise InvalidOrderError(
                    f"Amount of item '{values['name']}' should be >=1 "
                )

            values["price"] = str(values["price"])
            items_data.append(values)

        total_sum = sum(item.price * item.quantity for item in items)

        order = OrderModel(user_id=user_id, items=items_data, total_price=total_sum)

        async with self.session_factory() as session:
            session.add(order)
            await session.commit()
            await session.refresh(order, ["user"])
            return order

    async def get_order(
        self, order_id: uuid.UUID, request_from_user_id: int
    ) -> OrderModel:

        async with self.session_factory() as session:
            order = await session.get(OrderModel, order_id)

            if not order or order.user_id != request_from_user_id:
                raise OrderNotFoundError(order_id)
            return order

    async def update_status_order(
        self, order_id: UUID, request_from_user_id: int, new_status: str
    ) -> OrderModel:
        async with self.session_factory() as session:
            order = await session.get(OrderModel, order_id)

            if not order or order.user_id != request_from_user_id:
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

            return res.scalars().all()

            # todo добавить limit и offset


order_services = OrderServices(PostgresSettings.get_session())
