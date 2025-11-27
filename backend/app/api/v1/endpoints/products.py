from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.product import Product, ProductCreate
from app.crud.base import AbstractCRUD
from app.crud.product import ProductCRUD


class ProductController:
    """Controller for Product endpoints."""

    __router = APIRouter(prefix="/products", tags=["products"])
    __productCRUD: ProductCRUD = AbstractCRUD.create_crud()

    @__router.get("/", response_model=list[Product])
    async def read_products(self, skip: int = 0, limit: int = 100,
                            db: AsyncSession = Depends(get_db)):
        products = await self.__productCRUD.get(db, skip=skip, limit=limit)
        return products

    @__router.post("/", response_model=Product)
    async def create(self, product_in: ProductCreate,
                     db: AsyncSession = Depends(get_db)):
        return await self.__productCRUD.create(db, product_in)

    @__router.patch("/{product_id}", response_model=Product)
    async def update(self, product_id: int, updates: dict,
                     db: AsyncSession = Depends(get_db)):
        product = await self.__productCRUD.update(db, product_id, updates)
        if not product:
            raise HTTPException(404, "Product not found")
        return product

    @__router.delete("/{product_id}", response_model=Product)
    async def delete(self, product_id: int,
                     db: AsyncSession = Depends(get_db)):
        db_product = await self.__productCRUD.get_by_id(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return await self.__productCRUD.delete(db, product_id)

    def get_router(self):
        return self.__router
