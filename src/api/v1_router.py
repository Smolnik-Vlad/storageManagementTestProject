from fastapi import APIRouter

from src.api.v1.order_router import order_router
from src.api.v1.product_router import product_router

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(product_router, prefix='/product', tags=['product'])
v1_router.include_router(order_router, prefix='/order', tags=['order'])
