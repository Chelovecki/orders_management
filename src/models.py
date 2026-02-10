import enum
import uuid
from decimal import Decimal

from sqlalchemy import TIMESTAMP, Column, DateTime, NUMERIC, Enum, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, JSON


class Base(DeclarativeBase):
    pass


class OrderConditions(enum.Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    CANCELED = 'CANCELED'


class OrderModel(Base):
    __tablename__ = 'orders'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    items = Column(JSON)
    total_price: Mapped[Decimal] = mapped_column(
        NUMERIC(14, 2),
        nullable=False
    )
    status: Mapped[OrderConditions] = mapped_column(
        Enum(OrderConditions, native_enum=False),
        default=OrderConditions.PENDING,
        server_default=OrderConditions.PENDING.value,
        nullable=False,

    )
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp()
    )

    # many-to-one
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(
        'UserModel', back_populates='orders')


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    # one-to-many
    orders: Mapped[list['OrderModel']] = relationship(
        'OrderModel',
        back_populates='user',
        cascade='all, delete-orphan'
    )
