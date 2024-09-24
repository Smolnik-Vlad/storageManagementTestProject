from pydantic import BaseModel, field_validator, conint, ConfigDict

from src.core.exceptions import InvalidRequestDataException


class OrderItemsResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    count: int


class OrderCreateResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    list_of_orderItems: list[OrderItemsResponseModel]


class OrderCreateUnsuccessfulResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    list_of_ids_of_non_exist_products: list[int]
    list_of_undercount_products: list[int]


class OrderCreateRequestModel(BaseModel):
    product_id: int
    count: int = conint(ge=1)(1)


class ProductCreateRequestModel(BaseModel):
    title: str
    description: str | None = None
    price: float = conint(ge=0)(0)
    count: int = conint(ge=0)(0)


class ProductCreateResponseModel(BaseModel):
    product_id: int
    title: str


class ProductGetResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    title: str
    description: str | None = None
    price: float = conint(ge=0)(0)
    count: int = conint(ge=0)(0)
