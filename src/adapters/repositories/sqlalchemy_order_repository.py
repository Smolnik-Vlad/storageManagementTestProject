from dataclasses import dataclass

from sqlalchemy import update, case
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm_engine.models import Product, Order, OrderItem
from src.data_classes.order_product_dataclass import ProductDataClass, CreateOrderDataClass, NewOrderItemDataClass, \
    NewSavedOrderDataClass
from src.ports.repositories.order_rep import OrderRepository


@dataclass
class SQLAlchemyOrderRepository(OrderRepository):
    _db_session: AsyncSession

    async def create_order(self, order_items_list: list[CreateOrderDataClass]) -> NewSavedOrderDataClass:
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

        new_order = NewSavedOrderDataClass(
            order_id=new_order.order_id,
            list_of_orderItems=list_of_order_items
        )
        return new_order
