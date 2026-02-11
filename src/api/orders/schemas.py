import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import Field

from src.api.dependencies import BaseSchema
from src.api.users.schemas import UserSchema
from src.models import OrderConditions


class OrderSchema(BaseSchema):
    id: uuid.UUID
    items: list
    total_price: Decimal
    status: OrderConditions
    created_at: datetime

    user: UserSchema


class OrderItemSchema(BaseSchema):
    name: str
    price: Decimal
    quantity: int


class OrderCreateSchema(BaseSchema):
    items: list[OrderItemSchema] = Field(...)
