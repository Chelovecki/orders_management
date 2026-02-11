from datetime import datetime
import uuid
from pydantic import ConfigDict, Field, BaseModel
from decimal import Decimal
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
