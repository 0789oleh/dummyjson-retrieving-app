from fastapi import APIRouter
from .endpoints import products, users, cart


api_router = APIRouter()
api_router.include_router(products.ProductController().get_router())
api_router.include_router(users.UserController().get_router())
api_router.include_router(cart.CartController().get_router())


@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}
