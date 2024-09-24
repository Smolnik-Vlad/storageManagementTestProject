from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository
from src.adapters.repositories.sqlalchemy_ordertItem_repository import SQLAlchemyOrderItemRepository
from src.adapters.repositories.sqlalchemy_product_repository import SQLAlchemyProductRepository
from src.api.depends.database_depends import get_db
from src.ports.repositories.orderItem_rep import OrderItemRepository
from src.ports.repositories.order_rep import OrderRepository
from src.ports.repositories.product_rep import ProductRepository
from src.use_case.orderItem_use_case import OrderItemUseCase
from src.use_case.order_usecase import OrderUseCase
from src.use_case.product_usecase import ProductUseCase


def get_SQLAlchemyOrderRepository(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return SQLAlchemyOrderRepository(_db_session=db)


def get_SQLAlchemyProductRepository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return SQLAlchemyProductRepository(_db_session=db)


# def get_SQLAlchemyOrderItemRepository(db: AsyncSession = Depends(get_db)) -> OrderItemRepository:
#     return SQLAlchemyOrderItemRepository(_db_session=db)


def get_order_use_case(order_repo=Depends(get_SQLAlchemyOrderRepository),
                       product_repo=Depends(get_SQLAlchemyProductRepository)) -> OrderUseCase:
    return OrderUseCase(
        _order_repository=order_repo,
        _product_repository=product_repo
    )


def get_product_use_case(product_repo=Depends(get_SQLAlchemyProductRepository)) -> ProductUseCase:
    return ProductUseCase(
        _product_repository=product_repo
    )


# def get_orderItem_use_case(order_repo=Depends(get_SQLAlchemyOrderItemRepository)) -> OrderItemUseCase:
#     return OrderItemUseCase(
#         _orderItem_repository=order_repo
#     )


OrderUseCaseDependency = Annotated[OrderUseCase, Depends(get_order_use_case)]
# OrderItemUseCaseDependency = Annotated[OrderItemUseCase, Depends(get_orderItem_use_case)]
ProductUseCaseDependency = Annotated[ProductUseCase, Depends(get_product_use_case)]
