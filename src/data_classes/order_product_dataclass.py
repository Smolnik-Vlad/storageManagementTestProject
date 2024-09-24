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
