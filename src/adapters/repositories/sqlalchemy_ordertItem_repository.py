from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.ports.repositories.orderItem_rep import OrderItemRepository


@dataclass
class SQLAlchemyOrderItemRepository(OrderItemRepository):
    _db_session: AsyncSession
