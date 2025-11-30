from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.product import Product, ProductCreate
from app.crud.base import AbstractCRUD
from app.crud.product import ProductCRUD

router = APIRouter(prefix="/products", tags=["products"])
product_crud: ProductCRUD = AbstractCRUD.create_crud(ProductCRUD)


@router.get("", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 100,
                        db: AsyncSession = Depends(get_db)):
    return await product_crud.get(db, skip=skip, limit=limit)


@router.post("", response_model=Product)
async def create_product(product_in: ProductCreate,
                         db: AsyncSession = Depends(get_db)):
    return await product_crud.create(db, product_in)


@router.patch("/{product_id}", response_model=Product)
async def update_product(product_id: int, updates: dict | None = None,
                         db: AsyncSession = Depends(get_db)):
    product = await product_crud.update(db, product_id, updates or {})
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.delete("/{product_id}", response_model=bool)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await product_crud.delete(db, product_id)
    if not result:
        raise HTTPException(404, "Product not found")
    return result
