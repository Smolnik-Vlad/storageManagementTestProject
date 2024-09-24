from dataclasses import dataclass

from src.data_classes.order_product_dataclass import ProductDataClass
from src.ports.repositories.product_rep import ProductRepository


@dataclass
class ProductUseCase:
    _product_repository: ProductRepository

    async def create_new_product(self, product: ProductDataClass) -> ProductDataClass:
        created_product = await self._product_repository.add_new_product(product)
        return created_product

    async def get_products(self) -> list[ProductDataClass]:
        products = await self._product_repository.get_all_products()
        return products
