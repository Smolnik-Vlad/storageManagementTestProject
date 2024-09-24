from pydantic import BaseModel, field_validator, conint, ConfigDict

from src.core.exceptions import InvalidRequestDataException


class OrderCreateResponseModel(BaseModel):
    pass


class OrderCreateRequestModel(BaseModel):
    pass


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
