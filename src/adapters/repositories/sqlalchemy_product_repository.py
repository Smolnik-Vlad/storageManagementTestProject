from dataclasses import dataclass

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.orm_engine.models import Product
from src.core.exceptions import DatabaseException
from src.data_classes.order_product_dataclass import ProductDataClass
from src.ports.repositories.product_rep import ProductRepository


@dataclass
class SQLAlchemyProductRepository(ProductRepository):
    _db_session: AsyncSession

    @staticmethod
    def __from_model_to_dataclass(db_prod: Product) -> ProductDataClass:
        return ProductDataClass(
            product_id=db_prod.product_id,
            title=db_prod.title,
            description=db_prod.description,
            price=db_prod.price,
            count=db_prod.count
        )

    async def add_new_product(self, product: ProductDataClass) -> ProductDataClass:
        try:
            new_product = Product(
                title=product.title,
                description=product.description,
                price=product.price,
                count=product.count
            )
            self._db_session.add(new_product)
            await self._db_session.flush()
            return self.__from_model_to_dataclass(new_product)
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def get_all_products(self) -> list[ProductDataClass]:
        try:
            query = select(Product)
            print(query)
            db_response = await self._db_session.execute(query)
            result = db_response.scalars().all()
            return [self.__from_model_to_dataclass(prod) for prod in result]
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def get_product_by_id(self, product_id: int) -> ProductDataClass:
        pass
