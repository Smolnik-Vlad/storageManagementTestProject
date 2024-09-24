from dataclasses import dataclass

from src.ports.repositories.orderItem_rep import OrderItemRepository


@dataclass
class OrderItemUseCase:
    _orderItem_repository: OrderItemRepository
