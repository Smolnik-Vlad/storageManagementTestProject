from fastapi import APIRouter

from src.api.v1.product_router import product_router

v1_router = APIRouter(tags=['v1'], prefix='/v1')
v1_router.include_router(product_router, prefix='/product')