from src.data_classes.order_product_dataclass import ProductDataClass
from src.ports.repositories.product_rep import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: dict[int: ProductDataClass] = {}

    async def add_new_product(self, product: ProductDataClass) -> ProductDataClass:
        self.products[product.product_id] = product
        return product

    async def get_all_products(self) -> list[ProductDataClass]:
        return list(self.products.values())

    async def get_product_by_id(self, product_id: int) -> ProductDataClass | None:
        return self.products.get(product_id)

    async def update_product_by_id(self, product_id: int, product: ProductDataClass) -> ProductDataClass | None:
        if product_id in self.products:
            self.products[product_id] = product
            return product
        return None
