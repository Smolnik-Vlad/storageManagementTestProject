from dataclasses import dataclass

from sqlalchemy import exc, select, update
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
            db_response = await self._db_session.execute(query)
            result = db_response.scalars().all()
            return [self.__from_model_to_dataclass(prod) for prod in result]
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def get_product_by_id(self, product_id: int) -> ProductDataClass:
        try:
            query = select(Product).where(Product.product_id == product_id)
            db_response = await self._db_session.execute(query)
            result = db_response.scalar()
            return self.__from_model_to_dataclass(result) if result else None
        except exc.SQLAlchemyError:
            raise DatabaseException

    async def update_product_by_id(self, product_id: int, product: ProductDataClass) -> ProductDataClass:
        try:
            query = (update(Product)
                     .where(Product.product_id == product_id)
                     .values(**product.to_dict())
                     .returning(Product))
            res_database = await self._db_session.execute(query)
            result = res_database.scalar()
            user_result = self.__from_model_to_dataclass(result)
            return user_result

        except exc.SQLAlchemyError:
            raise DatabaseException

    async def get_products_by_ids(self, prod_ids: list[int]) -> list[ProductDataClass]:
        try:
            query = select(Product).where(Product.product_id.in_(prod_ids))
            db_response = await self._db_session.execute(query)
            result = db_response.scalars().all()
            return [self.__from_model_to_dataclass(prod) for prod in result]
        except exc.SQLAlchemyError:
            raise DatabaseException

