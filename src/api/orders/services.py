from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from src.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from src.models import OrderModel
from src.services import BaseService
from src.settings import PostgresSettings, oauth2_scheme
from src.security.jwt import decode_token
from src.api.orders.schemas import OrderItemSchema


class OrderServices(BaseService):
    def __init__(self, session):
        super().__init__(session)

    async def create_order(self, user_id: int, items: list[OrderItemSchema]) -> OrderModel:

        items_data = [
            {
                **item.model_dump(),
                'price': str(item.price)
            }
            for item in items
        ]

        total_sum = sum(item.price * item.quantity for item in items)

        order = OrderModel(
            user_id=user_id,
            items=items_data,
            total_price=total_sum
        )

        async with self.session_factory() as session:
            session.add(order)
            await session.commit()
            await session.refresh(order, ['user'])
            return order


order_services = OrderServices(PostgresSettings.get_session())
