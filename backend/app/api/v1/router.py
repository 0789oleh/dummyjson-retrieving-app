from fastapi import APIRouter
from .endpoints import products, users, cart, dashboard


api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(users.router)
api_router.include_router(cart.router)
api_router.include_router(dashboard.router)


@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}
