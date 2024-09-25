from abc import ABC
from dataclasses import dataclass


class DataClassFunctionality(ABC):
    def to_dict(self, exclude_none=True) -> dict:
        if exclude_none:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        else:
            return self.__dict__.copy()


@dataclass
class ProductDataClass(DataClassFunctionality):
    product_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: float = 0.0
    count: int = 0


@dataclass
class CreateOrderDataClass(DataClassFunctionality):
    product_id: int
    count: int


@dataclass
class UnsuccessfulOrderCreateDataClass(DataClassFunctionality):
    list_of_ids_of_non_exist_products: list[int]
    list_of_undercount_products: list[int]


@dataclass
class NewOrderItemDataClass(DataClassFunctionality):
    product_id: int
    count: int


@dataclass
class OrderDataClass(DataClassFunctionality):
    order_id: int
    list_of_orderItems: list[NewOrderItemDataClass] | None = None
    status: str | None = None
