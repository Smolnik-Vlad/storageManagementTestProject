from dataclasses import dataclass

from sqlalchemy import update, case, exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.orm_engine.models import Product, Order, OrderItem
from src.core.exceptions import DatabaseException
from src.data_classes.order_product_dataclass import ProductDataClass, CreateOrderDataClass, NewOrderItemDataClass, \
    OrderDataClass
from src.ports.repositories.order_rep import OrderRepository


@dataclass
class SQLAlchemyOrderRepository(OrderRepository):
    _db_session: AsyncSession

    async def create_order(self, order_items_list: list[CreateOrderDataClass]) -> OrderDataClass:
        try:
            new_order = Order()
            self._db_session.add(new_order)
            await self._db_session.flush()

            product_ids = [item.product_id for item in order_items_list]

            # update product count
            case_expression = case(
                *[
                    (Product.product_id == order_item.product_id, Product.count - order_item.count)
                    for order_item in order_items_list
                ],
                else_=Product.count
            )

            query_update_product = (
                update(Product)
                .where(Product.product_id.in_(product_ids))
                .values(count=case_expression)
                .returning(Product)
            )

            await self._db_session.execute(query_update_product)

            # create new order items
            new_order_items = [
                OrderItem(
                    order_id=new_order.order_id,
                    product_id=order_item.product_id,
                    product_count=order_item.count
                )
                for order_item in order_items_list
            ]

            self._db_session.add_all(new_order_items)
            await self._db_session.flush()

            list_of_order_items = [
                NewOrderItemDataClass(
                    product_id=order_item.product_id,
                    count=order_item.product_count
                )
                for order_item in new_order_items
            ]

            new_order = OrderDataClass(
                order_id=new_order.order_id,
                list_of_orderItems=list_of_order_items
            )
            return new_order
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def get_all_orders(self) -> list[OrderDataClass]:
        try:
            query = select(Order)
            db_response = await self._db_session.execute(query)
            result = db_response.unique().scalars().all()

            return [
                OrderDataClass(
                    order_id=order.order_id,
                    status=order.status,
                    list_of_orderItems=[
                        NewOrderItemDataClass(
                            product_id=order_item.product_id,
                            count=order_item.product_count
                        )
                        for order_item in order.order_items
                    ]
                )
                for order in result
            ]
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def get_order_by_id(self, order_id: int) -> OrderDataClass | None:
        try:
            query = select(Order).where(Order.order_id == order_id).distinct()
            res = await self._db_session.execute(query)
            order_data = res.unique().scalar_one_or_none()
            return OrderDataClass(
                order_id=order_data.order_id,
                status=order_data.status,
                list_of_orderItems=[
                    NewOrderItemDataClass(
                        product_id=order_item.product_id,
                        count=order_item.product_count
                    )
                    for order_item in order_data.order_items
                ]
            ) if order_data else None
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def update_order_status(self, order_id: int, new_status: str) -> OrderDataClass:
        try:
            query = (update(Order)
                     .where(Order.order_id == order_id)
                     .values(status=new_status)
                     .returning(Order))
            res_database = await self._db_session.execute(query)
            order_data = res_database.unique().scalar_one_or_none()
            return OrderDataClass(
                order_id=order_data.order_id,
                status=order_data.status,
            ) if order_data else None
        except exc.SQLAlchemyError:
            raise DatabaseException