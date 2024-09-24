from fastapi import APIRouter, status

from src.api.depends.use_case_depends import OrderUseCaseDependency
from src.api.schemas import OrderCreateResponseModel, OrderCreateRequestModel

order_router = APIRouter()


@order_router.post("/new_order", response_model=OrderCreateResponseModel, status_code=status.HTTP_201_CREATED)
def create_order(request, body: OrderCreateRequestModel, order_use_case: OrderUseCaseDependency):
    order_use_case.create_new_order()
