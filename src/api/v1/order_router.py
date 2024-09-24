from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api.depends.use_case_depends import OrderUseCaseDependency
from src.api.schemas import OrderCreateResponseModel, OrderCreateRequestModel, OrderCreateUnsuccessfulResponseModel, \
    OrderItemsResponseModel
from src.data_classes.order_product_dataclass import CreateOrderDataClass, UnsuccessfulOrderCreateDataClass

order_router = APIRouter()


@order_router.post("/new_order",
                   response_model=OrderCreateResponseModel | dict[str, OrderCreateUnsuccessfulResponseModel],
                   status_code=status.HTTP_201_CREATED)
async def create_order(body: list[OrderCreateRequestModel], order_use_case: OrderUseCaseDependency):
    order_data = [CreateOrderDataClass(**orderItem.model_dump()) for orderItem in body]
    res = await order_use_case.create_new_order(order_data)
    if isinstance(res, UnsuccessfulOrderCreateDataClass):
        response_model = OrderCreateUnsuccessfulResponseModel.model_validate(res)
        res = response_model.model_dump()

        response_model_result = {'failed': res}

        return JSONResponse(response_model_result, status_code=status.HTTP_400_BAD_REQUEST)

    list_of_itemOrder_items = [OrderItemsResponseModel.model_validate(item) for item in res.list_of_orderItems]
    order_response = OrderCreateResponseModel(
        list_of_orderItems=list_of_itemOrder_items,
        order_id=res.order_id,
    )
    return order_response
