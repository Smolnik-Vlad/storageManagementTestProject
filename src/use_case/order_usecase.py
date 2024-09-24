from dataclasses import dataclass

from src.ports.repositories.order_rep import OrderRepository


@dataclass
class OrderUseCase:
    _order_repository: OrderRepository

    async def create_new_order(self):
        pass

