from abc import ABC, abstractmethod

from src.data_classes.order_product_dataclass import ProductDataClass


class ProductRepository(ABC):
    @abstractmethod
    async def add_new_product(self, product: ProductDataClass) -> ProductDataClass:
        pass

    @abstractmethod
    async def get_all_products(self) -> list[ProductDataClass]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> ProductDataClass:
        pass
