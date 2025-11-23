from fastapi import APIRouter
from .endpoints import products, users, cart


api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(users.router)
api_router.include_router(cart.router)
