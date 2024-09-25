from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api.depends.use_case_depends import OrderUseCaseDependency
from src.api.schemas import OrderCreateResponseModel, OrderCreateRequestModel, OrderCreateUnsuccessfulResponseModel, \
    OrderItemsResponseModel, OrderResponseModel, OrderUpdateRequestModel, UpdatedOrderStatusResponseModel
from src.data_classes.order_product_dataclass import CreateOrderDataClass, UnsuccessfulOrderCreateDataClass

order_router = APIRouter()


@order_router.post("/",
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


@order_router.get('/', response_model=list[OrderResponseModel], status_code=status.HTTP_200_OK)
async def get_orders(order_use_case: OrderUseCaseDependency):
    order_response = await order_use_case.get_orders()
    order_response_schema = [OrderResponseModel(
        list_of_orderItems=[OrderItemsResponseModel.model_validate(item) for item in order.list_of_orderItems],
        order_id=order.order_id,
        status=order.status)
        for order in order_response]
    return order_response_schema


@order_router.get('/{id}', response_model=OrderResponseModel, status_code=status.HTTP_200_OK)
async def get_order_by_id(id: int, order_use_case: OrderUseCaseDependency):
    order_response = await order_use_case.get_order_by_id(id)
    if order_response is None:
        return JSONResponse(None, status_code=status.HTTP_404_NOT_FOUND)

    list_of_itemOrder_items = [OrderItemsResponseModel.model_validate(item) for item in
                               order_response.list_of_orderItems]
    order_response = OrderResponseModel(
        list_of_orderItems=list_of_itemOrder_items,
        order_id=order_response.order_id,
        status=order_response.status)
    return order_response


@order_router.patch('/{id}', response_model=UpdatedOrderStatusResponseModel, status_code=status.HTTP_200_OK)
async def update_order_by_id(id: int, body: OrderUpdateRequestModel, order_use_case: OrderUseCaseDependency):
    order_response = await order_use_case.update_order_status_by_id(id, body.status)
    if order_response is None:
        return JSONResponse(None, status_code=status.HTTP_404_NOT_FOUND)
    order_response = UpdatedOrderStatusResponseModel.model_validate(order_response)
    return order_response
