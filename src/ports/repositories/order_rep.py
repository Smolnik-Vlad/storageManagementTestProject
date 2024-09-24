from abc import ABC

from src.data_classes.order_product_dataclass import NewSavedOrderDataClass, CreateOrderDataClass


class OrderRepository(ABC):
    async def create_order(self, order_items_list: list[CreateOrderDataClass]) -> NewSavedOrderDataClass:
        pass

