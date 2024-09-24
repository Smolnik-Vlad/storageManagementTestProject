from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.ports.repositories.order_rep import OrderRepository


@dataclass
class SQLAlchemyOrderRepository(OrderRepository):
    _db_session: AsyncSession
