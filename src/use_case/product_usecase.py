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

    async def get_product_by_id(self, product_id: int) -> ProductDataClass:
        product = await self._product_repository.get_product_by_id(product_id)
        return product

    async def update_product_by_id(self, product_id: int, product: ProductDataClass) -> ProductDataClass | None:
        product.product_id = product_id
        if await self._product_repository.get_product_by_id(product_id) is not None:
            updated_product = await self._product_repository.update_product_by_id(product_id, product)
            return updated_product
        return None
