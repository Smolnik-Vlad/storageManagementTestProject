from abc import ABC

from src.data_classes.order_product_dataclass import OrderDataClass, CreateOrderDataClass


class OrderRepository(ABC):
    async def create_order(self, order_items_list: list[CreateOrderDataClass]) -> OrderDataClass:
        pass

    async def get_order_by_id(self, order_id: int) -> OrderDataClass:
        pass

    async def get_all_orders(self) -> list[OrderDataClass]:
        pass

    async def update_order_status(self, order_id: int, new_status: str) -> OrderDataClass:
        pass