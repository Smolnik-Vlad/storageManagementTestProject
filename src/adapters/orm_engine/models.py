import enum

from sqlalchemy import String, Float, CheckConstraint, Integer, types, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class Status(str, enum.Enum):
    IN_PROGRESS = "IN PROGRESS"
    IN_DELIVERY = "IN DELIVERY"
    DELIVERED = "DELIVERED"


class Product(Base):
    __tablename__ = 'product'
    product_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    description: Mapped[str]
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
        CheckConstraint('count >= 0', name='check_count_positive'),
    )

    order_items: Mapped[list['OrderItem']] = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined"
    )


class Order(Base):
    __tablename__ = 'order'
    order_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    created_at: Mapped[types.DateTime] = mapped_column(
        types.DateTime, server_default=func.current_timestamp()
    )
    status: Mapped[Status] = mapped_column(default=Status.IN_PROGRESS)

    order_items: Mapped[list['OrderItem']] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined"
    )


class OrderItem(Base):
    __tablename__ = 'order_item'
    order_item_id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False, autoincrement=True)
    product_count: Mapped[int]
    product_id: Mapped[int | None] = mapped_column(ForeignKey("product.product_id", ondelete="CASCADE"))
    order_id: Mapped[int] = mapped_column(ForeignKey("order.order_id", ondelete="CASCADE"))

    product: Mapped[Product] = relationship(
        back_populates="order_items",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined"
    )
    order: Mapped[Order] = relationship(
        back_populates="order_items",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined"
    )
