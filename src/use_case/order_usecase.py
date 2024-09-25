from dataclasses import dataclass

from src.data_classes.order_product_dataclass import CreateOrderDataClass, UnsuccessfulOrderCreateDataClass, \
    OrderDataClass
from src.ports.repositories.order_rep import OrderRepository
from src.ports.repositories.product_rep import ProductRepository


@dataclass
class OrderUseCase:
    _order_repository: OrderRepository
    _product_repository: ProductRepository

    async def create_new_order(self, orderData: list[
        CreateOrderDataClass]) -> UnsuccessfulOrderCreateDataClass | OrderDataClass:
        prod_ids = [item.product_id for item in orderData]
        products = await self._product_repository.get_products_by_ids(prod_ids)
        dict_of_products_and_count = {product.product_id: product.count for product in products}

        list_of_ids_of_non_exist_products = []
        list_of_undercount_products = []

        for item in orderData:
            if item.product_id not in dict_of_products_and_count:
                list_of_ids_of_non_exist_products.append(item.product_id)
                continue
            if item.count > dict_of_products_and_count.get(item.product_id, None):
                list_of_undercount_products.append(item.product_id)
                continue

        if list_of_ids_of_non_exist_products or list_of_undercount_products:
            unsuccessful_products = UnsuccessfulOrderCreateDataClass(
                list_of_ids_of_non_exist_products=list_of_ids_of_non_exist_products,
                list_of_undercount_products=list_of_undercount_products
            )
            return unsuccessful_products

        saved_order = await self._order_repository.create_order(orderData)

        return saved_order

    async def get_orders(self) -> list[OrderDataClass]:
        orders = await self._order_repository.get_all_orders()
        return orders

    async def get_order_by_id(self, order_id: int) -> OrderDataClass:
        return await self._order_repository.get_order_by_id(order_id)

    async def update_order_status_by_id(self, order_id: int, status: str):
        return await self._order_repository.update_order_status(order_id, status)
