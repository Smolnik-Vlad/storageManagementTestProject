from fastapi import APIRouter, status

from src.api.depends.use_case_depends import ProductUseCaseDependency
from src.api.schemas import ProductCreateResponseModel, ProductCreateRequestModel, ProductGetResponseModel
from src.data_classes.order_product_dataclass import ProductDataClass

product_router = APIRouter()


@product_router.post('/', response_model=ProductCreateResponseModel, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreateRequestModel, product_use_case: ProductUseCaseDependency):
    product_data = ProductDataClass(**product_data.model_dump(exclude_none=True))
    product_response_data_class = await product_use_case.create_new_product(product_data)
    product_response = ProductCreateResponseModel(product_id=product_response_data_class.product_id,
                                                  title=product_response_data_class.title)
    return product_response


@product_router.get('/', response_model=list[ProductGetResponseModel])
async def get_products(product_use_case: ProductUseCaseDependency):
    products_data_class = await product_use_case.get_products()
    products_response = [ProductGetResponseModel.model_validate(p) for p in products_data_class]
    return products_response


@product_router.get('/{product_id}', response_model=ProductGetResponseModel | None)
async def get_product_by_id(product_id: int, product_use_case: ProductUseCaseDependency):
    product_data_class = await product_use_case.get_product_by_id(product_id)
    product_response = ProductGetResponseModel.model_validate(product_data_class) if product_data_class else None
    return product_response


@product_router.put('/{product_id}', response_model=ProductGetResponseModel | None)
async def update_product_by_id(product_id: int, product_data: ProductCreateRequestModel,
                               product_use_case: ProductUseCaseDependency):
    product_data = ProductDataClass(**product_data.model_dump(exclude_none=True))
    product_response_data_class = await product_use_case.update_product_by_id(product_id, product_data)
    product_response = ProductGetResponseModel.model_validate(
        product_response_data_class) if product_response_data_class else None
    return product_response
